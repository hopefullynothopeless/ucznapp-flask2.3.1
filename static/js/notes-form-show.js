let the_add_link = document.getElementById('add');
console.log(the_add_link);
the_add_link.addEventListener("click", () =>{
    let flex_container = document.querySelector('.flex-container');
    flex_container.style.display = 'flex';
});

