from flask import (
    request,
    session,
    Blueprint,
)
from models.user import User
import json
from app import cache

main = Blueprint('index', __name__)


def current_user():
    uid = session['user_id']
    u = User.one(id=uid)
    print('user:',u)
    return u


@main.route("/")
def index():
    return 'mamengli'


@main.route("/register", methods=['POST', 'GET'])
@cache.cached(timeout=3600, key_prefix='view_%s', unless=None)
def register():
    if request.method == 'POST':
        para = request.get_data()
        form = json.loads(para)
        u = User.register(form)
        return para
    else:
        return 'please register'


@main.route("/login", methods=['POST', 'GET'])
@cache.cached(timeout=3600, key_prefix='view_%s', unless=None)
def login():
    if request.method == 'POST':
        para = request.get_data()
        form = json.loads(para)
        u = User.validate_login(form)
        if u is None:
            return 'please login'
        else:
            session['user_id'] = u.id
            session.permanent = True
            return para


@main.route('/profile')
@cache.cached(timeout=3600, key_prefix='view_%s', unless=None)
def user_profile():
    us = current_user()
    print('uu:',us)
    return 'username:{},password:{}, personalized_signature:{}'.format(us.username, us.password, us.personalized_signature)


@main.route('/settings',methods=['POST', 'GET'])
@cache.cached(timeout=3600, key_prefix='view_%s', unless=None)
def modify_information():
    u = current_user()
    if request.method == 'POST':
        para = request.get_data()
        form = json.loads(para)
        if not form['username']:
            form['username'] = u.username
        if not form['password']:
            form['password'] = u.password
        if not form['personalized_signature']:
            form['personalized_signature'] = u.personalized_signature
        User.update(u.id, form)
    return 'settings'


@main.route('/logout', methods=['GET'])
@cache.cached(timeout=3600, key_prefix='view_%s', unless=None)
def logout():
    u = current_user()
    session.pop('user_id', None)
    return 'logout'