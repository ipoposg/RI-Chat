from simpleapp import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from simpleapp import login

from flask_login import UserMixin

class User(db.Model, UserMixin):
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key = True, autoincrement=True)
  username = db.Column(db.String(50), unique=True)
  password = db.Column(db.String(256))
  date_created = db.Column(db.DateTime, default=datetime.now())
  
  posts= db.relationship('posts', backref='user', lazy=True)
  usergroups = db.relationship('usergroups', backref='user', lazy=True)
  
  
  
  def __repr__(self):
    return "<User {}>".format(self.username)

  def set_password(self, password):
    self.password = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password, password)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class usergroups(db.Model):
  __tablename__ = 'usergroups'
  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  name = db.Column(db.String(256))
  description = db.Column(db.String(256))
  user_id = db.Column((db.Integer), db.ForeignKey('user.id'))
  
  posts = db.relationship('posts', backref='usergroups', lazy=True)
  
  def __init__(self, id ,name , description, user_id):
      self.id = id
      self.name = name
      self.description = description
      self.user_id = user_id

  def __repr__(self):
    return f"{{{self.user_id}}}"


  
class posts(db.Model):
  __tablename__ = 'posts'
  postid = db.Column(db.Integer, primary_key = True)
  groupid=db.Column((db.Integer), db.ForeignKey('usergroups.id'))
  user_id= db.Column(db.Integer, db.ForeignKey("user.id"))
  post_content = db.Column(db.String(511))
  post_date = db.Column(db.DateTime, default=datetime.now())
  
  def __init__(self, postid, groupid, user_id, post_content, post_date):
    self.postid = postid
    self.groupid = groupid
    self.user_id =user_id
    self.post_content = post_content
    self.post_date = post_date
    
  def __repr__(self):
    return '{}-{}-{}-{}'.format(self.groupid, self.user_id, self.post_content, self.post_date)


def insert_dummy_data(db):
  db.drop_all()
  db.create_all()
  admin = User(username="admin")
  guest = User(username="guest")
  admin.set_password("secretpassword")
  guest.set_password("guestpassword")
  db.session.add(admin)
  db.session.add(guest)
  db.session.commit()


  group1 = usergroups(name="Global Group", description = "Group")

  group2 = usergroups(name="Raffles Institution Boys' Brigade", description = "RIBB")
  
  group3 = usergroups(name="Raffles Institution Guitar Ensemble", description = "RIGB")
  
  post1 = posts(post_content="Lol HAHAHAHAHAHAHHAHAHAHAHAHAHAHAHAHH", groupid=1, user_id= 1)


  db.session.add(group1)
  db.session.add(group2)
  db.session.add(group3)
  db.session.add(post1)
  db.session.commit()


#insert_dummy_data(db)