from flask import Flask, render_template  # <--- จุดที่ต้องแก้ครับ
from models import db
from dotenv import load_dotenv
import os

# โหลดค่าจากไฟล์ .env
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///miku_sekai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# เชื่อมต่อฐานข้อมูล
db.init_app(app)

with app.app_context():
    db.create_all()

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html') # <--- บรรทัดนี้จะทำงานได้แล้วครับ

if __name__ == '__main__':
    app.run(debug=True)