#loremipsum XDD
import flask
from functools import wraps
import db_utils
import json
import datetime
from flask import Flask, session, redirect, url_for, render_template, request
import uuid
class User:
    def __init__(self):
        self.username = None
        self.user_id = ""
        self.email = ""
        self.password = ""
        self.first_name = ""
        self.last_name = ""
        self.profile_pic = "" #is in link, we're taking it from folder from server
        self.bio = ""
        self.is_active = True
        self.created = None #datetime format
        self.is_moderator = False

    def dict_public(self): #Contains no password and email. Here is only publicly available data. Maybe I should remove is_active
        dict_public = {
            "user_id":self.user_id,
            "username":self.username,
            "first_name":self.first_name,
            "last_name":self.last_name,
            "profile_pic":self.profile_pic,
            "bio":self.bio,
            "is_active":self.is_active,
            "created":self.created,
            "is_moderator":self.is_moderator
        }
        return dict_public

    def pack_in_json(self, pack_dict): #just dict to JSON, maybe used for every dict
        return json.dumps(pack_dict)

    def import_from_db_public(self, user_id): #we get everything besides email and password.
        imported_data = db_utils.recall_user(user_id)
        self.username = imported_data[1]
        self.first_name = imported_data[2]
        self.last_name = imported_data[3]
        self.profile_pic = imported_data[4]
        self.bio = imported_data[5]
        self.created = imported_data[6]
        #add maybe some message to console with "[SUCCESS]User [user_id] data was recalled successfully"

    def log_out(self):
        self.username = None
        self.user_id = ""
        self.email = ""
        self.password = ""
        self.first_name = ""
        self.last_name = ""
        self.profile_pic = ""  # is in link, we're taking it from folder from server
        self.bio = ""
        self.is_active = True
        self.created = None  # datetime format
        self.is_moderator = False
        #message of logout in console

    def import_from_db_private(self, user_id):
        imported_data_private = db_utils.recall_user(user_id) #do private recall in db, but idk is it safe...

    def update_public(self, new_info: dict = None): #new info must be dict
        pass


class Post: #No public or private
    def __init__(self): #Every name of attr. is name of column in db(Post table)
        self.post_id = ""
        self.text = ""
        self.image = ""
        self.author_id = None
        self.created = None

    def dict(self): #pack data into dict for further jsonization
        dict_post = {
            "post_id":self.post_id,
            "text":self.text,
            "author_id":self.author_id,
            "created":self.created,
            "image":self.image,
        }
        return dict_post

    def pack_in_json(self, pack_dict): return json.dumps(pack_dict)

    def import_from_db(self, post_id): #updating or getting data
        imported_data = db_utils.recall_post(post_id)
        self.post_id = imported_data[0]
        self.text = imported_data[1]
        self.author_id = imported_data[2]
        self.created = imported_data[3]
        self.image = imported_data[4]

    def clear(self): #IT IS NOT DELETION, JUST CLEARING DATA
        self.text = ""
        self.author_id = ""
        self.created = None
        self.image = ""
        self.post_id = ""
        #console message



#CZĘŚĆ Z FLASKIEM
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')

        if user_id is None:
            flask.flash("To see this page please log in.", "error")
            return redirect(url_for('login'))

        cur_user = User()
        cur_user.import_from_db_public(user_id)

        kwargs['cur_user'] = cur_user

        return f(*args, **kwargs)

    return decorated_function

app = Flask(__name__)

@app.route('/')
@app.route("/index")
def index():
    return render_template("index.html")
    #here must be a "Qbi - the best ever!" "our values are" and other corporate bullshit

@app.route('/login', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        login_data = request.get_json(force = True)
        username = login_data.get("username", "")
        email = login_data.get("email", "")
        # metoda.get jest bezpieczniejsza, ponieważ w przypadku braku danych nie wyrzuci KeyError
        user_id = db_utils.log_in(username, email, password)
        if user_id is None:
            flask.flash("Wrong login/email or password")
            return render_template("login.html")
        else:
            cur_user = User()
            cur_user.user_id = user_id
            cur_user.update_public()
            cur_user.password = password #should I replace it with private update? I don't want to do request to database too often.
            cur_user.email = email
            return redirect(url_for("feed"))
            #I don't know: return /login or /feed?
    return render_template("login.html")
    #We send nothing but maybe answers... Yet I need to figure out how to send "wrong login or password" fast n' effective
    #TIP:  GET - We send data to Front. POST - we save data on server.

@app.route('/register', methods = ["POST", "GET"])
def register():
    if request.method == "POST":
        register_data = request.get_json(force = True)
        #get_json returns dictionary from the very beginning.
        #Do I need to enter data manually from json on server, or first put it on db, and do update?... For now I'll do it with db.
        username = register_data["username"]
        password = register_data["password"]
        email = register_data["email"]
        first_name = register_data["first_name"]
        last_name = register_data["last_name"]
        user_id = db_utils.register_user(username, email, password, first_name, last_name)
        if user_id:
            return {"status": "success", "user_id": user_id}, 201
        else:
            return {"status": "fail", "user_id": user_id}, 400

        cur_user = User()
        cur_user.user_id = user_id
        cur_user.update_public()
        cur_user.password = password
        cur_user.email = email
    return render_template("register.html")
    #we don't send anything special

@app.route('/logout', methods = ["POST"])
@login_required
def logout(cur_user):
    try:
        del cur_user
    except NameError:
        pass
    session.clear()
    return redirect(url_for("index"))

    #just "you've been logged out. Returning to homepage..." and timer thingy

@app.route("feed")
@login_required
def feed():

    return render_template("feed.html")

user_return = None # temporary, just to ask LLM can I do such thingy with address, or I need to do it another way

@app.route(f"profile/<username>")
@login_required
def profile(username):
    return render_template("profile.html")


