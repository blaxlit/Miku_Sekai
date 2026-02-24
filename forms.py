from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, URL, Optional

class RegisterForm(FlaskForm):
    username = StringField('ชื่อผู้ใช้', validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField('รหัสผ่าน', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('สมัครสมาชิก')

class LoginForm(FlaskForm):
    username = StringField('ชื่อผู้ใช้', validators=[DataRequired()])
    password = PasswordField('รหัสผ่าน', validators=[DataRequired()])
    submit = SubmitField('เข้าสู่ระบบ')

class AddSongForm(FlaskForm):
    title = StringField('ชื่อเพลง', validators=[DataRequired(), Length(max=100)])
    producer = StringField('โปรดิวเซอร์ (Vocaloid P)', validators=[DataRequired(), Length(max=100)])
    youtube_url = StringField('ลิงก์ YouTube (ถ้ามี)', validators=[Optional(), URL()])
    submit = SubmitField('เพิ่มเพลงลงคลัง')