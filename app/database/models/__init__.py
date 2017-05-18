from app import db


class Repo(db.Model):
    id = db.Column(db.TEXT, primary_key=True)
    path = db.Column(db.TEXT, unique=True)
    deploy_path = db.Column(db.TEXT, unique=True)
    url = db.Column(db.TEXT)
    last_used = db.Column(db.INTEGER)
    active = db.Column(db.BOOLEAN)

    def __init__(self, identifier, path, deploy_path, url, last_used, active):
        self.id = identifier
        self.path = path
        self.deploy_path = deploy_path
        self.url = url
        self.last_used = last_used
        self.active = active

    def __repr__(self):
        return "<ID: %s | URL: %s>" % (self.id, self.url)
