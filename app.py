from flask import Flask, render_template, redirect, url_for, request
from models import db, User, Song, Fanboard
from forms import RegisterForm, LoginForm, AddSongForm, FanboardForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user # นำเข้าเครื่องมือ Login
from dotenv import load_dotenv
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
            login_user(user) # สั่งให้ระบบจำว่าล็อกอินแล้ว
            return redirect(url_for('index'))
    return render_template('login.html', form=form)

# เพิ่ม Route ออกจากระบบ
@app.route('/logout')
@login_required
def logout():
    logout_user() # สั่งล้างข้อมูลล็อกอิน
    return redirect(url_for('index'))

# หน้าคลังเพลง (แสดงเพลงทั้งหมด)
@app.route('/songs')
def songs():
    all_songs = Song.query.order_by(Song.date_added.desc()).all()
    return render_template('songs.html', songs=all_songs)

# หน้าเพิ่มเพลง (ต้องล็อกอินก่อนถึงจะเข้าได้)
@app.route('/songs/add', methods=['GET', 'POST'])
@login_required
def add_song():
    form = AddSongForm()
    if form.validate_on_submit():
        new_song = Song(
            title=form.title.data,
            producer=form.producer.data,
            youtube_url=form.youtube_url.data
        )
        db.session.add(new_song)
        db.session.commit()
        return redirect(url_for('songs'))
    return render_template('add_song.html', form=form)

# หน้าเว็บบอร์ด
@app.route('/board', methods=['GET', 'POST'])
def board():
    form = FanboardForm()
    # ถ้ามีการกดปุ่มโพสต์ และผู้ใช้ล็อกอินอยู่
    if form.validate_on_submit() and current_user.is_authenticated:
        new_post = Fanboard(message=form.message.data, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('board')) # โพสต์เสร็จให้รีเฟรชหน้าเดิม

    # ดึงข้อความทั้งหมดจากฐานข้อมูล เรียงจากใหม่ไปเก่า
    posts = Fanboard.query.order_by(Fanboard.date_posted.desc()).all()
    return render_template('board.html', form=form, posts=posts)

# หน้าโปรไฟล์ส่วนตัว
@app.route('/profile')
@login_required
def profile():
    # ดึงเฉพาะโพสต์เว็บบอร์ดที่ User คนนี้เป็นคนเขียน
    user_posts = Fanboard.query.filter_by(user_id=current_user.id).order_by(Fanboard.date_posted.desc()).all()
    return render_template('profile.html', posts=user_posts)

# หน้ารายละเอียดเพลง (รับค่า id ของเพลงมาด้วย)
@app.route('/song/<int:song_id>')
def song_detail(song_id):
    song = Song.query.get_or_404(song_id) # หาเพลงจาก ID ถ้าไม่เจอจะขึ้น 404
    
    # แปลงลิงก์ YouTube ปกติ ให้กลายเป็นลิงก์แบบฝัง (Embed) เพื่อให้เล่นวิดีโอบนเว็บเราได้เลย
    embed_url = None
    if song.youtube_url:
        if 'watch?v=' in song.youtube_url:
            video_id = song.youtube_url.split('watch?v=')[-1].split('&')[0]
            embed_url = f"https://www.youtube.com/embed/{video_id}"
        elif 'youtu.be/' in song.youtube_url:
            video_id = song.youtube_url.split('youtu.be/')[-1].split('?')[0]
            embed_url = f"https://www.youtube.com/embed/{video_id}"

    return render_template('song_detail.html', song=song, embed_url=embed_url)

if __name__ == '__main__':
    app.run(debug=True)