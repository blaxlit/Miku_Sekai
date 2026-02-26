from functools import wraps
from flask import abort
from flask_login import current_user

def roles_required(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # 1. ถ้ายังไม่ได้ล็อกอิน ให้เด้งออก (Error 401)
            if not current_user.is_authenticated:
                return abort(401)
            # 2. ถ้าล็อกอินแล้ว แต่ยศ (role) ไม่ตรงกับที่อนุญาต ให้เด้งออก (Error 403)
            if current_user.role not in roles:
                return abort(403)
            # 3. ถ้าผ่านทั้ง 2 ด่าน ให้ใช้งานหน้าเว็บนั้นได้ปกติ
            return f(*args, **kwargs)
        return wrapped
    return wrapper