school_management_system/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── extensions.py
│   │   ├── models/
│   │   │   ├── central.py
│   │   │   └── tenant_base.py
│   │   ├── services/db_manager.py
│   │   ├── routes/
│   │   │   ├── auth_routes.py
│   │   │   └── tenant_routes.py
│   │   ├── middleware.py
│   │   └── main.py
│   ├── requirements.txt
│   └── .env.example
└── README.md




backend/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── tenant.py
│   │   ├── teacher.py          ✅ (new model for teachers)
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   ├── tenant_routes.py
│   │   ├── tenant_profile_routes.py
│   │   └── teacher_routes.py   ✅ (new teacher blueprint)
│   │
│   ├── modules/                ✅ (for modular expansion)
│   │   ├── __init__.py
│   │   ├── teachers/
│   │   │   ├── __init__.py
│   │   │   ├── controller.py   ✅ (teacher logic: CRUD, email sending, etc.)
│   │   │   ├── service.py      ✅ (handles DB operations and background tasks)
│   │   │   └── utils.py        ✅ (email sending helper, password generator)
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── email_helper.py     ✅ (shared email sender for all modules)
│   │
│   └── app.py
│
├── uploads/
│
├── requirements.txt
└── run.py
