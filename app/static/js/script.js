document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('feedbackForm');
    const message = document.getElementById('message');

    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            
            fetch('/', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                message.textContent = data.message;
                message.style.color = 'green';
                form.reset();
                setTimeout(() => {
                    message.textContent = '';
                    window.location.href = '/dashboard';  // Redirect to dashboard after submission
                }, 3000);
            })
            .catch(error => {
                console.error('Error:', error);
                message.textContent = 'An error occurred. Please try again.';
                message.style.color = 'red';
            });
        });
    }
});