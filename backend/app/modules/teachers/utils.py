# from utils import send_welcome_email
# from werkzeug.security import generate_password_hash
# from flask import current_app

# def generate_password():
#     """Generate a random password for a new teacher."""
#     import random, string
#     return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

# def notify_teacher(mail, recipient_email, subdomain):
#     """Send welcome email to teacher using your existing utility."""
#     send_welcome_email(mail, recipient_email, subdomain)



# backend/app/modules/teachers/utils.py
from werkzeug.security import generate_password_hash
from flask import current_app
from flask_mail import Message
import random, string
# from app.utils import get_tenant_engine
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from utils import get_tenant_engine


def generate_password(length=10):
    """Generate a random password for a new teacher."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def send_teacher_email(mail, teacher_email, password, subdomain):
    """Send welcome email with login details to teacher."""
    msg = Message(
        "Welcome to EvolTechs School System",
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[teacher_email]
    )
    msg.html = f"""
    <h3>Welcome!</h3>
    <p>Your account has been created.</p>
    <p>Email: <b>{teacher_email}</b></p>
    <p>Password: <b>{password}</b></p>
    <p>Login at: <a href='https://{subdomain}.evoltechs.top/login'>here</a></p>
    <p>Please change your password after first login.</p>
    """
    mail.send(msg)
