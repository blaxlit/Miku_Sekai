from app import app
from models import db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # สร้างตารางในฐานข้อมูลใหม่ (เพราะเราเพิ่งลบไฟล์ทิ้งไป)
    db.create_all()
    
    # เช็คว่ามีแอคเคาท์ admin หรือยัง
    admin = User.query.filter_by(username='admin').first()
    
    if not admin:
        hashed_password = generate_password_hash('admin123')
        # สังเกตว่าเรากำหนด role='admin' ให้เลย
        new_admin = User(username='admin', password=hashed_password, role='admin') 
        db.session.add(new_admin)
        db.session.commit()
        print("✅ สร้างบัญชี Admin สำเร็จ! (Username: admin / Password: admin123)")
    else:
        print("⚠️ มีบัญชี Admin อยู่ในระบบแล้ว")