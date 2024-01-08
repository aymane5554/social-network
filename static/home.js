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

function load_posts(url){

    return new Promise((resolve,reject)=>{
        posts = document.getElementById('posts');
        fetch(url)
        .then(response => response.json())
        .then(data =>{
            for(i in data){
                poster = document.createElement("div");
                poster.className = "poster";
                posts.appendChild(poster);
                a = document.createElement('a');
                a.setAttribute("href",`/account/${data[i].user[1]}`);
                userImg = document.createElement("img");
                userImg.setAttribute("src",`${data[i].user[2]}`) ;
                userImg.setAttribute("class","pfps") ;
                a.appendChild(userImg);
                a.innerHTML += `${data[i].user[1]}`;
                poster.appendChild(a);
                if(data[i].text != null){
                    poster.innerHTML += `<p class="post_text">${data[i].text}</p>`;
                }
                if(data[i].image != null){
                    poster.innerHTML += `<a href="/p/${data[i].id}"><img src="${data[i].image}" class="post_img"></a>`;
                }
                poster.innerHTML += `<hr>`;
                like = document.createElement("button");
                like.className = "like-btn";
                like.innerHTML = "like";
                like.setAttribute("onclick",`like_post(${data[i].id})`);
                button = document.createElement("button");
                button.className = "cmt-btn";
                button.innerHTML = "comments";
                save = document.createElement("button");
                save.className = "save-btn";
                save.innerHTML = "save";    
                button.setAttribute("data-id",`${data[i].id}`);
                button.setAttribute("onclick",`cmnt(${data[i].id})`);
                save.setAttribute("onclick",`s(${data[i].id})`);
                save.setAttribute("data-id",`${data[i].id}`);
                share = document.createElement("button");
                share.setAttribute("data-id",`${data[i].id}`);
                share.className = "share-btn";
                share.innerHTML = "=>";
                poster.appendChild(like);
                poster.appendChild(button);
                poster.appendChild(save);
                poster.appendChild(share);
                poster.innerHTML += `<p id="l${data[i].id}">${data[i].likes}</p><form  onsubmit="post_comment(${data[i].id});return false" id="c${data[i].id}">
                <textarea name="comment" id="textarea${data[i].id}" placeholder="comment" cols="30" rows="10"></textarea>
                <br>
                <input type="hidden" name="postId" value="${data[i].id}">
                <input type="submit" name="comment_submit">
                </form>`;
                poster.innerHTML += `<div id="cmnts${data[i].id}"></div>`
            }
        });

        resolve("Done");
    });
}

function cmnt(id){
    fetch(`/api/comments/${id}`)
    .then(response=>response.json())
    .then(data => {
        div = document.getElementById(`cmnts${id}`);
        div.innerHTML = '<b>comments : </b>';
        for(i = 0 ; i < data.length;i++){
            div.innerHTML += `<p><b><a href="account/${data[i]['user'][1]}"> ${data[i]['user'][1]} :</a></b> ${data[i]['text']}</p>`;
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
        body: JSON.stringify("save")
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

function like_post(id){
    fetch(`/api/${id}`, {
        method: "put",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify("like")
    })
    .then(response => response.json())
    .then(data=>{
        p = document.getElementById(`l${id}`);
        p.innerHTML = data['likes'];
    });
}

document.addEventListener("DOMContentLoaded",async function(){
    await load_posts("/api/feed") 
});
