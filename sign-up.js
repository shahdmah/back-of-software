document.getElementById('signup-form').addEventListener('submit', function (event) {
    event.preventDefault(); // منع السلوك الافتراضي للنموذج

    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    // تحقق من تطابق كلمتي المرور
    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    // إنشاء بيانات النموذج (Form Data)
    const formData = new FormData(this);

    // إرسال البيانات إلى السيرفر
    fetch('/signup', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            window.location.href = '/login'; // التوجيه لصفحة تسجيل الدخول
        } else {
            alert('Registration failed. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
});
