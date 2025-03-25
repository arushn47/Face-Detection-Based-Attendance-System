import smtplib
import os
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_attendance_email(student_name, status, date):
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    if not sender_email or not sender_password:
        return "Email credentials not set."

    # Load parent emails from users.csv
    parent_emails = {}
    with open("data/users.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            parent_emails[row["username"]] = row.get("email", "")

    if student_name not in parent_emails or not parent_emails[student_name]:
        return f"No email found for {student_name}"

    parent_email = parent_emails[student_name]

    subject = f"Attendance Update for {date}"
    body = f"Dear Parent,\n\nYour ward {student_name} is marked as {status} today ({date}).\n\nRegards,\nSchool Administration"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = parent_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, parent_email, msg.as_string())
        server.quit()
        return f"Email sent to {parent_email}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"
