from app import app, db

def post(data):
    db.session.add(data)
    db.session.commit()
    app.logger.info(f"{data} inserted into db.")