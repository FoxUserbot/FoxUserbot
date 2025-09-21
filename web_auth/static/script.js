let __lastError = null;
let __lastErrorStep = null;

function checkStep(phone, currentStep) {
    fetch('/check_step')
        .then(response => response.json())
        .then(data => {
            if (data.step === 'password' && currentStep !== 'password') {
                window.location.href = '?step=password&phone=' + encodeURIComponent(phone || '');
                return;
            }
            if (data.step === 'code' && currentStep !== 'code') {
                window.location.href = '?step=code&phone=' + encodeURIComponent(phone || '');
                return;
            }
            if (data.step === 'success' && currentStep !== 'success') {
                window.location.href = '?step=success';
                return;
            }

            const errorBox = document.getElementById('errorBox');
            const inputId = currentStep === 'password' ? 'password' : (currentStep === 'code' ? 'code' : null);
            const inputEl = inputId ? document.getElementById(inputId) : null;

            if (errorBox) {
                if (data.error) {
                    const newErrorCame = (data.error !== __lastError) || (currentStep !== __lastErrorStep);
                    errorBox.textContent = data.error;
                    errorBox.classList.remove('d-none');

                    if (newErrorCame) {
                        errorBox.classList.remove('shake');
                        void errorBox.offsetWidth;
                        errorBox.classList.add('shake');
                        if (inputEl) {
                            inputEl.classList.add('is-invalid');
                            if (document.activeElement !== inputEl) {
                                inputEl.focus();
                            }
                            inputEl.classList.remove('shake');
                            void inputEl.offsetWidth;
                            inputEl.classList.add('shake');
                        }
                    } else {
                        if (inputEl && document.activeElement === inputEl) {
                        } else if (inputEl) {
                            inputEl.classList.add('is-invalid');
                        }
                    }

                    __lastError = data.error;
                    __lastErrorStep = currentStep;
                } else {
                    errorBox.classList.add('d-none');
                    if (inputEl) {
                        inputEl.classList.remove('is-invalid');
                    }
                    __lastError = null;
                    __lastErrorStep = null;
                }
            }
        })
        .catch(error => console.error('Error checking step:', error));
    setTimeout(() => checkStep(phone, currentStep), 1200);
}
