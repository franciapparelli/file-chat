const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const fileUploadLabel = document.getElementById('file-upload-label');
const fileUploadMenu = document.getElementById('file-upload-menu');
const fileOptions = document.querySelectorAll('.file-option');
const fileInputs = document.querySelectorAll('.file-input');
const chatHistory = document.querySelector('.chat-history');

document.addEventListener('DOMContentLoaded', () => {
    // URL del endpoint para obtener chats del usuario
    let userId = localStorage.getItem("userId")
    const chatsUrl = `http://127.0.0.1:8000/chats/${userId}`; // Ajusta la URL según tu configuración

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
        });
    }

    // Llama a la función para cargar los chats al cargar la página
    loadChats();

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
});

function addMessage(message, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
    function formatMessage(message) {
        // Reemplazar negritas
        let formattedMessage = message.replace(/\*\*(.*?)\*\*/g, "<b>$1</b>");
        
        // Reemplazar cursivas
        formattedMessage = formattedMessage.replace(/\*(.*?)\*/g, "<i>$1</i>");
        
        // Reemplazar tachado
        formattedMessage = formattedMessage.replace(/~~(.*?)~~/g, "<s>$1</s>");
        
        // Reemplazar saltos de línea
        formattedMessage = formattedMessage.replace(/\n/g, "<br>");
        
        // Aquí puedes agregar más reglas de formato según lo necesites
        
        return formattedMessage;
      }
      
      const formatted = formatMessage(message);
      console.log(formatted);
      
    messageDiv.innerHTML = formatted;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function handleUserInput() {
    const message = userInput.value.trim();
    if (message) {
        addMessage(message, true);
        userInput.value = '';

        // Usar una promesa para retrasar la ejecución y manejar async correctamente
        try {
            const data = {
                content: message,
                chatId: selectedChatId, // Asegúrate de usar el chatId seleccionado
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

            if (!response.ok) {
                throw new Error('Error en la respuesta de la red');
            }

            const botResponse = await response.json(); // Asumiendo que el servidor devuelve JSON
            addMessage(botResponse.response); // Ajusta según la estructura de la respuesta del servidor
        } catch (error) {
            console.error('Hubo un problema con la operación fetch:', error);
            addMessage('Lo siento, hubo un error al procesar tu solicitud.');
        }
    }
}

function handleFileUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const fileType = event.target.accept.split('/')[0];
        addMessage(`Archivo ${fileType} seleccionado: ${file.name}`, true);
        setTimeout(() => {
            const botResponse = `He recibido tu archivo ${fileType}. En una implementación real, aquí procesaríamos el archivo y responderíamos de acuerdo a su contenido.`;
            addMessage(botResponse);
        }, 1000);
    }
}

sendButton.addEventListener('click', async (event) => {
    // Previene el comportamiento por defecto del botón (como enviar un formulario)
    event.preventDefault();

    await handleUserInput();
});

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleUserInput();
    }
});

fileUploadLabel.addEventListener('click', (e) => {
    e.stopPropagation();
    fileUploadMenu.style.display = fileUploadMenu.style.display === 'flex' ? 'none' : 'flex';
});

fileOptions.forEach(option => {
    option.addEventListener('click', (e) => {
        const fileType = e.target.closest('.file-option').getAttribute('data-type');
        document.getElementById(`file-upload-${fileType}`).click();
        fileUploadMenu.style.display = 'none';
    });
});

fileInputs.forEach(input => {
    input.addEventListener('change', handleFileUpload);
});

document.addEventListener('click', () => {
    fileUploadMenu.style.display = 'none';
});

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

document.getElementById('add-chat-button').addEventListener('click', async function() {
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




async function recivirChat(params) {
    addMessage("Hola", false)
}