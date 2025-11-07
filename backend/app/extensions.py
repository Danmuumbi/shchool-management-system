# from flask_sqlalchemy import SQLAlchemy
# from flask_jwt_extended import JWTManager
    

# db = SQLAlchemy()
# jwt = JWTManager()


# backend/app/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail  # <-- ADD THIS
from flask_cors import CORS

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()  # now Mail is defined

cors = CORS()

