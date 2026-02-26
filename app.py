from flask import Flask, render_template, redirect, url_for, request, abort
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

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

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

@app.route('/songs/add', methods=['GET', 'POST'])
@login_required
def add_song():
    form = AddSongForm()
    if form.validate_on_submit():
        new_song = Song(
            title=form.title.data,
            producer=form.producer.data,
            youtube_url=form.youtube_url.data,
            user_id=current_user.id
        )
        db.session.add(new_song)
        db.session.commit()
        return redirect(url_for('songs'))
    return render_template('add_song.html', form=form)

@app.route('/board', methods=['GET', 'POST'])
def board():
    form = FanboardForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        new_post = Fanboard(message=form.message.data, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('board'))
    posts = Fanboard.query.order_by(Fanboard.date_posted.desc()).all()
    return render_template('board.html', form=form, posts=posts)

@app.route('/profile')
@login_required
def profile():
    user_posts = Fanboard.query.filter_by(user_id=current_user.id).order_by(Fanboard.date_posted.desc()).all()
    return render_template('profile.html', posts=user_posts)

@app.route('/song/<int:song_id>')
def song_detail(song_id):
    song = Song.query.get_or_404(song_id)
    embed_url = None
    if song.youtube_url:
        if 'watch?v=' in song.youtube_url:
            video_id = song.youtube_url.split('watch?v=')[-1].split('&')[0]
            embed_url = f"https://www.youtube.com/embed/{video_id}"
        elif 'youtu.be/' in song.youtube_url:
            video_id = song.youtube_url.split('youtu.be/')[-1].split('?')[0]
            embed_url = f"https://www.youtube.com/embed/{video_id}"
    return render_template('song_detail.html', song=song, embed_url=embed_url)

@app.route('/songs/edit/<int:song_id>', methods=['GET', 'POST'])
@login_required
def edit_song(song_id):
    song = Song.query.get_or_404(song_id)
    if current_user.id != song.user_id and current_user.role != 'admin':
        return abort(403)
    form = AddSongForm(obj=song)
    if request.method == 'GET':
        form.title.data = song.title
        form.producer.data = song.producer
        form.youtube_url.data = song.youtube_url
    if form.validate_on_submit():
        song.title = form.title.data
        song.producer = form.producer.data
        song.youtube_url = form.youtube_url.data
        db.session.commit()
        return redirect(url_for('songs'))
    return render_template('edit_song.html', form=form, song=song)

@app.route('/songs/delete/<int:song_id>', methods=['POST'])
@login_required
def delete_song(song_id):
    song = Song.query.get_or_404(song_id)
    if current_user.id != song.user_id and current_user.role != 'admin':
        return abort(403)
    db.session.delete(song)
    db.session.commit()
    return redirect(url_for('songs'))

if __name__ == '__main__':
    app.run(debug=True)