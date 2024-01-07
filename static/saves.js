function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function cmnt(id){
    fetch(`/api/comments/${id}`)
    .then(response=>response.json())
    .then(data => {
        div = document.getElementById(`cmnts${id}`);
        div.innerHTML = '<b>comments : </b>';
        for(i = 0 ; i < data.length;i++){
            div.innerHTML += `<p><b> ${data[i]['user'][1]} :</b> ${data[i]['text']}</p>`;
        } 
    });

}

function s(id){
    fetch(`/api/${id}`, {
        method: "put",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify(" ")
    })
    .then(response => response.json())
    .then(data=>console.log(data));
}


function post_comment(id){
    form = $(`#c${id}`).serializeArray();
    if(form[0].value === ""){
        return;
    } 
    data = {text : form[0].value ,post : form[1].value};
    fetch(`/api/comments/${id}`, {
        method: "post",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data=>{
        cmnt(id); 
    });
    document.querySelector(`#textarea${id}`).value = "";
    
}