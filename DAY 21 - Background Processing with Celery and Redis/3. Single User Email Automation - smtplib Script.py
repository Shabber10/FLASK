"""
=============================================================================
CLASS NOTES PRACTICAL PROJECT: EMAIL SENDING AUTOMATION USING PYTHON SMTPLIB
=============================================================================
Project Goal: Email sending for a Single User using Gmail SMTP_SSL.
Features:
- Connects securely to smtp.gmail.com over port 465 (SSL).
- Builds formatted email with Subject, From, To, and Body.
- Includes automated scheduling example with the 'schedule' library.
=============================================================================
"""
import smtplib
from email.message import EmailMessage
import os

# Configuration details (Set your Gmail and 16-character App Password)
SENDER_EMAIL = os.environ.get('GMAIL_USER', 'janpadushaik@gmail.com')
RECEIVER_EMAIL = os.environ.get('GMAIL_RECEIVER', 'janibashadshaik@gmail.com')
APP_PASSWORD = os.environ.get('GMAIL_APP_PASS', 'ktsi quvu syfy jylh')

def send_single_email(sender=SENDER_EMAIL, receiver=RECEIVER_EMAIL, app_pass=APP_PASSWORD, subject='Meeting Reminder', body=None):
    if body is None:
        body = """Hi Guys,

Just reminding you about our meeting tomorrow at 10 AM.

Regards,
Jani"""

    # Create Email Message object
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    msg.set_content(body)

    print(f"[*] Connecting to Gmail SMTP_SSL (smtp.gmail.com:465)...")
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender, app_pass)
            smtp.send_message(msg)
            print("[+] Email sent successfully!!")
            return {"status": "success", "message": "Email sent successfully!"}
    except Exception as e:
        print(f"[-] Error sending email: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == '__main__':
    print("=" * 60)
    print("Class Notes Email Automation Project (smtplib + SSL)")
    print("=" * 60)
    print(f"Sender:   {SENDER_EMAIL}")
    print(f"Receiver: {RECEIVER_EMAIL}")
    print("To run live: provide valid Gmail & App Password credentials.")
    print("=" * 60)
