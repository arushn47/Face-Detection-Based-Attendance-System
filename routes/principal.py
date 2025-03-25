from flask import Blueprint, render_template, request, redirect, url_for, session
import os
import csv
import random
import string

principal_bp = Blueprint('principal', __name__, template_folder='../templates/principal')
USER_CSV = os.path.join(os.getcwd(), 'data', 'users.csv')
ATTENDANCE_DIR = os.path.join(os.getcwd(), 'data', 'attendance')

def ensure_users_csv():
    os.makedirs(os.path.join(os.getcwd(), 'data'), exist_ok=True)
    if not os.path.exists(USER_CSV):
        with open(USER_CSV, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['unique_code', 'username', 'password', 'role', 'assigned_class'])

def generate_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_unique_code(role):
    prefix = "PR-" if role == "principal" else "T-"
    last_code = 1000  

    if os.path.exists(USER_CSV):
        with open(USER_CSV, 'r') as file:
            reader = list(csv.reader(file))[1:]  
            codes = [int(row[0].split('-')[1]) for row in reader if row[0].startswith(prefix)]
            if codes:
                last_code = max(codes) + 1

    return f"{prefix}{last_code}"

@principal_bp.route('/dashboard')
def dashboard():
    if 'username' not in session or session.get('role') != 'principal':
        return redirect(url_for('auth.login'))
    available_classes = [d for d in os.listdir(ATTENDANCE_DIR) if os.path.isdir(os.path.join(ATTENDANCE_DIR, d))]
    return render_template('principal/dashboard.html', available_classes=available_classes)

@principal_bp.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    if 'username' not in session or session.get('role') != 'principal':
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        if 'add_user' in request.form:
            role = request.form['role']
            unique_code = generate_unique_code(role)
            username = request.form['username']
            password = generate_password()
            assigned_classes = request.form.getlist('assigned_class')
            assigned_class = ";".join(assigned_classes) if role == "teacher" else ""
            
            with open(USER_CSV, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([unique_code, username, password, role, assigned_class])  

        elif 'remove_user' in request.form:
            user_code = request.form['user_code']
            with open(USER_CSV, 'r') as file:
                users = [row for row in csv.reader(file)]
            users = [users[0]] + [row for row in users[1:] if row[0] != user_code]
            with open(USER_CSV, 'w', newline='') as file:
                csv.writer(file).writerows(users)
            if len(users) == 1:
                os.remove(USER_CSV)
                ensure_users_csv()
            return redirect(url_for('principal.manage_users'))
    
    users = []
    if os.path.exists(USER_CSV):
        with open(USER_CSV, 'r') as file:
            users = list(csv.reader(file))[1:]
    
    available_classes = [d for d in os.listdir(ATTENDANCE_DIR) if os.path.isdir(os.path.join(ATTENDANCE_DIR, d))]
    return render_template('principal/manage_users.html', users=users, available_classes=available_classes)

@principal_bp.route('/reset_user_codes', methods=['POST'])
def reset_user_codes():
    if 'username' not in session or session.get('role') != 'principal':
        return redirect(url_for('auth.login'))
    ensure_users_csv()
    return redirect(url_for('principal.manage_users'))

@principal_bp.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if 'username' not in session or session.get('role') != 'principal':
        return redirect(url_for('auth.login'))
    
    selected_class = request.args.get('class_name')
    date = request.args.get('date')
    attendance_records = []
    
    if os.path.exists(ATTENDANCE_DIR):
        classes = [d for d in os.listdir(ATTENDANCE_DIR) if os.path.isdir(os.path.join(ATTENDANCE_DIR, d))]
        if selected_class and date:
            file_path = os.path.join(ATTENDANCE_DIR, selected_class, f"{date}.csv")
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    reader = csv.reader(file)
                    attendance_records = [
                        {"student_name": row[0], "reg_no": row[1], "status": row[2], "time": row[3]}
                        for row in list(reader)[1:]
                    ]
    else:
        classes = []
    
    if request.method == 'POST' and selected_class and date:
        updated_attendance = {k: v for k, v in request.form.items() if k != 'csrf_token'}
        file_path = os.path.join(ATTENDANCE_DIR, selected_class, f"{date}.csv")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Student Name", "Reg No", "Status", "Time"])
            for row in attendance_records:
                status = updated_attendance.get(row['student_name'], row['status'])
                writer.writerow([row['student_name'], row['reg_no'], status, row['time']])
        return redirect(url_for('principal.attendance', class_name=selected_class, date=date))
    
    return render_template('principal/attendance.html', classes=classes, selected_class=selected_class, date=date, attendance_records=attendance_records)