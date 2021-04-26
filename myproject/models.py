from myproject import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()


# The user_loader decorator allows flask-login to load the current user
# and grab their id.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash,password)

class Student(db.Model):

    __tablename__ = 'students'
    emails = db.Column(db.String(10),primary_key = True)
    firstname = db.Column(db.Text)
    lastname = db.Column(db.Text)
    dateofbirth = db.Column(db.Text)
    pronouns = db.Column(db.Text)
    citys = db.Column(db.Text)
    addresss = db.Column(db.Text)
    nutritions = db.Column(db.Text)
    phonenums = db.Column(db.String(10))
    schoolname = db.Column(db.Text)
    dateaddeds = db.Column(db.Text)
    statuss = db.Column(db.Text)
    parents = db.Column(db.Text)
    details = db.Column(db.String(500))

    studentsingroups = db.relationship('StudentInGroup',backref='student',lazy=False)

    def __init__(self,emails,firstname,lastname,dateofbirth,pronouns,citys,addresss,nutritions,phonenums,schoolname,dateaddeds,statuss,parents,details):
        self.emails = emails
        self.firstname = firstname
        self.lastname = lastname
        self.dateofbirth = dateofbirth
        self.pronouns = pronouns
        self.citys = citys
        self.addresss = addresss
        self.nutritions = nutritions
        self.phonenums = phonenums
        self.schoolname = schoolname
        self.dateaddeds = dateaddeds
        self.statuss = statuss
        self.parents = parents
        self.details = details


 #  def __repr__(self):
  #      if self.studentingroup:
   #         return f"Student full  name is{self.emails},{self.firstname},{self.lastname}, {self.dateofbirth},{self.pronouns},{self.citys},{self.addresss},{self.nutritions},{self.phonenums},{self.schoolname}and group is {self.studentingroup.student_emails}"
    #    else:
     #       return f"Student full  name is{self.emails},{self.firstname},{self.lastname}, {self.dateofbirth},{self.pronouns},{self.citys},{self.addresss},{self.nutritions},{self.phonenums},{self.schoolname}and has no group assigned yet."

class Group(db.Model):

    __tablename__ = 'groups'

    id = db.Column(db.Integer,primary_key= True)
    name = db.Column(db.Text)
    regionorsubject = db.Column(db.Text)
    city = db.Column(db.Text)
    
    condidates = db.relationship('Condidate',backref='condidate',lazy=False)

    def __init__(self,name,regionorsubject,city):
        self.name = name
        self.regionorsubject = regionorsubject
        self.city = city

    def __repr__(self):
        return f"Group Name: {self.name}"

class Age(db.Model):

    __tablename__ = 'ages'

    id = db.Column(db.Integer,primary_key= True)
    namea = db.Column(db.Text)
    
    agesingroups = db.relationship('AgesInGroup',backref='ages',lazy=False)


    def __init__(self,namea):
        self.namea = namea

class AgesInGroup(db.Model):

    __tablename__ = 'agesingroups'

    age_id = db.Column(db.Integer,db.ForeignKey('ages.id'),primary_key=True)
    group_id = db.Column(db.Integer,db.ForeignKey('groups.id'))



    def __init__(self,age_id,group_id):
        self.age_id = age_id
        self.group_id = group_id


class Condidate(db.Model):

    __tablename__ = 'condidates'

    id = db.Column(db.Integer,primary_key= True)
    group_id = db.Column(db.Integer,db.ForeignKey('groups.id'))
    emailc = db.Column(db.String(64), unique=True, index=True)
    stimes = db.Column(db.Text)



    def __init__(self,group_id,emailc,stimes):
        self.group_id = group_id
        self.emailc = emailc
        self.stimes = stimes

class StudentInGroup(db.Model):

    __tablename__ = 'studentsingroups'

    id = db.Column(db.Integer,primary_key= True)
    student_emails = db.Column(db.String(10),db.ForeignKey('students.emails'))
    group_id = db.Column(db.Integer,db.ForeignKey('groups.id'))
    stimes = db.Column(db.Text)
    ftimef = db.Column(db.Text)
  

    def __init__(self,stimes,ftimef,student_emails,group_id):
        self.stimes = stimes
        self.ftimef = ftimef
        self.student_emails = student_emails
        self.group_id = group_id

    def __repr__(self):
        return f"the name of the student is {self.student_emails} and he is in group: {self.group_id}"


user_test1 = Age(namea='ז')
user_test2 = Age(namea='ח')
user_test3 = Age(namea='ט')
user_test4 = Age(namea='י')
user_test5 = Age(namea='יא')
user_test6 = Age(namea='יב')

db.session.add(user_test1)
db.session.add(user_test2)
db.session.add(user_test3)
db.session.add(user_test4)
db.session.add(user_test5)
db.session.add(user_test6)



db.create_all()
db.session.commit()