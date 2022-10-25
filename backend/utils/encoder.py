import decimal
import datetime
import flask.json
# import pdb; pdb.set_trace()

class JSONEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        # print("\nIn JSONEncoder ------ 0")
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

        return super(JSONEncoder, self).default(obj)