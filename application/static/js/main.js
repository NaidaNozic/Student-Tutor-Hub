

var el = document.getElementById('buttonPosts');
if(el){
}
    el.addEventListener("click", () => {
        document.getElementById('questions').style.display = "none"
    document.getElementById('posts').style.display = ""
});

var el1 = document.getElementById('buttonQuestions');
if(el1){
}
    el1.addEventListener("click", () => {
    document.getElementById('posts').style.display = "none"
    document.getElementById('questions').style.display = ""
});