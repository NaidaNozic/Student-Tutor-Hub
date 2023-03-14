

var el = document.getElementById('buttonPosts');
if(el){
    el.addEventListener("click", () => {
        document.getElementById('addQuestions').style.display = "none"
        document.getElementById('questions').style.display = "none"
        document.getElementById('posts').style.display = ""
        document.getElementById('assignmentsDiv').style.display = "none"
});
}

var el1 = document.getElementById('buttonQuestions');
if(el1){
    el1.addEventListener("click", () => {
        document.getElementById('posts').style.display = "none"
        document.getElementById('addQuestions').style.display = ""
        document.getElementById('questions').style.display = ""
        document.getElementById('assignmentsDiv').style.display = "none"
    });
}

var el2 = document.getElementById('buttonAssignments');
if(el2){
    el2.addEventListener("click", () => {
        document.getElementById('assignmentsDiv').style.display = ""
        document.getElementById('posts').style.display = "none"
        document.getElementById('addQuestions').style.display = "none"
        document.getElementById('questions').style.display = "none"
    });
}