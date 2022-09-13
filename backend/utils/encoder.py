import decimal
import datetime
import flask.json
import json
from sqlalchemy.ext.declarative import DeclarativeMeta

class JSONEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        # Convert Decimal Values
        if isinstance(obj, decimal.Decimal):
            return str(obj)

        # Convert DateTime
        if isinstance(obj, datetime.date):
            return str(obj)

        # Remove _sa_class_manager
        if 'class_' in obj.__dict__:
            if '_sa_class_manager' in obj.__dict__['class_'].__dict__:
                return ''

        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return super(JSONEncoder, self).default(obj)

    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError ("Type %s not serializable" % type(obj))
