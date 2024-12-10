// هنا يتم إضافة وظيفة القبول والرفض مباشرة من خلال الضغط على الأزرار
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const appointmentId = this.querySelector('input[name="appointment_id"]').value;
        const action = this.querySelector('button[type="submit"]').value;

        fetch(`/doctor_appointments`, {
            method: 'POST',
            body: new URLSearchParams({
                'appointment_id': appointmentId,
                'action': action
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(`Appointment ${action} successfully`);
                window.location.reload(); // إعادة تحميل الصفحة لعرض التحديث
            } else {
                alert("An error occurred");
            }
        })
        .catch(err => {
            console.error('Error:', err);
            alert("An error occurred");
        });
    });
});
