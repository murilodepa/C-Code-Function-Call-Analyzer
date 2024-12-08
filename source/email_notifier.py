import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Developer's email
DEVELOPER_EMAIL = "lukaoborgesrondon@gmail.com"

def send_email(subject, body):
    """
    Sends an email to the developer with the given subject and body.
    """
    # SMTP server configuration
    smtp_server = "smtp.gmail.com"  # Change this if using a different provider
    smtp_port = 587
    sender_email = "your_email@gmail.com"  # Replace with your email
    sender_password = "your_password"  # Replace with your email password or app password

    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = DEVELOPER_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, DEVELOPER_EMAIL, msg.as_string())

        print(f"Email sent to {DEVELOPER_EMAIL} with subject: '{subject}'")
    except Exception as e:
        print(f"Failed to send email: {e}")
