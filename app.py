from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify
from database import init_db
from models import User, Sensor
from utils import login_required
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

init_db()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.login(email, password)
        if user:
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['user_name'] = user.name
            session['user_birthday'] = user.birthday
            session['user_picture'] = user.picture
            return redirect(url_for('main'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        birthday = request.form['birthday']
        if User.register(email, password, name, birthday):
            return redirect(url_for('login'))
        else:
            flash('Email already registered', 'error')
    return render_template('register.html')

@app.route('/main')
@login_required
def main():
    user_picture = session.get('user_picture', 'static/defaultpfp.png')
    user_id = session['user_id']
    sensores = Sensor.get_sensors_by_user(user_id)
    return render_template('main.html', user_email=session['user_email'], user_name=session['user_name'], user_picture=user_picture, sensores=sensores)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        picture = request.files['picture']
        picture_data = picture.read() if picture else None
        User.update_profile(session['user_id'], email, password, picture_data, name, session['user_birthday'])
        session['user_email'] = email
        session['user_name'] = name
        if picture_data:
            session['user_picture'] = f'static/user_{session["user_id"]}_profile.png'
        return redirect(url_for('main'))
    user_picture = session.get('user_picture', 'static/defaultpfp.png')
    return render_template('profile.html', user_email=session['user_email'], user_name=session['user_name'], user_birthday=session['user_birthday'], user_picture=user_picture)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/user_picture/<int:user_id>')
def user_picture(user_id):
    picture_path = User.get_picture(user_id)
    if picture_path:
        return send_file(picture_path, mimetype='image/png')
    else:
        return send_file('static/defaultpfp.png', mimetype='image/png')

@app.route('/update_sensor', methods=['POST'])
@login_required
def update_sensor():
    sensor_id = request.form['sensor_id']
    status = request.form['status']
    Sensor.update_status(sensor_id, status)
    return "Status updated", 200

@app.route('/add_sensor', methods=['POST'])
@login_required
def add_sensor():
    nome = request.form['nome']
    user_id = session['user_id']
    Sensor.add_sensor(nome, user_id)
    return redirect(url_for('main'))

@app.route('/delete_sensor', methods=['POST'])
@login_required
def delete_sensor():
    sensor_id = request.form['sensor_id']
    Sensor.delete_sensor(sensor_id)
    return redirect(url_for('main'))

@app.route('/get_sensor_data/<int:sensor_id>')
@login_required
def get_sensor_data(sensor_id):
    data = Sensor.get_sensor_data(sensor_id)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
