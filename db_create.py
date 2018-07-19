from jsabrandeis import db
from model import User
import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
db.create_all()

admin = User(email=os.environ.get('ADMIN_EMAIL'), password=os.environ.get('ADMIN_PASSWORD'))

db.session.add(admin)
db.session.commit()