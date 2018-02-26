import time

from bson import ObjectId
from pymongo import MongoClient


class Model(object):
    db = MongoClient()['jiyanzheng']

    @classmethod
    def valid_names(cls):
        names = [
            ('deleted', bool, False),
            ('created_time', int, 0),
            ('updated_time', int, 0),
        ]
        return names

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    @classmethod
    def new(cls, form, **kwargs):
        m = cls()

        for name in cls.valid_names():
            k, t, v = name
            if k in form:
                setattr(m, k, t(form[k]))
            else:
                setattr(m, k, v)


        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)
            else:
                raise KeyError


        timestamp = int(time.time())
        m.created_time = timestamp
        m.updated_time = timestamp

        m.save()
        return m

    def save(self):
        name = self.__class__.__name__
        _id = self.db[name].save(self.__dict__)
        self.id = str(_id)

    @classmethod
    def delete(cls, id):
        name = cls.__name__
        query = {
            '_id': ObjectId(id),
        }
        values = {
            '$set': {
                'deleted': True
            }
        }
        cls.db[name].update_one(query, values)

    @classmethod
    def update(cls, id, form):
        name = cls.__name__
        query = {
            '_id': ObjectId(id),


        }
        values = {
            '$set': form,
        }
        cls.db[name].update_one(query, values)
        return cls

    @classmethod
    def _new_with_bson(cls, bson):
        m = cls()
        for key in bson:
            setattr(m, key, bson[key])
        m.id = str(bson['_id'])
        return m

    @classmethod
    def all(cls, **kwargs):
        kwargs['deleted'] = False
        if 'id' in kwargs:
            kwargs['_id'] = ObjectId(kwargs['id'])
            kwargs.pop('id')
        name = cls.__name__
        docuemtns = cls.db[name].find(kwargs)
        l = [cls._new_with_bson(d) for d in docuemtns]
        return l

    @classmethod
    def one(cls, **kwargs):
        documents = cls.all(**kwargs)
        if len(documents) > 0:
            return documents[0]
        else:
            return None

