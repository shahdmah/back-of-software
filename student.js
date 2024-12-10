document.getElementById("student-form").addEventListener("submit", function (e) {
    e.preventDefault();

    
    const doctor = document.getElementById("doctor").value;
    const time = document.getElementById("time").value;

    
    alert(`Your appointment with ${doctor} at ${time} has been confirmed.`);

    
    console.log(`Appointment saved: Doctor - ${doctor}, Time - ${time}`);


    window.location.href = "index.html"; 
});
