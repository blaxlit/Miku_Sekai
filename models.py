from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# 1. ตารางผู้ใช้งาน
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# 2. ตารางคลังเพลง
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    producer = db.Column(db.String(100), nullable=False)
    youtube_url = db.Column(db.String(200), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

# 3. ตารางเว็บบอร์ด
class Fanboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)