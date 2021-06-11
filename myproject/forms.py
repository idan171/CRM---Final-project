from flask_wtf import FlaskForm
from numpy import str_
from wtforms import StringField, PasswordField, SubmitField,TextAreaField, SelectField, IntegerField, RadioField, FileField,SelectMultipleField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from myproject.models import User, Group, Poss, Student
from wtforms.widgets import TextArea


#classes for login and register process:
class LoginForm(FlaskForm):
    email = StringField('דוא״ל', validators=[DataRequired(), Email()])
    password = PasswordField('סיסמא', validators=[DataRequired()])
    submit = SubmitField('התחברות')


class RegistrationForm(FlaskForm):
    id = StringField('תעודת זהות:')
    email = StringField('דוא״ל', validators=[DataRequired(),Email()])
    username = StringField('שם משתמש', validators=[DataRequired()])
    password = PasswordField('סיסמא', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('אימות סיסמא', validators=[DataRequired()])
    firstname = StringField('שם פרטי')
    lastname = StringField('שם משפחה')
    tel = StringField('מספר נייד')
    permission = StringField('הרשאות')

    submit = SubmitField('שלח פרטים')

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
    emails = StringField('דואר אלקטורני:')
    firstname = StringField('שם פרטי:')
    lastname = StringField('שם משפחה:')
    dateofbirth = StringField('תאריך לידה:')
    pronouns = SelectField('לשון פניה', choices = [('בחר/י מתוך הרשימה', 'בחר/י מתוך הרשימה'),('את', 'את'), ('אתה', 'אתה'), ('מעורבת', 'מעורבת')])
    citys = StringField('עיר מגורים:')
    addresss = StringField('כתובת מגורים:')
    nutritions = SelectField('תזונה', choices = [('בחר/י מתוך הרשימה', 'בחר/י מתוך הרשימה'),('צמחוני', 'צמחוני'), ('טבעוני', 'טבעוני'), ('אוכל כל', 'אוכל כל')])
    phonenums = StringField('מספר טלפון נייד:')
    schoolname = StringField('שם בית הספר:')
    dateaddeds = StringField('Current Date:')
    statuss = StringField('סטטוס פעילות:')
    parents = StringField('יחסים עם המשפחה:')
    details = StringField('פרטים נוספים:')


    submit = SubmitField('הוספת חניכ.ה')

class AddGroupForm(FlaskForm):

    name = StringField('שם קבוצה:')
    regionorsubject = SelectField('אזור או תחום', choices = [('בחר/י מתוך הרשימה', 'בחר/י מתוך הרשימה'),('צפון', 'צפון'), ('שרון', 'שרון'), ('מרכז', 'מרכז'),('שפלה', 'שפלה'),('דרום', 'דרום'),('תחום טרנס', 'תחום טרנס'),('תחום דתיות', 'תחום דתיות'),('תחום אלואן', 'תחום אלואן'),('תכנית ניר', 'תכנית ניר')])
    city = StringField('עיר הקבוצה:')
    agesingroup = SelectMultipleField('שכבות גיל בקבוצה:', choices=[('ז','ז'), ('ח','ח'), ('ט','ט'),('י','י'),('יא','יא'),('יב','יב')])


    #להכניס נתונים קבועים לתוך הגילאים ולהתאים כאן את הערכים
    submit = SubmitField('הוספה')


class DelForm(FlaskForm):

    student_emails = StringField('דוא״ל להסרה:')
    submit = SubmitField('הסרה')

class DelGroupForm(FlaskForm):

    student_in_group_id = StringField('ID of student In Group')
    submit = SubmitField('Remove Student from Group')

class AddStuGroupForm(FlaskForm):

    group_list = list(Group.query.all())
    groups = [(int(g.id), g.name) for g in group_list]

    group_id = SelectField('קבוצה:', choices = groups)
    student_emails = StringField("דואר אלקטרוני: ")
    statusg = SelectField('סטטוס פעילות בקבוצה:', choices = [('פעיל','פעיל'),('לא פעיל','לא פעיל')])
    # stimes = StringField('start time')
    # ftimef = StringField('finish time')
    submit = SubmitField('שיבוץ חניכ.ה בקבוצה')

class NewCondidateForm(FlaskForm):
#לשנות לסלקט ולא לסטרינג ולדאוג שהמשתמש יבחר קבוצה ויוזן איי די.
    #group_id = StringField('ID of Group that you want to assign')
    group_list = list(Group.query.all())
    groups = [(int(g.id), g.name) for g in group_list]

    group_id = SelectField('קבוצה:', choices = groups)
    emailc = StringField("אימייל: ")
    pronounc = SelectField('לשון פניה', choices = [('בחר/י מתוך הרשימה', 'בחר/י מתוך הרשימה'),('את', 'את'), ('אתה', 'אתה'), ('מעורבת', 'מעורבת')])
    phonenumc = StringField('מספר טלפון:')
    text = StringField('תיאור הטיפול:')
    status = SelectField('סטטוס הפניה:', choices = [('',''),('בטיפול','בטיפול '),('טופל','טופל ')])
    firstname = StringField('שם פרטי:')
    lastname = StringField('שם משפחה:')

    # stimes = StringField('start time')
    submit = SubmitField('שלח')

class AddVolunteerForm(FlaskForm):
    IDV = StringField('ת״ז מתנדב.ת:')
    emailv = StringField("אימייל: ")
    FnameV = StringField('שם פרטי:')
    SnameV = StringField('שם משפחה:')
    DateOfBirthV = StringField('תאריך לידה:')
    PronounsV = SelectField('לשון פניה', choices = [('בחר/י מתוך הרשימה', 'בחר/י מתוך הרשימה'),('את', 'את'), ('אתה', 'אתה'), ('מעורבת', 'מעורבת')])
    CityV = StringField('עיר מגורים:')
    AdressV = StringField('כתובת:')
    NutritionV = SelectField('הרגלי תזונה', choices = [('בחר/י מתוך הרשימה', 'בחר/י מתוך הרשימה'),('צמחוני', 'צמחוני'), ('טבעוני', 'טבעוני'), ('אוכל כל', 'אוכל כל')])
    PhoneNumV = StringField('מספר נייד:')
    StatusV = SelectField('סטטוס', choices = [('בחר/י מתוך הרשימה', 'בחר/י מתוך הרשימה'),('פעיל', 'פעיל'), ('לא פעיל', 'לא פעיל'), ('הודח ', 'הודח  ')])
    submit = SubmitField('הוספה')

class VolunteersInGroupsForm(FlaskForm):
    group_list = list(Group.query.all())
    groups = [(g.id, g.name) for g in group_list]
    IDV = StringField('ת״ז מתנדב.ת:')
    IDG = SelectField('קבוצה:', choices = groups)
    emailc = StringField("אימייל: ")
    #TimeS = StringField('Current Date:')
    TimeF = StringField('Current Date:')
    statusV = SelectField('סטטוס פעילות בקבוצה:', choices = [('פעיל','פעיל'),('לא פעיל','לא פעיל')])

    submit = SubmitField('הוספה')

class VolunteerDocumentsForm(FlaskForm):
    IDV = StringField('ת״ז מתנדב.ת:')
    Dname = SelectField('שם המסמך:', choices = [('אחר', 'אחר'),('אישור משטרה', 'אישור משטרה'), ('תעודת זהות', 'תעודת זהות'), (' מסמכי מתנדב', ' מסמכי מתנדב')])
    DocDescription = StringField('תיאור המסמך:')
    Document = FileField('Document')

    submit = SubmitField(' העלה מסמך  (:')

class VolunteersInPossForm(FlaskForm):
    poss_list = list(Poss.query.all())
    posss = [(p.IDP, p.PossName) for p in poss_list]

    IDV = StringField('ת״ז מתנדב.ת:')
    IDP = SelectField('תפקיד בארגון:', choices = posss )
    Statusvp = SelectField('סטטוס פעילות בתפקיד:', choices = [('פעיל','פעיל'),('לא פעיל','לא פעיל')])

    submit = SubmitField(' שייך תפקיד למתנדב (:')

class AddPossForm(FlaskForm):
    IDP = StringField('ID of the Poss:')
    PossName = StringField('תפקיד בארגון:')
    PossDescription = StringField('תיאור התפקיד:')
    #AddTime = StringField('Current Date:')
    
    submit = SubmitField('הוספה')
    
class MeetingsForm(FlaskForm):
    group_list = list(Group.query.all())
    groups = [(int(g.id), g.name) for g in group_list]

    student_list = list(Student.query.all())
    students = [(str(g.emails), g.firstname) for g in student_list]

    

    IDG = SelectField('קבוצה:', choices = groups)
    Mdate = StringField('תאריך:')
    Mtime = StringField('שעת התחלת המפגש:')
    Occurence = SelectField('סטטס פגישה?', choices = [('בוטל','בוטל'),('בוצע','בוצע')])
    Platform = SelectField('סוג פגישה:', choices = [('פרונטאלי','פרונטאלי'),('מקוון','מקוון')])
    Rate = SelectField('דרוג:', choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Pros = StringField('נקודות לשימור:')
    Cons = StringField('נקודות לשיפור:')
    attending = SelectMultipleField('נוכחות חניכימ.ות:', choices = students)
    title = StringField('נושא הפעולה/סיבת הביטול:')
    TheFile = FileField('מסמך:')

    submit = SubmitField('צור פגישה')


 
class MessageForme(FlaskForm):
    #idv_list = list(Volunteers.query.all())
   #idvs = [(v.IDV,v.FnameV) for v in idv_list]
 
    #IDV = SelectField('ID Volunteer:', choices = idvs)
    IDV = StringField('ת״ז כותב ההודעה:')
    Content = TextAreaField('תוכן ההודעה:', widget=TextArea())
    submit = SubmitField('פרסם הודעה למדריכים')



class MFileForm(FlaskForm):
    IDM = StringField('מזהה פגישה:') 
    FileName = StringField('שם הקובץ:') 
    FileDescription = StringField('תאור הקובץ:')
    TheFile = FileField('מסמך:')

    submit = SubmitField('העלה קובץ')
