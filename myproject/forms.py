from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, RadioField, FileField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from myproject.models import User

#classes for login and register process:
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register!')

    def check_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=self.data).first():
            raise ValidationError('Your email has been registered already!')

    def check_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=self.data).first():
            raise ValidationError('Sorry, that username is taken!')


#classes for IGY process:

class AddForm(FlaskForm):
    emails = StringField('Email of Student:')
    firstname = StringField('First Name of Student:')
    lastname = StringField('Last Name of Student:')
    dateofbirth = StringField('Date of Birth:')
    pronouns = SelectField('Pronoun', choices = [('בחר/י מתוך הרשימה', 'בחר/י מתוך הרשימה'),('את', 'את'), ('אתה', 'אתה'), ('מעורבת', 'מעורבת')])
    citys = StringField('City:')
    addresss = StringField('Address:')
    nutritions = SelectField('Nutrition', choices = [('בחר/י מתוך הרשימה', 'בחר/י מתוך הרשימה'),('צמחוני', 'צמחוני'), ('טבעוני', 'טבעוני'), ('אוכל כל', 'אוכל כל')])
    phonenums = StringField('Phone Number:')
    schoolname = StringField('Name of School:')
    dateaddeds = StringField('Current Date:')
    statuss = StringField('My statuss:')
    parents = StringField('Family Relationship:')
    details = StringField('Introductory Meeting Summary:')


    submit = SubmitField('Add Student')

class AddGroupForm(FlaskForm):

    name = StringField('Name of Group:')
    regionorsubject = SelectField('Region or Subject of Group', choices = [('בחר/י מתוך הרשימה', 'בחר/י מתוך הרשימה'),('צפון', 'צפון'), ('שרון', 'שרון'), ('מרכז', 'מרכז'),('שפלה', 'שפלה'),('דרום', 'דרום'),('תחום טרנס', 'תחום טרנס'),('תחום דתיות', 'תחום דתיות'),('תחום אלואן', 'תחום אלואן'),('תכנית ניר', 'תכנית ניר')])
    city = StringField('City of Group:')

    #להכניס נתונים קבועים לתוך הגילאים ולהתאים כאן את הערכים
    submit = SubmitField('Add Group')

class AddAgeGroupForm(FlaskForm):
    age_id = RadioField('Ages', choices=[('1','ז'), ('2','ח'), ('3','ט'),('4','י'),('5','יא'),('6','יב')])
    group_id = IntegerField('ID of Group:')
    submit = SubmitField('Add age to Group')

class DelForm(FlaskForm):

    student_emails = StringField('Email of Students to Remove:')
    submit = SubmitField('Remove Students')

class DelGroupForm(FlaskForm):

    student_in_group_id = StringField('ID of student In Group')
    submit = SubmitField('Remove Student from Group')

class AddStuGroupForm(FlaskForm):

    group_id = SelectField('קבוצה:', choices = [('1','תל אביב(ז׳-ט׳)'), ('2','גבעתיים(ז׳-ט׳)'),('3','רחובות(י׳-י״ב)')])
    student_emails = StringField("Email of Student: ")
    # stimes = StringField('start time')
    # ftimef = StringField('finish time')
    submit = SubmitField('Add him')

class NewCondidateForm(FlaskForm):
#לשנות לסלקט ולא לסטרינג ולדאוג שהמשתמש יבחר קבוצה ויוזן איי די.
    #group_id = StringField('ID of Group that you want to assign')
    group_id = SelectField('קבוצה:', choices = [('1','תל אביב(ז׳-ט׳)'), ('2','גבעתיים(ז׳-ט׳)'),('3','רחובות(י׳-י״ב)')])
    emailc = StringField("אימייל: ")
    pronounc = SelectField('לשון פניה', choices = [('בחר/י מתוך הרשימה', 'בחר/י מתוך הרשימה'),('את', 'את'), ('אתה', 'אתה'), ('מעורבת', 'מעורבת')])
    phonenumc = StringField('מספר טלפון:')
    # stimes = StringField('start time')
    submit = SubmitField('Send')

