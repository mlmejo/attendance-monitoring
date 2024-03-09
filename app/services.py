from flask_login import LoginManager
from flask_migrate import Migrate
from flask_qrcode import QRcode
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate(db=db)
qrcode = QRcode()

login_manager.login_view = 'auth.login'
