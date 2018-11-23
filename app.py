from __future__ import division
from flask import Flask, render_template, abort, redirect, url_for, request, flash, session
import model as model
import modelBeat as modelBeat
import os
from flask_bcrypt import Bcrypt
from flask_session import Session

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# session = Session()
# session.init_app(app)

# Routing----------------------------------------------------------------------
@app.route('/')
def root():
    return redirect(url_for('login'))

# Home
@app.route('/home/')
@app.route('/home/<error>')
def home(error=None):
    if 'user' in session:
        # Request Headers, sent on every request
        print("\n\n\n[Client-side]\n", request.headers)
        if 'visits' in session:
            # getting value from session dict (Server-side) and incrementing by 1
            session['visits'] = session.get('visits') + 1
        else:
            # first visit, generates the key/value pair {"visits":1}
            session['visits'] = 1
            # 'session' cookie tracked from every request sent
            print("[Server-side]\n", session)
        print("Total visits:{0}".format(session.get('visits')))
        users = model.get_all_users()
        if error=="":
            return render_template('index.html', error="", users=users), 200
        else:
            return render_template('index.html', error=error, users=users), 200
    return render_template('login.html', msg='You are not logged in'), 200

@app.route('/beats/')
def beats():
    if 'user' in session:
        beats = modelBeat.get_all_beats()
        return render_template('all_beats.html', beats=beats), 200
    return redirect(url_for('home'))

@app.route('/home/<string:name>/<string:beat>')
def get_beat(name,beat):
    if 'user' in session:
        infos = modelBeat.get_beat_for_beatmaker(name,beat)
        return render_template('get_beat.html', name=name, beat=beat, infos=infos)
    return redirect(url_for('home'))

@app.route('/sampler/')
def sampler():
    if 'user' in session:
        return render_template('sampler.html'), 200
    return redirect(url_for('home'))

@app.route('/login/')
def login():
    return render_template('login.html'), 200

@app.route('/connexion/', methods=['POST'])
def connexion():
    user = request.form['username']
    password = request.form['password']
    msg = model.decrypt_method(user, password)
    if msg == "success" :
        session['user'] = user
        session['mail'] = model.get_mail_method(user)
        session['password'] = model.get_user_password_method(user)
        msg = "Welcome "+user+" !"
        return home(msg)
    return render_template('login.html', msg='Failed connection'), 200

@app.route('/register/')
@app.route('/register/<error>')
def register(error=None):
    if not error:
        res = render_template('register.html')
    else:
        res = render_template('register.html', error=error)
    return res

@app.route('/add_user/', methods=['POST'])
def add_user():
    if 'user' in session:
        user = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_verif = request.form['password_verif']
        msg = model.verify_method(user, email, password, password_verif)
        if msg == "success":
            res = login()
        else:
            res = register(msg)#msg="error"
        return res
    return redirect(url_for('home'))

@app.route('/delete_user/', methods=['POST'])
def delete_user():
    if 'user' in session:
        user = request.form['username']
        password = request.form['password']
        if model.decrypt_method(user, password) == "success":
            msg = model.delete_user_method(user)
        else:
            msg = model.decrypt_method(user, password)
        return home(msg)
    return redirect(url_for('home'))

@app.route('/modify_password/', methods=['POST'])
def modify_password():
    if 'user' in session:
        user = session['user']
        password = request.form['password']
        new_password = request.form['new_password']
        new_password_verif = request.form['new_password_verif']
        if model.decrypt_method(user, password) == "success":
            if new_password == new_password_verif:
                msg = model.update_user_method(user, new_password)
            msg = "Password not equals!"
        else:
            msg = model.decrypt_method(user, password)
        return home(msg)
    return redirect(url_for('home'))

@app.route('/add_mark/<string:beat>')
def add_mark(beat):
    if 'user' in session:
        msg = model.add_mark_method(beat)
        return home(msg)
    return redirect(url_for('home'))

@app.route('/del_mark/<string:beat>')
def del_mark(beat):
    if 'user' in session:
        msg = model.del_mark_method(beat)
        return home(msg)
    return redirect(url_for('home'))

@app.route('/logout/')
def logout():
    if 'user' in session:
        # remove the username from the session if it's there
        session.pop('user', None)
        session.pop('mail', None)
        session.pop('password', None)
        session.pop('visits', None)
        return render_template('login.html', msg='You are logged out'), 200
    return redirect(url_for('home'))

# Genre
@app.route('/genre/')
def genre():
    if 'user' in session:
        return render_template('genre.html')
    return redirect(url_for('home'))

@app.route('/genre/<string:name>')
def get_genre(name):
    if 'user' in session:
        beats = modelBeat.get_beats_by_genre(name)
        return render_template('get_genre.html', name=name, infos=beats)
    return redirect(url_for('home'))

@app.route('/genre/<string:genre>/<string:beat>')
def get_beat_for_genre(genre,beat):
    if 'user' in session:
        infos = modelBeat.get_beat_for_genre(genre,beat)
        return render_template('get_beat.html', genre=genre, beat=beat, infos=infos)
    return redirect(url_for('home'))

# Beatmaker
@app.route('/beatmaker/')
def beatmaker():
    if 'user' in session:
        beatmaker = modelBeat.get_all_beatmaker()
        return render_template('beatmaker.html', beatmaker=beatmaker)
    return redirect(url_for('home'))

@app.route('/beatmaker/<string:name>')
def get_beatmaker(name):
    if 'user' in session:
        infos = modelBeat.get_beat_by_beatmaker(name)
        return render_template('get_beatmaker.html', name=name, infos=infos)
    return redirect(url_for('home'))

@app.route('/beatmaker/<string:name>/<string:beat>')
def get_beat_for_beatmaker(name,beat):
    if 'user' in session:
        infos = modelBeat.get_beat_for_beatmaker(name,beat)
        return render_template('get_beat.html', name=name, beat=beat, infos=infos)
    return redirect(url_for('home'))

# Error handler-----------------------------------------------------------------
@app.errorhandler(400)
def page_not_found (error):
    message = "Server cannot/will not process the request"
    return render_template('error.html', nb=400, message=message, error=error)
@app.errorhandler(401)
def page_not_found (error):
    message = "User doesn't have the necessary credentials"
    return render_template('error.html', nb=401, message=message, error=error)
@app.errorhandler(403)
def page_not_found (error):
    message = "Don't have the permissions"
    return render_template('error.html', nb=403, message=message, error=error)
@app.errorhandler(404)
def page_not_found (error):
    message = "Internal Server Error"
    return render_template('error.html', nb=404, message=message, error=error)

if __name__ == "__main__":
    app.run(debug=True)
