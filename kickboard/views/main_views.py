from flask import Blueprint, current_app
from flask import redirect, render_template, request, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from kickboard import db
from kickboard.models import information

import os

bp = Blueprint('main_views', __name__, url_prefix='/')

#POST 요청으로 json 받아서 user 객체 생성
@bp.route('/signup1/', methods=['POST'])
def signup1():
    if request.method == 'POST':
        data = request.get_json() #json 데이터 받아옴

        if not data: 
            return jsonify({'error': '데이터가 올바르지 않습니다'}), 400

        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        name = data.get('name')
        phone_number = data.get('phone_number')
        
        existing_user = information.query.filter_by(email=email).first()
        if existing_user:
            return "아이디가 이미 존재합니다", 202

        if password != confirm_password:
            return "비밀번호가 일치하지 않습니다", 203

        hashed_password = generate_password_hash(password)
        user = information(email=email, password=hashed_password, name=name, phone_number=phone_number)
        db.session.add(user)
        db.session.commit()

        return "회원가입이 성공적으로 완료되었습니다", 201



@bp.route('/signin1/', methods=['POST'])
def signin1():
    if request.method == 'POST':
        data = request.get_json()

        if not data: 
            return jsonify({'error': '데이터가 올바르지 않습니다'}), 400

        email = data.get('email')
        password = data.get('password')
        
        user = information.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session.clear()
            session['session_user'] = user.email #세션에 id 저장
            return "로그인 성공", 200
        else:
            return "비밀번호가 일치하지 않습니다" ,401


#테스트가 안된 코드
@bp.route('/image1/', methods=['POST'])
def getImage1():
        if request.method == 'POST':
            if 'image_file' not in request.files:
                return 'File is missing', 404
            
            image_file = request.files['image_file']
            
            if image_file.filename == '':
                return 'File is missing', 404
            
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'],filename))

            return "이미지 파일 전송 성공", 200
        
