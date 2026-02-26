from flask import Flask, render_template, redirect, url_for, request, abort # ⭐️ เพิ่ม abort ตรงนี้
from models import db, User, Song, Fanboard
from forms import RegisterForm, LoginForm, AddSongForm, FanboardForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from dotenv import load_dotenv
from acl import roles_required
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///miku_sekai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --- ตั้งค่าระบบ Login ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/songs')
def songs():
    all_songs = Song.query.order_by(Song.date_added.desc()).all()
    return render_template('songs.html', songs=all_songs)

# ⭐️ อัปเดต: บันทึก user_id ของคนเพิ่มเพลง
@app.route('/songs/add', methods=['GET', 'POST'])
@login_required
def add_song():
    form = AddSongForm()
    if form.validate_on_submit():
        new_song = Song(
            title=form.title.data,
            producer=form.producer.data,
            youtube_url=form.youtube_url.data,
            user_id=current_user.id  # ⭐️ สั่งให้บันทึก ID ของคนเพิ่มเพลง
        )
        db.session.add(new_song)
        db.session.commit()