from myproject.forms import LoginForm, RegistrationForm, AddForm , DelForm, AddGroupForm, AddStuGroupForm, AddAgeGroupForm,NewCondidateForm,DelGroupForm
from flask import render_template, redirect, request, url_for, flash,abort
from flask_login import login_user,login_required,logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from myproject.models import Student, User, Group, StudentInGroup, AgesInGroup, Condidate
from myproject import app,db
from datetime import date

app.config['SECRET_KEY'] = 'any secret string'

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()
        
        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user.check_password(form.password.data) and user is not None:
            #Log in the user

            login_user(user)
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('welcome_user')

            return redirect(next)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/add', methods=['GET', 'POST'])
def add_stu():
    form = AddForm()

    if form.validate_on_submit():
        new_stu = Student(emails = form.emails.data,
                            firstname = form.firstname.data,
                            lastname = form.lastname.data,
                            dateofbirth = form.dateofbirth.data,
                            pronouns = form.pronouns.data,
                            citys = form.citys.data,
                            addresss = form.addresss.data,
                            nutritions = form.nutritions.data,
                            phonenums = form.phonenums.data,
                            schoolname = form.schoolname.data,
                            dateaddeds = form.dateaddeds.data,
                            statuss = form.statuss.data,
                            parents = form.parents.data,
                            details = form.details.data)


        # Add new Student to database
        db.session.add(new_stu)
        db.session.commit()

        return redirect(url_for('list_stu'))

    return render_template('add.html',form=form)

@app.route('/add_group', methods=['GET', 'POST'])
def add_group():

    form = AddGroupForm()

    if form.validate_on_submit():
        name = form.name.data
        regionorsubject = form.regionorsubject.data
        city = form.city.data
        # Add new group to database
        new_group = Group(name,regionorsubject,city)

        db.session.add(new_group)

        db.session.commit()
        
        return redirect(url_for('list_gru'))
    return render_template('add_group.html',form=form)

@app.route('/new_condidate', methods=['GET', 'POST'])
def new_condidate():
    form = NewCondidateForm()

    if form.validate_on_submit():
        group_id = form.group_id.data
        emailc = form.emailc.data
        stimes = date.today()

        # Add new group to database
        new_con = Condidate(group_id,emailc,stimes)

        db.session.add(new_con)

        db.session.commit()
        
        return redirect(url_for('Thank_you'))
    return render_template('new_condidate.html',form=form)

@app.route('/condidate_mang', methods=['GET', 'POST'])
def condidate_mang():
    condidates_list = Condidate.query.all()
    form = NewCondidateForm()

    if form.validate_on_submit():
        group_id = form.group_id.data
        emailc = form.emailc.data
        stimes = date.today()

        # Add new group to database
        new_con = Condidate(group_id,emailc,stimes)

        db.session.add(new_con)

        db.session.commit()
        
        return redirect(url_for('list_condidate'))
    return render_template('condidate_mang.html',form=form,condidates_list=condidates_list)

@app.route('/list_condidate')
def list_condidate():
    # Grab a list of students from database.
    condidates_list = Condidate.query.all()
    return render_template('list_condidate.html',condidates_list=condidates_list)

@app.route('/add_age_group', methods=['GET', 'POST'])
def add_age_group():

    form = AddAgeGroupForm()

    if form.validate_on_submit():
        age_id = form.age_id.data
        group_id = form.group_id.data

        new_agesingroup = AgesInGroup(age_id,group_id)
        db.session.add(new_agesingroup)
        db.session.commit()

        return redirect(url_for('list_gru'))

    return render_template('add_age_group.html',form=form)

    
@app.route('/student_in_group', methods=['GET', 'POST'])
def student_in_group():
    form = AddStuGroupForm()

    if form.validate_on_submit():
        stimes = date.today()
        ftimef = ''#form.ftimef.data
        student_emails = form.student_emails.data
        group_id = form.group_id.data
        new_studentingroup = StudentInGroup(stimes,ftimef,student_emails,group_id)
        db.session.add(new_studentingroup)
        db.session.commit()
            
        return redirect(url_for('list_stu'))

    return render_template('student_in_group.html',form=form)


@app.route('/list')
def list_stu():
    # Grab a list of students from database.
    students_list = Student.query.all()
    return render_template('list.html',students_list=students_list)

#read with filter:  students = Student.query.filter_by(citys = 'Ramat Gan').all()
#read without filter:     students = Student.query.all()

@app.route('/list-gru')
def list_gru():
    # Grab a list of students from database.
    groups = Group.query.all()
    return render_template('list-gru.html',groups=groups)
    # delete a students from database.


@app.route('/delete', methods=['GET', 'POST'])
def del_stu():
    students_list = Student.query.all()

    form = DelForm()

    if form.validate_on_submit():
        emails = form.student_emails.data
        stu = Student.query.get(emails)
        db.session.delete(stu)
        db.session.commit()

        return redirect(url_for('list_stu'))
    return render_template('delete.html',students_list=students_list,form=form)

@app.route('/delete_gru', methods=['GET', 'POST'])
def del_gru():
    groups_list = Group.query.all()

    form = DelGroupForm()

    if form.validate_on_submit():
        id = form.group_id.data
        gru = Group.query.get(id)
        db.session.delete(gru)
        db.session.commit()

        return redirect(url_for('list_gru'))
    return render_template('delete_gru.html',groups_list=groups_list,form=form)



@app.route('/Thank_you')
def Thank_you():
    # Grab a list of students from database.
    return render_template('Thank_you.html')


if __name__ == '__main__':
    app.run(debug=True)
