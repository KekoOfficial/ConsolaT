import sys
import os

# Añadir el directorio raíz al path para poder importar la app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models.database import db, User
from app.services.auth import AuthService

def create_admins(count=100):
    app = create_app()
    with app.app_context():
        print(f"Creating {count} admin users...")
        for i in range(1, count + 1):
            username = f"admin{i:03d}"
            password = f"pass{i:03d}"

            if not User.query.filter_by(username=username).first():
                user = User(
                    username=username,
                    password_hash=AuthService.hash_password(password),
                    role="admin"
                )
                db.session.add(user)
                if i % 10 == 0:
                    db.session.commit()
                    print(f"Created {i} admins...")

        db.session.commit()
        print("Done! All admins created.")

if __name__ == "__main__":
    create_admins()
