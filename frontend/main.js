const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
// const fileUploadLabel = document.getElementById('file-upload-label');
// const fileUploadMenu = document.getElementById('file-upload-menu');
// const fileOptions = document.querySelectorAll('.file-option');
// const fileInputs = document.querySelectorAll('.file-input');
const chatHistory = document.querySelector('.chat-history');
const form = document.getElementById('message-form');
let userId = localStorage.getItem("userId");
const chatsUrl = `http://127.0.0.1:8000/chats/${userId}`; // Ajusta la URL según tu configuración

function addMessage(message, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
    function formatMessage(message) {
        // Reemplazar negritas
        let formattedMessage = message.replace(/\*\*(.*?)\*\*/g, "<b>$1</b>");
        
        // Reemplazar tachado
        formattedMessage = formattedMessage.replace(/~~(.*?)~~/g, "<s>$1</s>");
        
        // Reemplazar saltos de línea por <br>
        formattedMessage = formattedMessage.replace(/\n/g, "<br>");
        
        // Reemplazar líneas que comienzan con * por viñetas
        formattedMessage = formattedMessage.replace(/^\*(.*?)$/gm, "<li>$1</li>");
        
        // Envolver las viñetas en <ul> si existen
        if (formattedMessage.includes("<li>")) {
            formattedMessage = formattedMessage.replace(/<li>/g, "<ul><li>").replace(/<\/li>/g, "</li></ul>");
        }

        return formattedMessage;
    }
      
      const formatted = formatMessage(message);
      console.log(formatted);
      
    messageDiv.innerHTML += formatted;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Función para actualizar la barra lateral con los chats
function updateChatHistory(chats) {
    const chatHistoryList = document.querySelector('.chat-history');
    chatHistoryList.innerHTML = ''; // Limpiar el historial de chats existente

    chats.forEach(chat => {
        const chatItem = document.createElement('li');
        chatItem.textContent = chat.chatName; // Ajusta según el campo que desees mostrar
        chatItem.setAttribute("id", chat.chatId);
        chatItem.setAttribute("class", "chat");
        chatHistoryList.appendChild(chatItem);

        // Agregar evento de clic para cargar los mensajes del chat seleccionado
        chatItem.addEventListener('click', () => {
            loadMessages(chat.chatId); // Cargar mensajes del chat seleccionado
            setActiveChat(chatItem);  // Marcar chat como activo
        });
    });

    // Seleccionar el primer chat por defecto (si existe)
    if (chats.length > 0) {
        const firstChat = document.getElementById(chats[0].chatId);
        firstChat.classList.add('active');
        selectedChatId = chats[0].chatId
        loadMessages(selectedChatId);
    }
}

// Función para cargar los chats
async function loadChats() {
    try {
        const response = await fetch(chatsUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error('Error al obtener los chats');
        }

        const chats = await response.json();
        updateChatHistory(chats);
    } catch (error) {
        console.error('Error al cargar los chats:', error);
    }
}

// Función para marcar el chat activo
function setActiveChat(chatItem) {
    const chatItems = document.getElementsByClassName('chat');
    Array.from(chatItems).forEach(item => item.classList.remove('active'));
    chatItem.classList.add('active');
}

 // Función para cargar los mensajes de un chat específico
 async function loadMessages(chatId) {
    const messagesUrl = `http://127.0.0.1:8000/messages/chat/${chatId}`;

    try {
        const response = await fetch(messagesUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error('Error al obtener los mensajes');
        }

        const messages = await response.json();
        updateMessages(messages);
    } catch (error) {
        console.error('Error al cargar los mensajes:', error);
    }
}

// Función para actualizar los mensajes en el chat
function updateMessages(messages) {
    chatMessages.innerHTML = ''; // Limpiar el historial de mensajes existente

    messages.forEach(message => {
        let user = message.userId == userId; // Verifica si el mensaje es del usuario actual
        addMessage(message.content, user);
    });
}

document.addEventListener('DOMContentLoaded', async (e) => {
    // Cargar los chats al iniciar
    loadChats();
});

    // Función para agregar un nuevo chat
    async function addChat(){
        const chatName = prompt('Ingresa el título del nuevo chat:');
    
        if (!chatName) {
            alert('El título del chat es necesario.');
            return;
        }

        try {
            const response = await fetch(chatsUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({"chatName": chatName, "userId": localStorage.getItem("userId")})
            });

            if (!response.ok) {
                throw new Error('Error al agregar el chat');
            }

            // Vuelve a cargar los chats después de agregar uno nuevo
            loadChats();
        } catch (error) {
            console.error('Error al agregar el chat:', error);
        }
    };

form.addEventListener('submit', function(event) {
    event.preventDefault(); // Prevenir el comportamiento por defecto (refrescar la página)
    handleUserInput(); // Llamar a la función que maneja el envío del mensaje
});

