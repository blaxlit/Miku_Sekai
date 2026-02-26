from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin  # เพิ่มบรรทัดนี้
from datetime import datetime

db = SQLAlchemy()

# ใส่ UserMixin เข้าไปในวงเล็บด้วย
class User(UserMixin, db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user') # ⭐️ เพิ่มบรรทัดนี้: กำหนดค่าเริ่มต้นเป็น 'user' ธรรมดา
    songs = db.relationship('Song', backref='uploader', lazy=True)
    posts = db.relationship('Fanboard', backref='author', lazy=True)

# (ส่วนคลาส Song และ Fanboard ปล่อยไว้เหมือนเดิมได้เลยครับ)

# 2. ตารางคลังเพลง
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    producer = db.Column(db.String(100), nullable=False)
    youtube_url = db.Column(db.String(200))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    # ⭐️ เพิ่มบรรทัดนี้: เก็บ ID ของคนที่เพิ่มเพลง
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# 3. ตารางเว็บบอร์ด
class Fanboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)