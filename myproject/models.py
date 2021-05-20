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


class VolunteerDocuments(db.Model):
    IDD = db.Column(db.Integer,primary_key = True)

    IDV = db.Column(db.Integer,db.ForeignKey('volunteers.IDV'))
    Dname = db.Column(db.Text)
    DocDescription = db.Column(db.String(500))
    Document = db.Column(db.LargeBinary)
    DateAdded = db.Column(db.Text)

    def __init__(self,IDV,Dname,DocDescription,image,DateAdded):
       
        self.IDV = IDV
        self.Dname = Dname
        self.DocDescription = DocDescription
        self.image = image
        self.DateAdded = DateAdded

    def __repr__(self):
        return f"Document Name: {self.Dname}, Description: {self.DocDescription} "


class VolunteersInPoss(db.Model):
    id = db.Column(db.Integer,primary_key=True)

    IDV = db.Column(db.Integer,db.ForeignKey('volunteers.IDV'))
    IDP = db.Column(db.Integer,db.ForeignKey('poss.IDP'))
    TimeS = db.Column(db.Text)
    Statusvp = db.Column(db.Text)
    #TimeF = db.Column(db.Text)

    def __init__(self,IDV,IDP,TimeS,Statusvp):
        self.IDV = IDV
        self.IDP = IDP
        self.TimeS = TimeS
        #self.TimeF = TimeF
        self.Statusvp = Statusvp

    def __repr__(self):
        return f"ID Volunteer: {self.IDV} , ID Poss: {self.IDP}"   

class MFile(db.Model):
    __tablename__ = 'mfile'

    IDF = db.Column(db.Integer,primary_key= True)
    IDM = db.Column(db.Integer,db.ForeignKey('meetings.IDM'))
    Filename = db.Column(db.Text)
    FileDescription = db.Column(db.Text)
    TheFile = db.Column(db.LargeBinary)
    AddTime = db.Column(db.Text)

    def __init__(self,IDM,FileName,FileDescription,image,AddTime):
        self.IDM = IDM
        self.FileName = FileName
        self.FileDescription = FileDescription
        self.image = image
        self.AddTime = AddTime

    def __repr__(self):
        return f"and ID of Meetings: {self.IDM}.."    


class Volunteers(db.Model):
    IDV = db.Column(db.Integer,primary_key = True)
    emailv = db.Column(db.String(64))
    FnameV = db.Column(db.Text)
    SnameV = db.Column(db.Text)
    DateOfBirthV = db.Column(db.Text)
    PronounsV = db.Column(db.Text)
    CityV = db.Column(db.Text)
    AdressV = db.Column(db.Text)
    NutritionV = db.Column(db.Text)
    PhoneNumV = db.Column(db.String(10))
    StatusV = db.Column(db.Text)
    DateAdded = db.Column(db.Text)
    
    Message = db.relationship('Message',backref='volunteers',lazy='dynamic')
    volunteersingroups = db.relationship('VolunteersInGroups',backref='volunteers',lazy='dynamic')
    volunteerDocuments = db.relationship('VolunteerDocuments',backref='volunteers',lazy='dynamic')
    volunteersinPoss = db.relationship('VolunteersInPoss',backref='volunteers',lazy='dynamic')


    def __init__(self,IDV,emailv,FnameV,SnameV,DateOfBirthV,PornounsV,CityV,AdressV,NutritionV,PhoneNumV,StatusV,DateAdded ):
        self.IDV = IDV
        self.emailv=emailv
        self.FnameV = FnameV
        self.SnameV = SnameV
        self.DateOfBirthV = DateOfBirthV
        self.PornounsV = PornounsV
        self.CityV = CityV
        self.AdressV = AdressV
        self.NutritionV = NutritionV
        self.PhoneNumV = PhoneNumV
        self.StatusV = StatusV
        self.DateAdded = DateAdded

    def __repr__(self):
        return f"Volunteer Name: {self.FnameV} {self.SnameV} Volunteer ID: {self.IDV} "

class Poss(db.Model):
    IDP = db.Column(db.Integer,primary_key= True)
    PossName = db.Column(db.Text)
    PossDescription = db.Column(db.Text)
    AddTime = db.Column(db.Text)

    volunteersinPoss = db.relationship('VolunteersInPoss',backref='poss',lazy='dynamic')

    def __init__(self,PossName,PossDescription,AddTime):
        #self.IDP = IDP
        self.PossName = PossName
        self.PossDescription = PossDescription
        self.AddTime = AddTime

    def __repr__(self):
        return f"Poss Name: {self.PossName}, ID Poss: {self.IDP}."



