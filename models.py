# models for database interaction#

from HadesV2App import db

class Advert(db.Model):
    __tablename__ = "advert"
    __table_args__ = {"extend_existing": True}
    advert_id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.Text)
    category = db.Column(db.Text)
    updated_by = db.Column(db.Text)
    updated_date = db.Column(db.Text)
    seller = db.Column(db.Text)
    polonius_caseid=db.Column(db.Integer)
    
class Takedown(db.Model):
    __tablename__ = "takedowns"
    __table_args__ = {"extend_existing": True}
    advert_id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)
    domain = db.Column(db.Text)
    takedown_confirmed = db.Column(db.Text)
    review = db.Column(db.Text)
