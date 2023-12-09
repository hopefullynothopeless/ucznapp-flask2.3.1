from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import random
from flaskext.markdown import Markdown

app = Flask(__name__)
app.config['UPLOAD_FOLDER']="E:\\Apps\\Релевантные\\ucznapp-flask2.3.1\\app\\books"
Markdown(app, output_format='html4', extensions=['fenced_code', 'tables', 'abbr', 'footnotes'])

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database = SQLAlchemy(app)

class Entry(database.Model):
    entry_id = database.Column(database.Integer, primary_key=True)
    entry_title = database.Column(database.String(150))
    entry_content = database.Column(database.String(7000))
    entry_active = database.Column(database.Boolean)

class Note(database.Model):
    note_id = database.Column(database.Integer, primary_key=True)
    note_content = database.Column(database.String(150))
    note_important = database.Column(database.Boolean)
    note_not_important = database.Column(database.Boolean)

with app.app_context():
    database.create_all()

@app.route('/')
def main():
    entries_list = database.session.query(Entry).all()
    return render_template('main.html', entries_list=entries_list)

@app.route('/searchpage')
def searchpage():
    return render_template('searchresults.html')

@app.route('/searchentry')
def searchentry():
    query_value = request.args.get("searchfield")
    if query_value:
        res = database.session.query(Entry).filter(Entry.entry_title.icontains(query_value) | Entry.entry_content.icontains(query_value))\
        .order_by(Entry.entry_id.asc()).all()
    else:
        res = []

    return render_template('resulttemplate.html', searchresults=res)
    
#-----------------BOOKS-----------------

@app.route('/book1')
def book1():
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'Linux_Книга_рецептов_2-е_изд.pdf')

@app.route('/book2')
def book2():
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'DevOpsbook.pdf')

@app.route('/book3')
def book3():
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'Docker_на_практике.pdf')

@app.route('/book4')
def book4():
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'Linux_Командная_строкa.pdf')

@app.route('/book5')
def book5():
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'Python_для_сетевых_инженеров.pdf')

@app.route('/book6')
def book6():
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'Python_и_DevOps_Ключ_к_автоматизации_Linux.pdf')

@app.route('/book7')
def book7():
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'Unixtoolbox_rus.pdf')

@app.route('/book8')
def book8():
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'Анализ_пакетов.pdf')

@app.route('/book9')
def book9():
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'Восстановление_данных_Практическое_руководство_2_е_изд.pdf')

@app.route('/book10')
def book10():
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'Компьютерные_сети_Принципы_технологии_протоколы.pdf')

@app.route('/book11')
def book11():
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'Компьютерные_сети_Танненбаум_6_изд.pdf')

#---------------------------------------------------------------

@app.route('/add_entry_page')
def addentry():
    return render_template('add_entry_page.html')

@app.route('/get_me_out_of_here')
def get_me_out_of_here():
    popular_sites = ['https://habr.com/ru/articles/', 'https://proglib.io/', 
                     'https://dtf.ru/', 'https://pikabu.ru/', 'https://4pda.to/']
    final_choice = random.choice(popular_sites)
    return redirect(final_choice)

@app.get('/entry/<int:entry_id>')
def get_entry(entry_id):
    entry = database.session.query(Entry).filter(Entry.entry_id == entry_id).first()
    return render_template("entry_page.html", entry=entry)

#-----------------NOTES-----------------

@app.get('/notes.html')
def notes():
    notes_list = database.session.query(Note).all()
    print(notes_list)
    return render_template('notes.html', notes_list=notes_list)

@app.post('/add_note')
def add_note():
    note_content = request.form.get("note_content")
    if note_content == "":
        return redirect(url_for('notes'))
    
    important = False
    not_important = False
    if request.form.get("important"):
        important = True
    if request.form.get("not_important"):
        not_important = True
    new_note = Note(note_content=note_content, note_important=important,
                    note_not_important=not_important)
    
    database.session.add(new_note)
    database.session.commit()
    return redirect(url_for('notes'))

@app.post('/delete_note/<int:note_id>')
def delete_note(note_id):
    note = database.session.query(Note).filter(Note.note_id == note_id).first()
    database.session.delete(note)
    database.session.commit()
    return redirect(url_for('notes'))

#---------------------------------------------------------------

@app.post('/add_entry')
def add_entry():
    entry_title = request.form.get("entry_title")
    entry_content = request.form.get("entry_content")
    new_entry = Entry(entry_title=entry_title, entry_content=entry_content, entry_active=True)
    database.session.add(new_entry)
    database.session.commit()
    return redirect(url_for("main"))

@app.post('/modify_entry/<int:entry_id>')
def modify_entry(entry_id):
    entry = database.session.query(Entry).filter(Entry.entry_id == entry_id).first()
    entry.entry_active = False
    database.session.commit()
    return redirect(url_for("main"))

@app.post('/delete_entry/<int:entry_id>')
def delete_entry(entry_id):
    entry = database.session.query(Entry).filter(Entry.entry_id == entry_id).first()
    if not entry.entry_active:
        database.session.delete(entry)
        database.session.commit()
        return redirect(url_for("main"))
    else:
        return redirect(url_for("main"))
    
@app.post('/untag_entry/<int:entry_id>')
def untag_entry(entry_id):
    entry = database.session.query(Entry).filter(Entry.entry_id == entry_id).first()
    if not entry.entry_active:
        entry.entry_active = True
        database.session.commit()
    return redirect(url_for("main"))


if __name__ == "__main__":
    app.run(debug=True)