class Student(db.Model):

    __tablename__ = 'students'
    emails = db.Column(db.String(64),primary_key = True)
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
    Studentsinmeeting = db.relationship('StudentsInMeeting',backref='student',lazy=False)

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
    agesingroup = db.Column(db.String(500))

    condidates = db.relationship('Condidate',backref='condidate',lazy=False)
    volunteersinGroups = db.relationship('VolunteersInGroups',backref='group',lazy='dynamic')
    Meetings = db.relationship('Meetings',backref='group',lazy='dynamic')

    def __init__(self,name,regionorsubject,city,agesingroup):
        self.name = name
        self.regionorsubject = regionorsubject
        self.city = city
        self.agesingroup=agesingroup

    def __repr__(self):
        return f"Group Name: {self.name} Group ID: {self.id}"


class VolunteersInGroups(db.Model):
    id = db.Column(db.Integer,primary_key=True)

    #IDV = db.relationship('Volunteers',backref='VolunteersInGroups',uselist=False)
    IDV = db.Column(db.Integer,db.ForeignKey('volunteers.IDV'))
    #IDG = db.relationship('Group',backref='VolunteersInGroups',uselist=False)
    IDG = db.Column(db.Integer,db.ForeignKey('groups.id'))
    TimeS = db.Column(db.Text)
    TimeF = db.Column(db.Text)
    statusV = db.Column(db.Text)

    def __init__(self,IDV,IDG,TimeS,TimeF,statusV):
        self.IDV = IDV
        self.IDG = IDG
        self.TimeS = TimeS
        self.TimeF = TimeF
        self.statusV = statusV

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
    firstname = db.Column(db.Text)
    lastname = db.Column(db.Text)
    pronounc = db.Column(db.Text)
    phonenumc = db.Column(db.String(10))
    stimes = db.Column(db.Text)
    text = db.Column(db.Text)
    status = db.Column(db.Text)



    def __init__(self,group_id,emailc,pronounc,phonenumc,stimes,text,status,firstname,lastname):
        self.group_id = group_id
        self.emailc = emailc
        self.pronounc = pronounc
        self.phonenumc = phonenumc
        self.stimes = stimes
        self.text = text
        self.status = status
        self.fristname =firstname
        self.lastname = lastname
        
class StudentInGroup(db.Model):

    __tablename__ = 'studentsingroups'

    id = db.Column(db.Integer,primary_key= True)
    student_emails = db.Column(db.String(64),db.ForeignKey('students.emails'))
    group_id = db.Column(db.Integer,db.ForeignKey('groups.id'))
    stimes = db.Column(db.Text)
    ftimef = db.Column(db.Text)
    statusg = db.Column(db.Text)


    def __init__(self,stimes,ftimef,student_emails,group_id,statusg):
        self.stimes = stimes
        self.ftimef = ftimef
        self.student_emails = student_emails
        self.group_id = group_id
        self.statusg = statusg

    def __repr__(self):
        return f"the name of the student is {self.student_emails} and he is in group: {self.group_id} and the id of the row is: {self.id}"

class Meetings(db.Model):
    IDM = db.Column(db.Integer,primary_key= True)
    Mdate = db.Column(db.Text)
    Mtime = db.Column(db.Text)
    IDG = db.Column(db.Integer,db.ForeignKey('groups.id'))
    Occurence = db.Column(db.Text) 
    Platform = db.Column(db.Text)
    title = db.Column(db.Text)
    Rate = db.Column(db.Integer)
    Pros = db.Column(db.String(500))
    Cons = db.Column(db.String(500))
    DateAdded = db.Column(db.Text)
    attending = db.Column(db.String(500))

    mfile = db.relationship('MFile',backref='meetings',lazy='dynamic')
    studentsinMeeting = db.relationship('StudentsInMeeting',backref='meetings',lazy='dynamic')

    def __init__(self,Mdate,Mtime,IDG,Occurence,Platform,title,Rate,Pros,Cons,DateAdded,attending):
        self.Mdate = Mdate
        self.Mtime = Mtime
        self.IDG = IDG
        self.Occurence= Occurence
        self.Platform = Platform
        self.title = title
        self.Rate = Rate
        self.Pros = Pros
        self.Cons = Cons
        self.DateAdded = DateAdded
        self.attending = attending

class StudentsInMeeting(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    IDM = db.Column(db.Integer,db.ForeignKey('meetings.IDM'))
    EmailS = db.Column(db.String(64),db.ForeignKey('students.emails'))
    Attendance = db.Column(db.Text)

    def __init__(self,IDM,EmailS,Attendance):
        self.IDM = IDM
        self.EmailS = EmailS
        self.Attendance = Attendance

    def __repr__(self):
        return f"Student Email: {self.EmailS}, ID of Meeting: {self.IDM}. "   
        
class Message(db.Model):
    IDM = db.Column(db.Integer,primary_key=True)
    Mdate = db.Column(db.Text)
    IDV = db.Column(db.Integer,db.ForeignKey('volunteers.IDV'))
    Content = db.Column(db.Text)

    def _init_(self,Mdate,IDV,Content):
        #self.IDM = IDM       
        self.Mdate = Mdate
        self.IDV = IDV
        self.Content = Content
        
    def _repr_(self):
        return f"{Mdate} {Content}"
         
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