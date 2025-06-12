import smtplib
from email.message import EmailMessage
from app.core.config import EMAIL_USER, EMAIL_PASSWORD

def send_reset_email(to_email: str, token: str):
    msg = EmailMessage()
    msg["Subject"] = "Your Password Reset Token"
    msg["From"] = EMAIL_USER
    msg["To"] = to_email

    msg.set_content(f"""
Hello,

You requested to reset your password.

Here is your secure token:
{token}

Use this token in the /auth/reset-password endpoint to set your new password.

Thank you.
""")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print(f"Password reset email sent to {to_email}")
    except Exception as e:
        print(f" Failed to send email to {to_email}: {e}")
