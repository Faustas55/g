from HadesV2App import db

class Advert(db.Model):
    __tablename__ = 'advert'
    __table_args__ = { 'extend_existing': True }
    advert_id = db.Column(db.Integer, primary_key=True)   

