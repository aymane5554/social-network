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
            if (data[i].is_share == true){
                main = document.createElement("div");
                main.className = "poster";
                posts.appendChild(main);
                a = document.createElement('a');
                a.setAttribute("href",`/account/${data[i].user[1]}`);
                userImg = document.createElement("img");
                userImg.setAttribute("src",`${data[i].user[2]}`) ;
                userImg.setAttribute("class","pfps") ;
                a.appendChild(userImg);
                a.innerHTML += `${data[i].user[1]}`;
                main.appendChild(a);
                if(data[i].text != null){
                    main.innerHTML += `<p class="post_text">${data[i].text}</p>`;
                }
                //#################################################################
                //#################################################################
                poster = document.createElement("div");
                poster.className = "shared_posts";
                
                a = document.createElement('a');
                a.setAttribute("href",`/account/${data[i].shared[1]}`);
                userImg = document.createElement("img");
                userImg.setAttribute("src",`${data[i].shared[2]}`) ;
                userImg.setAttribute("class","pfps") ;
                a.appendChild(userImg);
                a.innerHTML += `${data[i].shared[1]}`;
                poster.appendChild(a);
                if(data[i].shared[3] != null){
                    poster.innerHTML += `<p class="post_text">${data[i].shared[3]}</p>`;
                }
                if(data[i].shared[4] != null){
                    poster.innerHTML += `<a href="/p/${data[i].id}"><img src="${data[i].shared[4]}" class="post_img"></a>`;
                }
                
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
                share.setAttribute("data-id",`${data[i].shared[0]}`);
                share.className = "share-btn";
                share.innerHTML = "=>";
                share.setAttribute("onclick",`share_post(${data[i].shared[0]})`);
                main.appendChild(poster);
                main.appendChild(like);
                main.appendChild(button);
                main.appendChild(save);
                main.appendChild(share);
                main.innerHTML += `<p id="l${data[i].id}">${data[i].likes}</p><form  onsubmit="post_comment(${data[i].id});return false" id="c${data[i].id}">
                <textarea name="comment" id="textarea${data[i].id}" placeholder="comment" cols="30" rows="10"></textarea>
                <br>
                <input type="hidden" name="postId" value="${data[i].id}">
                <input type="submit" name="comment_submit">
                </form>`;
                main.innerHTML += `<div id="cmnts${data[i].id}"></div>`;
                
                continue;
            }
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
            share.setAttribute("onclick",`share_post(${data[i].id})`);
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

function show_users(){
        pdiv = document.getElementById("result-posts");
        udiv = document.getElementById("result-users");
        udiv.style.display = "block";
        pdiv.style.display = "none";
    }
    
async function show_posts(){
        pdiv = document.getElementById("result-posts");
        udiv = document.getElementById("result-users");
        udiv.style.display = "none";
        pdiv.style.display = "block";
        s = document.getElementById("show-posts-btn").dataset.s;
        await load_posts(`/api/result${s}`) 
}
    
function cmnt(id){
    fetch(`/api/comments/${id}`)
    .then(response=>response.json())
    .then(data => {
        div = document.getElementById(`cmnts${id}`);
        div.innerHTML = '<b>comments : </b>';
        for(i = 0 ; i < data.length;i++){
            div.innerHTML += `<p><a href="account/${data[i]['user'][1]}"><b> ${data[i]['user'][1]} :</a></b> ${data[i]['text']} -- <button onclick="reply(${data[i]['post']},${data[i]["id"]})">reply</button></p>`;
            for(j = 0 ; j < data[i]["reply"].length ; j++){
                div.innerHTML += `<p style="margin-left: 5%;"><b>${data[i]["reply"][j]["user"]} : </b> ${data[i]["reply"][j]["text"]}</p>`;
            }
        } 
    });

}

function reply(pid,id){
    div = document.querySelector("#reply");
    if(div != null){
        div.remove();
    }
    div = document.createElement('div');
    div.innerHTML += `<h2> reply ${id}<h2>`;
    div.setAttribute("id","reply");
    div.style.backgroundColor = "grey";
    div.style.padding = "1%";
    div.style.position = "absolute";
    div.style.width = "70%";
    y = window.scrollY+(window.innerHeight*0.3);
    div.style.top = `${y}px`;
    div.style.left = "15%";
    div.style.height = "200px";
    div.innerHTML += `<form id="replyForm" onsubmit="post_reply(${pid},${id});return false">
    <textarea name="recmnt" id="pc_id" cols="30" rows="10" placeholder="reply" style="width: 100%;"></textarea><br>
    <input type="hidden" name="Id" value="${pid}">
    <button type="submit" id="sb" name="post_submit">share</button>
    </form>`;
    document.querySelector("body").appendChild(div);
}

function post_reply(pid,cid){
    form = $("#replyForm").serializeArray();
    if(form[0].value == ""){
        return false;
    }
    data = {text : form[0].value ,post : form[1].value,reply :cid};
    fetch(`/api/comments/${pid}`, {
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
        send_notification("reply",data.comment)
        cmnt(pid); 
    });
    div = document.querySelector("#reply");
    if(div != null){
        div.remove();
    }

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
    data = {text : form[0].value ,post : form[1].value , reply : null};
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
        send_notification("comment",data.post)
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
        send_notification("like",data.id);
    });
}

function share_post(id){
    div = document.querySelector("#shp");
    if(div != null){
        div.remove();
    }
    div = document.createElement('div');
    div.innerHTML += `<h2> share ${id}<h2>`;
    div.setAttribute("id","shp");
    div.style.backgroundColor = "grey";
    div.style.padding = "1%";
    div.style.position = "absolute";
    div.style.width = "70%";
    y = window.scrollY+(window.innerHeight*0.3);
    div.style.top = `${y}px`;
    div.style.left = "15%";
    div.style.height = "200px";
    div.innerHTML += `<form id="shaaaaaare" onsubmit="spp();return false">
    <textarea name="cntnt" id="pc_id" cols="30" rows="10" placeholder="say something" style="width: 100%;"></textarea><br>
    <input type="hidden" name="Id" value="${id}">
    <button type="submit" id="sb" name="post_submit">share</button>
    </form>`;
    document.querySelector("body").appendChild(div);
}
function spp(){
    form = $("#shaaaaaare").serializeArray();
    
    data  = {"text":form[0].value,"id":form[1].value};
    fetch(`/api/share`, {
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
        send_notification("share",data.shared);
    });
    div = document.querySelector("#shp");
    if(div != null){
        div.remove();
    }
}

function send_notification(text,user){
    data = {note : `${text}` , id : user};
    fetch(`/api/inbox`, {
        method: "post",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
}
