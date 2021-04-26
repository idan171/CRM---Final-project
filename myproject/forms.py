from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, RadioField
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

    group_id = StringField('ID of Group')
    submit = SubmitField('Remove Group')

class AddStuGroupForm(FlaskForm):

    group_id = StringField('ID of Group')
    student_emails = StringField("Email of Student: ")
    # stimes = StringField('start time')
    # ftimef = StringField('finish time')
    submit = SubmitField('Add him')

class NewCondidateForm(FlaskForm):

    group_id = StringField('ID of Group that you want to assign')
    emailc = StringField("Email of you: ")
    # stimes = StringField('start time')
    submit = SubmitField('Send')


