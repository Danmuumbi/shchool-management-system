from flask import Flask, g
from app.config import Config
from app.extensions import db, jwt
from app.routes.auth_routes import auth_bp
from app.routes.tenant_routes import tenant_bp
from app.middleware import tenant_resolver
from app.models.central import Tenant

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(tenant_bp)

    # run tenant resolver before requests to tenant routes
    @app.before_request
    def _resolve_tenant():
        # skip resolving for central admin endpoints if needed
        # We'll call tenant_resolver for routes where subdomain matters
        return tenant_resolver()

    @app.route("/")
    def index():
        return "EvolTechs backend running."

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
