// إذا كنت ترغب في إضافة تحقق من صحة البيانات قبل إرسال النموذج:
document.querySelector('form').addEventListener('submit', function(event) {
    const password = document.getElementById('password').value;
    if (password.length < 6) {
        alert("Password must be at least 6 characters long");
        event.preventDefault(); // منع إرسال النموذج حتى يتم التحقق من كلمة المرور
    }
});
