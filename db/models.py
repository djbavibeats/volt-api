import json
import datetime

from . import db
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

print(datetime)

def default(o):
   if isinstance(o, datetime):
      return o.isoformat()

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_name = db.Column(db.String)
    description = db.Column(db.String)
    ecommerce = db.Column(db.Boolean)
    domain = db.Column(db.String)
    domain_provider = db.Column(db.String)
    domain_email = db.Column(db.String)
    domain_username = db.Column(db.String)
    domain_password = db.Column(db.String)
    hosting = db.Column(db.String)
    hosting_email = db.Column(db.String)
    hosting_username = db.Column(db.String)
    hosting_password = db.Column(db.String)
    web_platform = db.Column(db.String)
    web_platform_email = db.Column(db.String)
    web_platform_username = db.Column(db.String)
    web_platform_password = db.Column(db.String)
    socials = db.Column(db.String)
    pages = db.Column(db.String)
    # Pages
    # Analytics
    # Integrations
    # Billing Information

    def serializers(self):
        dict_val={"id":self.id,"user_id":self.user_id,"project_name":self.project_name,"description":self.description,"ecommerce":self.ecommerce,"domain":self.domain,"domain_provider":self.domain_provider,
        "domain_email":self.domain_email,"domain_username":self.domain_username,"domain_password":self.domain_password,"hosting":self.hosting,"hosting_email":self.hosting_email,"hosting_username":self.hosting_username,
        "hosting_password":self.hosting_password,"web_platform":self.web_platform,"web_platform_email":self.web_platform_email,"web_platform_username":self.web_platform_username,"web_platform_password":self.web_platform_password,
        "socials":self.socials,"pages":self.pages}
        return json.loads(json.dumps(dict_val,default=default))
    

class User(db.Model, UserMixin, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    projects = db.relationship('Project')