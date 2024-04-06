function drawPeople(data){
    const people = document.querySelector(".people")

    people.innerHTML = "";
                    
    for(let i = 0; i < data.length; i++){
        const personsArticle = document.createElement("article")
        personsArticle.classList.add("person")
        personsArticle.setAttribute("id",data[i]["chat_id"])


        const avatar = document.createElement("img")
        avatar.classList.add("avatar")
        avatar.setAttribute("src","img/avatar.jpeg")

        const personName = document.createElement("h1")
        personName.textContent = data[i]["user"]
        personName.classList.add("person-name")

        personsArticle.appendChild(avatar)
        personsArticle.appendChild(personName)

        people.appendChild(personsArticle)

        personsArticle.addEventListener("click", function() {
            const selectedPeople = document.querySelectorAll(".selected")
            // do something when the button is clicked
            console.log("You clicked a button");
            for (let i = 0; i < selectedPeople.length; i++){
                selectedPeople[i].classList.remove("selected");
            }
            personsArticle.classList.add("selected")
            const chatId = personsArticle.getAttribute("id")

            getChat(personsArticle)
            getSuggestions(chatId)

        })

    }
}

function drawChat(data){
    const messages = document.querySelector(".messages")
    messages.innerHTML = "";

    for(let i = 0; i < data.length; i++){
        const messageWrap = document.createElement("div")
        messageWrap.classList.add("message-wrap")
                    
        const message = document.createElement("section")
        message.classList.add("message")

        if (data[i].user === "Me"){
            message.classList.add("user-message")

        }

                    

        const messageText = document.createElement("p")
        messageText.textContent = data[i]["message"]

        const messageTime = document.createElement("p")
        messageTime.textContent = "12:19"
        messageText.classList.add("time")

        if(data[i].user !== "Me"){
            const personsName = document.createElement("h1")
            personsName.textContent = data[i]["user"]
            personsName.classList.add("person-name-message")
            message.appendChild(personsName)
        }

                    
        message.appendChild(messageText)
        message.appendChild(messageTime)

        messageWrap.appendChild(message)

        messages.appendChild(messageWrap)
                    
    }
}

function getChat(personsArticle){
    const chat_id = personsArticle.getAttribute("id")

    const HTTP = new XMLHttpRequest();
    const url = 'http://127.0.0.1:5000/messages/'+ chat_id;
    HTTP.open("GET", url);
    HTTP.send();

    HTTP.onreadystatechange = (e) => {
        if (HTTP.readyState === XMLHttpRequest.DONE) {
            if (HTTP.status === 200) {
                const data = JSON.parse(HTTP.responseText)

                drawChat(data)
                
            }
        }
    }
}

function getPeople(){
        const HTTP = new XMLHttpRequest();
        const url='http://127.0.0.1:5000/chats';
        HTTP.open("GET", url);
        HTTP.send();

        HTTP.onreadystatechange = (e) => {
            if (HTTP.readyState === XMLHttpRequest.DONE) {
                if (HTTP.status === 200) {
                    const data = JSON.parse(HTTP.responseText)
                    console.log(data)
                    
                    drawPeople(data)
                    
                }
            }
        }
}

function drawSuggestions(data){
    const suggestions = document.querySelectorAll(".suggestion")

    for(let i = 0; i < suggestions.length; i++){
        suggestions[i].children[1].textContent = data[i]
    }
}

function getSuggestions(chatId){
    const HTTP = new XMLHttpRequest();
    const url = "http://127.0.0.1:5000/suggestions/" + chatId;
    HTTP.open("GET", url);
    HTTP.send();

    HTTP.onreadystatechange = (e) => {
        if (HTTP.readyState === XMLHttpRequest.DONE) {
            if (HTTP.status === 200) {
                const data = JSON.parse(HTTP.responseText)
                console.log(data)
                
                drawSuggestions(data)
                
            }
        }
    }


}

function sendMessage(){
    const inputText = document.querySelector('.input-text').value;
    const personsArticle = document.querySelector(".selected")
    const chatId = personsArticle.getAttribute("id")


    const formData = new FormData();
    formData.append('name', "Me");
    formData.append('message', inputText);
    formData.append("chat_id", chatId)

    const HTTP = new XMLHttpRequest();
    const url = "http://127.0.0.1:5000/message";
    HTTP.open("POST", url);
    HTTP.send(formData);

    HTTP.onreadystatechange = (e) => {
        if (HTTP.readyState === XMLHttpRequest.DONE) {
            if (HTTP.status === 200) {
                
                getChat(personsArticle)
                getSuggestions(chatId)
                
            }
        }
    }
}


