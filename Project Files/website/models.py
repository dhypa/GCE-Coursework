from website import db 
from flask_login import UserMixin, FlaskLoginClient
from sqlalchemy.sql import func 



class Users(db.Model, UserMixin):
    def get_id(self):
           return (self.UserID)
    UserID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(150))
    accesslevel = db.Column(db.String())
    
    
class product(db.Model):
    ProductID = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String(150))
    stocklevel = db.Column(db.Integer)
    barcode = db.Column(db.String(13))
    Pricing = db.Column(db.Numeric())
    
    def to_dict(self):
        return {
            'ProductID':self.ProductID,
            'ProductName':self.ProductName,
            'stocklevel':self.stocklevel,
            'barcode':self.barcode,
            'Pricing':self.Pricing
        }
    
#class stockcounter(db.Model):
#    ProductID = db.Column(db.Integer, db.ForeignKey('product.ProductID'))
#    stockremaining = db.Column(db.Integer)
#    criticalthreshold = db.Column(db.Integer)
    