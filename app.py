from flask import Flask, render_template, redirect, url_for, request # เพิ่ม redirect, url_for, request
from models import db, User # เพิ่ม User
from forms import RegisterForm, LoginForm # ดึงฟอร์มมาใช้
from werkzeug.security import generate_password_hash, check_password_hash # ระบบเข้ารหัสผ่าน
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///miku_sekai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

# เพิ่ม Route สมัครสมาชิก
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # เข้ารหัสผ่านก่อนบันทึกเพื่อความปลอดภัย
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login')) # สมัครเสร็จเด้งไปหน้าล็อกอิน
    return render_template('register.html', form=form)

# เพิ่ม Route เข้าสู่ระบบ
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            return redirect(url_for('index')) # ล็อกอินสำเร็จเด้งไปหน้าแรก (เดี๋ยวค่อยทำระบบ Session ทีหลัง)
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)