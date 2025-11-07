

# backend/app/modules/teachers/service.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from utils import get_tenant_engine
from app.modules.teachers.utils import generate_password, send_teacher_email
from app.models.teacher import Teacher
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

def add_teacher(subdomain, mail, teacher_data):
    """
    Create teacher in tenant DB, hash password, send welcome email.
    teacher_data: dict with keys: first_name, last_name, email, phone, subjects
    """
    try:
        # 1️⃣ Generate password
        plain_password = generate_password()
        password_hash = generate_password_hash(plain_password)

        # 2️⃣ Get tenant DB engine
        engine = get_tenant_engine(subdomain)
        Session = sessionmaker(bind=engine)
        session = Session()

        # 3️⃣ Check if teacher already exists
        existing_teacher = session.query(Teacher).filter_by(email=teacher_data['email']).first()
        if existing_teacher:
            session.close()
            raise Exception("Teacher with this email already exists")

        # 4️⃣ Create teacher instance
        teacher = Teacher(
            first_name=teacher_data['first_name'],
            last_name=teacher_data['last_name'],
            email=teacher_data['email'],
            phone=teacher_data.get('phone'),
            subjects=teacher_data.get('subjects', []),
            password_hash=password_hash
        )

        # 5️⃣ Save to tenant DB
        session.add(teacher)
        session.commit()

        # 6️⃣ Send email (optional - you can comment this out for testing)
        try:
            send_teacher_email(mail, teacher.email, plain_password, subdomain)
        except Exception as email_error:
            print(f"⚠️ Email sending failed: {email_error}")
            # Don't fail the whole request if email fails

        teacher_dict = teacher.to_dict()
        session.close()
        
        return teacher_dict

    except IntegrityError as e:
        session.rollback()
        session.close()
        raise Exception("Teacher with this email already exists")
    except Exception as e:
        if 'session' in locals():
            session.rollback()
            session.close()
        raise e


# # backend/app/modules/teachers/service.py

# from app.modules.teachers.utils import generate_password, send_teacher_email
# from app.models.teacher import Teacher
# from sqlalchemy.orm import sessionmaker
# from werkzeug.security import generate_password_hash
# from sqlalchemy.exc import IntegrityError


# def add_teacher(engine, mail, teacher_data):
#     """
#     Create a teacher in the tenant DB, hash password, send welcome email.
#     teacher_data: dict with keys: first_name, last_name, email, phone, subjects
#     """
#     try:
#         # 1️⃣ Generate password
#         plain_password = generate_password()
#         password_hash = generate_password_hash(plain_password)

#         # 2️⃣ Start session using the provided engine
#         Session = sessionmaker(bind=engine)
#         session = Session()

#         # 3️⃣ Check if teacher already exists
#         existing_teacher = session.query(Teacher).filter_by(email=teacher_data['email']).first()
#         if existing_teacher:
#             session.close()
#             raise Exception("Teacher with this email already exists")

#         # 4️⃣ Create teacher record
#         teacher = Teacher(
#             first_name=teacher_data['first_name'],
#             last_name=teacher_data['last_name'],
#             email=teacher_data['email'],
#             phone=teacher_data.get('phone'),
#             subjects=teacher_data.get('subjects', []),
#             password_hash=password_hash
#         )

#         # 5️⃣ Save to DB
#         session.add(teacher)
#         session.commit()

#         # 6️⃣ Send welcome email (optional)
#         try:
#             send_teacher_email(mail, teacher.email, plain_password)
#         except Exception as email_error:
#             print(f"⚠️ Email sending failed: {email_error}")

#         teacher_dict = teacher.to_dict()
#         session.close()

#         return teacher_dict

#     except IntegrityError:
#         session.rollback()
#         session.close()
#         raise Exception("Teacher with this email already exists")
#     except Exception as e:
#         if 'session' in locals():
#             session.rollback()
#             session.close()
#         raise e