async function handleUserInput() {
    const userInput = document.getElementById("user-input");
    const message = userInput.value.trim();

    if (message) {
        addMessage(message, true); // Añadir el mensaje del usuario al DOM sin recargar todo
        userInput.value = '';

        try {
            const data = {
                content: message,
                chatId: selectedChatId, 
                userId: localStorage.getItem("userId")
            };

            const response = await fetch('http://127.0.0.1:8000/messages/gemini', {
                method: 'POST',
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) throw new Error('Error en la respuesta de la red');

            const result = await response.json();

            // Añadir la respuesta del servidor al DOM
            if (result && result.message) {
                addMessage(result.message, false); // Añadir el mensaje del sistema al DOM
            } else {
                throw new Error('Respuesta inesperada del servidor');
            }

        } catch (error) {
            console.error('Error procesando la respuesta:', error);
        }
    }
}


// function handleFileUpload(event) {
//     const file = event.target.files[0];
//     if (file) {
//         const fileType = event.target.accept.split('/')[0];
//         addMessage(`Archivo ${fileType} seleccionado: ${file.name}`, true);
//         setTimeout(() => {
//             const botResponse = `He recibido tu archivo ${fileType}. En una implementación real, aquí procesaríamos el archivo y responderíamos de acuerdo a su contenido.`;
//             addMessage(botResponse);
//         }, 1000);
//     }
// }

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault()
        handleUserInput();
    }
});

// fileUploadLabel.addEventListener('click', (e) => {
//     e.stopPropagation();
//     fileUploadMenu.style.display = fileUploadMenu.style.display === 'flex' ? 'none' : 'flex';
// });

// fileOptions.forEach(option => {
//     option.addEventListener('click', (e) => {
//         const fileType = e.target.closest('.file-option').getAttribute('data-type');
//         document.getElementById(`file-upload-${fileType}`).click();
//         fileUploadMenu.style.display = 'none';
//     });
// });

// fileInputs.forEach(input => {
//     input.addEventListener('change', handleFileUpload);
// });

// document.addEventListener('click', () => {
//     fileUploadMenu.style.display = 'none';
// });

chatHistory.addEventListener('click', async (e) => {
    if (e.target.tagName === 'LI') {
        chatHistory.querySelectorAll('li').forEach(li => li.classList.remove('active'));
        e.target.classList.add('active');

        selectedChatId = e.target.id;
        console.log(selectedChatId)

        // Aquí se simularía la carga del chat seleccionado
            chatMessages.innerHTML = '';
        const chatsUrl = `http://127.0.0.1:8000/messages/chat/${selectedChatId}`;

    // Función para cargar los chats
    async function loadMessages() {
        try {
            const response = await fetch(chatsUrl, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (!response.ok) {
                throw new Error('Error al obtener los chats');
            }

            const messages = await response.json();
            updateMessages(messages);
        } catch (error) {
            console.error('Error al cargar los chats:', error);
        }
    }

    function updateMessages(messages) {
        chatMessages.innerHTML = ''; // Limpiar el historial de chats existente

        messages.forEach(message => {
            let user = true
            if(message.userId == 3){
                user = false
            }
            addMessage(message.content, user)
        });
    }

    loadMessages();
    }
});

document.getElementById('send-button').addEventListener('click', async function() {
    e.preventDefault()
    const userInput = document.getElementById('user-input').value;

    if (!userInput.trim()) {
        alert('Por favor, ingresa un mensaje.');
        return;
    }

    try {
        const response = await fetch('http://localhost:8000/messages', {  // Reemplaza con la URL de tu API
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ content: userInput }),
        });

        if (response.ok) {
            const data = await response.json();
            // Actualiza la interfaz con el nuevo mensaje
            const chatMessages = document.getElementById('chat-messages');
            const newMessage = document.createElement('div');
            newMessage.className = 'message user-message';
            newMessage.textContent = userInput;
            chatMessages.appendChild(newMessage);
            document.getElementById('user-input').value = '';
        } else {
            const errorData = await response.json();
            alert(`Error: ${errorData.message || 'No se pudo enviar el mensaje.'}`);
        }
    } catch (error) {
        alert('Error de red: ' + error.message);
    }
});

document.getElementById('add-chat-button').addEventListener('click', async function(e) {
    e.preventDefault()
    const chatName= prompt('Ingresa el título del nuevo chat:');
    
    if (!chatName) {
        alert('El título del chat es necesario.');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/chats', {  // Reemplaza con la URL de tu API
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ chatName: chatName, userId: localStorage.getItem("userId") }),
        });

        if (response.ok) {
            const data = await response.json();
            // Actualiza la interfaz con el nuevo chat
            const chatHistory = document.querySelector('.chat-history');
            const newChatItem = document.createElement('li');
            newChatItem.textContent = chatName;
            chatHistory.appendChild(newChatItem);
        } else {
            const errorData = await response.json();
            alert(`Error: ${errorData.message || 'No se pudo agregar el chat.'}`);
        }
    } catch (error) {
        alert('Error de red: ' + error.message);
    }
});