const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const fileUploadLabel = document.getElementById('file-upload-label');
const fileUploadMenu = document.getElementById('file-upload-menu');
const fileOptions = document.querySelectorAll('.file-option');
const fileInputs = document.querySelectorAll('.file-input');
const chatHistory = document.querySelector('.chat-history');

function addMessage(message, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function handleUserInput() {
    const message = userInput.value.trim();
    if (message) {
        addMessage(message, true);
        userInput.value = '';

        // Using a promise to delay the execution and handle async properly
        setTimeout(async () => {
            try {
                const response = await fetch("http://127.0.0.1:8000/users", {
                    method: "POST",
                    headers: {
                        Accept: 'application/json',
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ input: message }) // Wrap message in an object
                    
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const botResponse = await response.json(); // Assuming the server returns JSON
                addMessage(botResponse); // Adjust based on the response structure
            } catch (error) {
                console.error('There was a problem with the fetch operation:', error);
                addMessage('Sorry, there was an error processing your request.');
            }
        }, 1);
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

sendButton.addEventListener('click', handleUserInput);
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

chatHistory.addEventListener('click', (e) => {
    if (e.target.tagName === 'LI') {
        chatHistory.querySelectorAll('li').forEach(li => li.classList.remove('active'));
        e.target.classList.add('active');
        // Aquí se simularía la carga del chat seleccionado
        chatMessages.innerHTML = '';
        addMessage(`Has seleccionado: ${e.target.textContent}`, false);
    }
});
