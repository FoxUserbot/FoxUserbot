function checkStep(phone) {
    fetch('/check_step')
        .then(response => response.json())
        .then(data => {
            if (data.step === 'password') {
                window.location.href = '?step=password&phone=' + phone;
            }
        })
        .catch(error => console.error('Error checking step:', error));
    setTimeout(() => checkStep(phone), 100);
}