class AddVolunteerForm(FlaskForm):
    IDV = StringField('ID Of Volunteer:')
    FnameV = StringField('First Name of Volunteer:')
    SnameV = StringField('Last Name of Volunteer:')
    DateOfBirthV = StringField('Date of Birth:')
    PronounsV = SelectField('Pronoun', choices = [('בחר/י מתוך הרשימה', 'בחר/י מתוך הרשימה'),('את', 'את'), ('אתה', 'אתה'), ('מעורבת', 'מעורבת')])
    CityV = StringField('City:')
    AdressV = StringField('Address:')
    NutritionV = SelectField('Nutrition', choices = [('בחר/י מתוך הרשימה', 'בחר/י מתוך הרשימה'),('צמחוני', 'צמחוני'), ('טבעוני', 'טבעוני'), ('אוכל כל', 'אוכל כל')])
    PhoneNumV = StringField('Phone Number:')
    StatusV = SelectField('Nutrition', choices = [('בחר/י מתוך הרשימה', 'בחר/י מתוך הרשימה'),('פעיל', 'פעיל'), ('לא פעיל', 'לא פעיל'), ('הודח ', 'הודח  ')])
    submit = SubmitField('Send')

class VolunteersInGroupsForm(FlaskForm):
    IDV = StringField('ID Of Volunteer:')
    IDG = SelectField('קבוצה:', choices = [('1','תל אביב(ז׳-ט׳)'), ('2','גבעתיים(ז׳-ט׳)'),('3','רחובות(י׳-י״ב)')])
    emailc = StringField("אימייל: ")
    #TimeS = StringField('Current Date:')
    TimeF = StringField('Current Date:')

    submit = SubmitField('בצע שידוך  (:')

class VolunteerDocumentsForm(FlaskForm):
    IDV = StringField('ID Of Volunteer:')
    Dname = SelectField('Document Name:', choices = [('אחר', 'אחר'),('אישור משטרה', 'אישור משטרה'), ('תעודת זהות', 'תעודת זהות'), (' מסמכי מתנדב', ' מסמכי מתנדב')])
    DocDescription = StringField('Document Description:')
    Document = FileField('Document')

    submit = SubmitField(' העלה מסמך  (:')

class VolunteersInPossForm(FlaskForm):
    IDV = StringField('ID Of Volunteer:')
    IDP = SelectField('תפקיד בארגון:', choices = [('1','מדריכ/ה'), ('2','ספריית הדרכה'),('3','מחלקת הדרכה - בתי ספר'),('4','רכז/ת חינוך'),('5','רכז/ת פעילות')])

    submit = SubmitField(' שייך תפקיד למתנדב (:')

class AddPossForm(FlaskForm):
    IDP = StringField('ID of the Poss:')
    PossName = StringField('Poss Name:')
    PossDescription = StringField('Poss Description:')
    #AddTime = StringField('Current Date:')
    
    submit = SubmitField('Add Poss')
    
class MeetingsForm(FlaskForm):
    Mdate = StringField('תאריך:')
    Mtime = StringField('שעה:')
    IDG = StringField('ID of Group')
    Occurence = SelectField('סטטס פגישה?', choices = [('1','ממתין'),('2','בוטל'),('3','בוצע')])
    Platform = SelectField('סוג פגישה:', choices = [('1','פרונטאלי'),('2','מקוון')])
    Rate = SelectField('דרוג:', choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Pros = StringField('נקודות לשימור:')
    Cons = StringField('נקודות לשיפור:')

    submit = SubmitField('צור פגישה')

class MFileForm(FlaskForm):
    IDM = StringField('ID of Meetings:') 
    FileName = StringField('שם הקובץ:') 
    FileDescription = StringField('תאור הקובץ:')
    TheFile = FileField('מסמך:')

    submit = SubmitField('העלה קובץ')

class StudentsInMeetingForm(FlaskForm):
    IDM = StringField('ID of Meetings:') 
    EmaillS = StringField('אימייל של החניך:') 
    Attendance = StringField('נוכחות:')

    submit = SubmitField('סמן')