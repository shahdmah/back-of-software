// وظيفة لتصفية البيانات حسب اسم الطالب
function filterStudents() {
    const filter = document.getElementById('studentFilter').value.toLowerCase();
    const rows = document.querySelectorAll('tbody tr');

    rows.forEach(row => {
        const studentName = row.cells[0].textContent.toLowerCase();
        if (studentName.includes(filter)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// وظيفة لإعادة تعيين الفلتر
function resetFilter() {
    document.getElementById('studentFilter').value = '';
    const rows = document.querySelectorAll('tbody tr');
    rows.forEach(row => row.style.display = '');
}
