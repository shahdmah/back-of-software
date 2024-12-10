from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

# إعداد الاتصال بقاعدة البيانات
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'shwk@Rz1!',
    'database': 'clinic_app'
}
db = mysql.connector.connect(**db_config)
cursor = db.cursor()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        try:
            username = request.form['name']
            email = request.form['email']
            password = request.form['password']

            # حفظ البيانات في قاعدة البيانات
            cursor.execute("INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, 'student')", (username, email, password))
            db.commit()

            return jsonify({'success': True, 'message': 'User registered successfully'})
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return jsonify({'success': False, 'message': f"Database error: {str(err)}"})
        except Exception as e:
            print(f"Error during sign up: {e}")
            return jsonify({'success': False, 'message': f"An error occurred: {str(e)}"})
    return render_template('sign-up.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']

            # التحقق من بيانات المستخدم
            cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
            user = cursor.fetchone()

            if user:
                return jsonify({'success': True, 'message': f'Welcome, {user[1]}!', 'username': user[1]})
            else:
                return jsonify({'success': False, 'message': 'Invalid email or password'})
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return jsonify({'success': False, 'message': f"Database error: {str(err)}"})
        except Exception as e:
            print(f"Error during login: {e}")
            return jsonify({'success': False, 'message': f"An error occurred: {str(e)}"})
    return render_template('login-after-sign-up.html')


@app.route('/appointments', methods=['POST', 'GET'])
def appointments():
    if request.method == 'POST':
        student_id = request.form.get('student_id')  # التأكد من وجود student_id
        doctor_name = request.form['doctor']
        day = request.form['day']
        time = request.form['time']

        if not student_id:
            return jsonify({'success': False, 'message': 'Student ID is missing'})
        
        try:
            cursor.execute("""
                INSERT INTO appointments (student_id, doctor_name, day, time)
                VALUES (%s, %s, %s, %s)
            """, (student_id, doctor_name, day, time))
            db.commit()
            return jsonify({'success': True, 'message': 'Appointment booked successfully'})
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return jsonify({'success': False, 'message': f"Database error: {err}"})
    else:
        doctors = [
            {'name': 'Dr. Ahmed', 'specialization': 'Dermatology', 'available_days': 'Saturday, Monday'},
            {'name': 'Dr. Sara', 'specialization': 'Cardiology', 'available_days': 'Tuesday, Thursday'},
            {'name': 'Dr. Samir', 'specialization': 'Orthopedics', 'available_days': 'Sunday, Wednesday'}
        ]
        student_id = 1  # مثال: قيمة ثابتة أو استخرجيها من جلسة المستخدم
        return render_template('appointments.html', doctors=doctors, student_id=student_id)
@app.route('/logout')
def logout():
    # إزالة الجلسة (إذا كنتِ تستخدمين جلسات)
    # session.clear()
    # إعادة توجيه المستخدم إلى صفحة تسجيل الخروج
    return render_template('logout.html')

# كود Flask للتعامل مع المواعيد من جانب الدكتور
@app.route('/doctor_appointments', methods=['GET', 'POST'])
def doctor_appointments():
    if request.method == 'POST':
        appointment_id = request.form['appointment_id']
        action = request.form['action']  # القبول أو الرفض

        # تحديث حالة الموعد في قاعدة البيانات بناءً على الإجراء
        if action == 'approve':
            cursor.execute("UPDATE appointments SET status = 'approved' WHERE id = %s", (appointment_id,))
        elif action == 'reject':
            cursor.execute("UPDATE appointments SET status = 'rejected' WHERE id = %s", (appointment_id,))
        db.commit()

    # جلب جميع المواعيد مع حالة "approved" أو "rejected"
    cursor.execute("""
        SELECT a.id, u.username, a.doctor_name, a.day, a.time, a.status
        FROM appointments a
        JOIN users u ON a.student_id = u.id
        WHERE a.status IN ('approved', 'rejected')
    """)
    appointments = cursor.fetchall()

    return render_template('doctor_appointments.html', appointments=appointments)


@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    doctor = request.form['doctor']  # الحصول على اسم الدكتور
    day = request.form['day']        # الحصول على اليوم
    time = request.form['time']      # الحصول على الوقت
    
    # تحقق من البيانات المستلمة (يمكنك الطباعة هنا لمراجعة القيم)
    print(f"Booking appointment for {doctor} on {day} at {time}")
    
    # تنفيذ إضافة البيانات إلى قاعدة البيانات
    cursor.execute("INSERT INTO appointments (doctor_name, day, time, status) VALUES (%s, %s, %s, %s)", (doctor, day, time, 'pending'))
    db.commit()
    
    # إعادة التوجيه إلى صفحة مواعيد الدكتور
    return redirect(url_for('doctor_appointments'))

@app.route('/approved_students', methods=['GET'])
def approved_students():
    # جلب الطلاب الذين تم قبول حجوزاتهم
    cursor.execute("""
        SELECT u.username, a.doctor_name, a.day, a.time
        FROM appointments a
        JOIN users u ON a.student_id = u.id
        WHERE a.status = 'approved'
    """)
    approved_appointments = cursor.fetchall()

    # إرسال البيانات إلى صفحة HTML
    return render_template('approved_students.html', appointments=approved_appointments)


@app.route('/rejected_students')
def rejected_students():
    # جلب الطلاب المرفوضين
    cursor.execute("""
        SELECT u.username, a.doctor_name, a.day, a.time
        FROM appointments a
        JOIN users u ON a.student_id = u.id
        WHERE a.status = 'rejected'
    """)
    rejected_students = cursor.fetchall()

    return render_template('rejected_students.html', rejected_students=rejected_students)



@app.route('/doctor_dashboard', methods=['POST', 'GET'])
def doctor_dashboard():
    if request.method == 'POST':
        appointment_id = request.form['appointment_id']
        action = request.form['action']  # approved أو rejected
        cursor.execute("UPDATE appointments SET status = %s WHERE id = %s", (action, appointment_id))
        db.commit()
        return jsonify({'success': True, 'message': 'Appointment updated successfully'})
    cursor.execute("SELECT * FROM appointments WHERE status = 'pending'")
    appointments = cursor.fetchall()
    return render_template('doctor.html', appointments=appointments)

@app.route('/update_profile', methods=['POST', 'GET'])
def update_profile():
    if request.method == 'POST':
        user_id = request.form['user_id']
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        try:
            cursor.execute("""
                UPDATE users 
                SET username = %s, email = %s, password = %s 
                WHERE id = %s
            """, (username, email, password, user_id))
            db.commit()
            
            return jsonify({'success': True, 'message': 'Profile updated successfully'})
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return jsonify({'success': False, 'message': f"Database error: {err}"})
    return render_template('update-doctor.html', doctor=current_user)


if __name__ == '__main__':
    app.run(debug=True)
    