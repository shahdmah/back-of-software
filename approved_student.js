// رسالة ترحيب عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', () => {
    const message = document.createElement('div');
    message.classList.add('success-message');
    message.textContent = 'Here are the approved appointments!';
    document.body.prepend(message);

    // إخفاء الرسالة بعد 3 ثوانٍ
    setTimeout(() => {
        message.remove();
    }, 3000);
});
