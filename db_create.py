from jsabrandeis import db
from model import User
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
db.create_all()

admin = User(email=os.environ.get('ADMIN_EMAIL'), password=generate_password_hash(os.environ.get('ADMIN_PASSWORD')))

db.session.add(admin)
db.session.commit()