import traceback
from flask import jsonify
# from app import app

# import pdb; pdb.set_trace()


def log_error(error=None):
    try:
        err_msg = error.msg 
    except Exception as e: 
        err_msg = error

    try:
        status = error.status_code 
    except Exception as e: 
        status = 400
    
    return jsonify({
        "exception_type": type(error).__name__,
        "error_reason": str(err_msg),
        "status_code": status,
        "traceback": traceback.format_exc(),
        'content-type': 'application/json'
    })

class Base(Exception):
    def __init__(self, msg, status_code=500, log_msg=None, title=None):
        super().__init__(msg)
        self.status_code = status_code
        self.msg = msg
        self.log_msg = log_msg
        self.title = title

class ProviderMissing(Base):
    def __init__(self, msg=None, log_msg=None, title=None):
        super().__init__(
            msg=msg or 'Provider missing.',
            status_code=400,
            log_msg=log_msg,
            title=title
        )

class ProviderOffline(Base):
    def __init__(self, msg=None, log_msg=None, title=None):
        super().__init__(
            msg=msg or 'Provider is not online.',
            status_code=400,
            log_msg=log_msg,
            title=title
        )

class DataBaseOffline(Base):
    def __init__(self, msg=None, log_msg=None, title=None):
        super().__init__(
            msg=msg or 'Database is not online.',
            status_code=400,
            log_msg=log_msg,
            title=title
        )

class DatabaseError(Base):
    def __init__(self, msg=None, log_msg=None, title=None):
        super().__init__(
            msg=msg or 'Database error.',
            status_code=400,
            log_msg=log_msg,
            title=title
        )

class DomainModelDataTypeError(Base):
    def __init__(self, msg=None, log_msg=None, title=None):
        super().__init__(
            msg=msg or 'Data type is not valid',
            status_code=400,
            log_msg=log_msg,
            title=title
        )

class GraphQLRequestError(Base):
    def __init__(self, msg=None, log_msg=None, title=None):
        super().__init__(
            msg=msg or 'Data type is not valid',
            status_code=400,
            log_msg=log_msg,
            title=title
        )