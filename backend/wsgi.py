

# from app.app import create_app

# app = create_app()

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)



# backend/wsgi.py

from app.app import create_app  # ✅ correct import path

app = create_app()

if __name__ == "__main__":
    from app.config import Config
    app.run(host="0.0.0.0", port=Config.APP_PORT, debug=True)
