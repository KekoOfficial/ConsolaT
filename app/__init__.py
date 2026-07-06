from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO
from app.models.database import db, User
import config

socketio = SocketIO()
login_manager = LoginManager()

def create_app():
    flask_app = Flask(__name__)
    flask_app.config["SECRET_KEY"] = config.SECRET_KEY
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///enterprise.db"
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Init extensions
    db.init_app(flask_app)
    socketio.init_app(flask_app, cors_allowed_origins="*")
    login_manager.init_app(flask_app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.routes.main import main as main_blueprint
    from app.routes.auth import auth as auth_blueprint
    flask_app.register_blueprint(main_blueprint)
    flask_app.register_blueprint(auth_blueprint)

    # Error handlers
    from flask import render_template
    @flask_app.errorhandler(404)
    def page_not_found(e):
        return render_template("error.html", code=404, title="Página No Encontrada", message="Lo sentimos, la ruta solicitada no existe o ha sido movida."), 404

    @flask_app.errorhandler(500)
    def internal_server_error(e):
        return render_template("error.html", code=500, title="Error Interno del Servidor", message="Se ha producido un error inesperado. Nuestro equipo técnico ha sido notificado."), 500

    # Import sockets
    with flask_app.app_context():
        import app.sockets

    # Create DB tables
    with flask_app.app_context():
        db.create_all()
        # Crear admin por defecto si no existe
        if not User.query.filter_by(username=config.ADMIN_USER).first():
            from app.services.auth import AuthService
            admin = User(
                username=config.ADMIN_USER,
                password_hash=AuthService.hash_password(config.ADMIN_PASS)
            )
            db.session.add(admin)
            db.session.commit()

        # Log de inicio empresarial
        from app.models.database import AuditLog
        db.session.add(AuditLog(event="Sistema Empresarial iniciado y auditado."))
        db.session.commit()

    return flask_app
