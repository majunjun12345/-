# from models import Model
from models import Model
import models

Model = Model


class User(Model):

    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('username', str, ''),
            ('password', str, ''),
            ('personalized_signature', str, ''),
        ]
        return names

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        import hashlib
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()

        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    def hashed_password(self, pwd):
        import hashlib
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        return s.hexdigest()

    @classmethod
    def register(cls, form):
        name = form['username']
        password = form['password']
        if len(name) > 2 and User.one(username=name) is None:
            password = User.salted_password(password)
            u = User.new(dict(
                username=name,
                password=password,
            ))
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        user = User.one(
            username=form['username'],
            password=User.salted_password(form['password'])
        )
        return user
