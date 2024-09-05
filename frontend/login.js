document.getElementById('loginForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch(`http://127.0.0.1:8000/users/login/?username=${username}&password=${password}`, {  // Reemplaza con la URL de tu API
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        console.log(response)

        if (response.ok) {
            const data = await response.json();
            console.log(data)
            // Maneja el éxito aquí, por ejemplo, redirigir al usuario a otra página
            alert('Login successful!');
            var userId = data.id
            localStorage.setItem("userId", userId)
            window.location.href = "chat_ui.html"
        } else {
            const errorData = await response.json();
            document.getElementById('error-message').innerText = errorData.message || 'Login failed';
        }
    } catch (error) {
        document.getElementById('error-message').innerText = 'Error de red: ' + error.message;
    }
});
