from myproject.forms import LoginForm, RegistrationForm, AddForm , DelForm, AddGroupForm, AddStuGroupForm, AddAgeGroupForm, NewCondidateForm, DelGroupForm, AddVolunteerForm, VolunteersInGroupsForm, VolunteerDocumentsForm, AddPossForm, MeetingsForm, MFileForm, VolunteersInPossForm, StudentsInMeetingForm 
from flask import render_template, redirect, request, url_for, flash,abort
from flask_login import login_user,login_required,logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from myproject.models import Student, User, Group, StudentInGroup, AgesInGroup, Condidate, VolunteerDocuments, VolunteersInPoss, MFile, Volunteers, Poss, VolunteersInGroups, Meetings, StudentsInMeeting   
from myproject import app,db
from datetime import date
#from flask_uploads import configure_uploads,IMAGES,UploadSet
from werkzeug import secure_filename,FileStorage
from flask_uploads import configure_uploads, IMAGES, UploadSet

app.config['SECRET_KEY'] = 'any secret string'
app.config['UPLOADED_IMAGES_DEST'] = 'uploads/images'

images = UploadSet('images',IMAGES)
configure_uploads(app,images)

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
        pronounc = form.pronounc.data
        phonenumc = form.phonenumc.data
        stimes = date.today()

        # Add new group to database
        new_con = Condidate(group_id,emailc,pronounc,phonenumc,stimes)

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

        #group_id_3 = Group.query.filter_by(id =form.group_id.data).all()
        #print(group_id_3)
        #print(group_id)

        # Add new group to database
        new_con = Condidate(group_id,emailc,stimes)

        db.session.add(new_con)

        db.session.commit()


        return redirect(url_for('list_condidate'))
    return render_template('condidate_mang.html',form=form,condidates_list=condidates_list)

#read with filter:  students = Student.query.filter_by(citys = 'Ramat Gan').all()


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

@app.route('/delete_student_gru', methods=['GET', 'POST'])
def delete_student_gru1():
    groups_list = StudentInGroup.query.all()

    form = DelGroupForm()

    if form.validate_on_submit():
        id1 = form.student_in_group_id.data
        
        gru = StudentInGroup.query.get(id1)
        gru.ftimef = date.today()
        db.session.add(gru)
        db.session.commit()

        return redirect(url_for('list_stu'))
    return render_template('delete_student_gru.html',groups_list=groups_list,form=form)



#student in group list (can use for anything!)
@app.route('/QA')
def Check():
    studentsingroup_list = StudentInGroup.query.all()
    studentsingroup_list2 = StudentInGroup.query.filter_by(group_id = '1').all()

    return render_template('QA.html',studentsingroup_list=studentsingroup_list,studentsingroup_list2=studentsingroup_list2)


@app.route('/Thank_you')
def Thank_you():
    # Grab a list of students from database.
    return render_template('Thank_you.html')

@app.route('/volunteer', methods=['GET', 'POST'])
def add_volunteer():
    volunteers_list = Volunteers.query.all()
    form = AddVolunteerForm()

    if form.validate_on_submit():
        
        IDV = form.IDV.data
        FnameV = form.FnameV.data
        SnameV = form.SnameV.data
        DateOfBirthV = form.DateOfBirthV.data
        PronounsV = form.PronounsV.data
        CityV = form.CityV.data
        AdressV = form.AdressV.data
        NutritionV = form.NutritionV.data
        PhoneNumV = form.PhoneNumV.data
        StatusV = form.StatusV.data
        DateAdded = date.today()


        # Add new volunteer to database
        new_volunteer = Volunteers(IDV,FnameV,SnameV,DateOfBirthV,PronounsV,CityV,AdressV,NutritionV,PhoneNumV,StatusV,DateAdded)
        db.session.add(new_volunteer)
        db.session.commit()

        return redirect(url_for('list_volunteers'))

    return render_template('add_volunteer.html',form=form, volunteers_list=volunteers_list)

@app.route('/list_volunteers')
def list_volunteers():
    # Grab a list of Volunteers from database.
    volunteers_list = Volunteers.query.all()
    return render_template('list_volunteers.html',volunteers_list=volunteers_list)

@app.route('/add_poss', methods=['GET', 'POST'])
def add_poss():

    poss_list = Poss.query.all()

    form = AddPossForm()

    if form.validate_on_submit():
        
        PossName = form.PossName.data
        PossDescription = form.PossDescription.data
        AddTime = date.today()
        # Add new poss to database
        new_poss = Poss(PossName,PossDescription,AddTime)
        db.session.add(new_poss)
        db.session.commit()

        return redirect(url_for('list_poss'))
        
    return render_template('add_poss.html',form=form,poss_list=poss_list)

@app.route('/list_poss')
def list_poss():
    # Grab a list of Possitions from database.
    poss = Poss.query.all()
    return render_template('list_poss.html',poss=poss)

@app.route('/volunteer_in_group', methods=['GET', 'POST'])
def volunteer_in_group():

    volunteer_in_group = VolunteersInGroups.query.all()
    group = Group.query.all()
    volunteers_list = Volunteers.query.all()


    form = VolunteersInGroupsForm()

    if form.validate_on_submit():
        
        IDV = form.IDV.data
        IDG = form.IDG.data
        TimeS = date.today()
        TimeF = form.TimeF.data
        # Add new "Volunteers In Groups" to database
        new_volunteer_in_groups = VolunteersInGroups(IDV,IDG,TimeS,TimeF)
        db.session.add(new_volunteer_in_groups)
        db.session.commit()

        return redirect(url_for('volunteer_in_group'))
        
    return render_template('volunteer_in_group.html',form=form,volunteer_in_group=volunteer_in_group,group=group,volunteers_list=volunteers_list)

@app.route('/volunteer_documents',methods=['GET', 'POST'])
def volunteer_documents():
    Dname = VolunteerDocuments.query.all()
    volunteers_list = Volunteers.query.all()

    form = VolunteerDocumentsForm()
    if form.validate_on_submit():
        IDV = form.IDV.data
        Dname = form.Dname.data
        DocDescription = form.DocDescription.data 
        Document = images.save(form.Document.data)
        DateAdded = date.today()
        #aa = form.Document.data
        
        #Document = images.save(form.document.data)

        # Add new "VolunteerDocuments" to database
        volunteer_documents = VolunteerDocuments(IDV,Dname,DocDescription,Document,DateAdded)
        db.session.add(volunteer_documents)
        db.session.commit()

        
        return redirect(url_for('volunteer_documents'))
        
    return render_template('volunteer_documents.html',form=form,Dname=Dname,volunteers_list=volunteers_list)

@app.route('/volunteers_in_poss', methods=['GET', 'POST'])
def volunteers_in_poss():

    volunteers_in_poss = VolunteersInPoss.query.all()
    poss_list = Poss.query.all()
    volunteers_list = Volunteers.query.all()

    form = VolunteersInPossForm()
    if form.validate_on_submit():
        IDV = form.IDV.data
        IDP = form.IDP.data
        TimeS = date.today()
        #TimeF = ''#form.TimeF.data
       

        new_volunteers_in_poss = VolunteersInPoss(IDV,IDP,TimeS)
        db.session.add(new_volunteers_in_poss)
        db.session.commit()
            
        return redirect(url_for('volunteers_in_poss'))

    return render_template('volunteers_in_poss.html',form=form,volunteers_in_poss=volunteers_in_poss,poss_list=poss_list,volunteers_list=volunteers_list)

@app.route('/meetings', methods=['GET', 'POST'])
def meetings():

    group = Group.query.all()
    meetings = Meetings.query.all()

    form = MeetingsForm()

    if form.validate_on_submit():
        Mdate = form.Mdate.data
        Mtime = form.Mtime.data
        IDG = form.IDG.data
        Occurence = form.Occurence.data
        Platform = form.Platform.data
        Rate = form.Rate.data
        Pros = form.Pros.data
        Cons = form.Cons.data
        DateAdded = date.today()       

        new_meetings = Meetings(Mdate,Mtime,IDG,Occurence,Platform,Rate,Pros,Cons,DateAdded)
        db.session.add(new_meetings)
        db.session.commit()
            
        return redirect(url_for('meetings'))

    return render_template('meetings.html',form=form,group=group,meetings=meetings)

@app.route('/meetings_file',methods=['GET', 'POST'])
def meetings_file():

    the_file = MFile.query.all()
    meetings = Meetings.query.all()

    form = MFileForm()
    if form.validate_on_submit():
        IDM = form.IDM.data
        FileName = form.FileName.data
        FileDescription = form.FileDescription.data
        TheFile = images.save(form.TheFile.data)
        AddTime = date.today()

        # Add new "meetings file" to database
        new_meetings_file = MFile(IDM,FileName,FileDescription,TheFile,AddTime)
        db.session.add(new_meetings_file)
        db.session.commit()


        return redirect(url_for('meetings_file'))
        
    return render_template('meetings_file.html',form=form,the_file=the_file,meetings=meetings)




@app.route('/students_in_meeting', methods=['GET', 'POST'])
def students_in_meeting():

    meetings = Meetings.query.all()
    students = Student.query.all()
    students_in_meeting = StudentsInMeeting.query.all()

    form = StudentsInMeetingForm()

    if form.validate_on_submit():
        IDM = form.IDM.data
        EmaillS = form.EmaillS.data
        Attendance = form.Attendance.data

        new_students_in_meeting = StudentsInMeeting(IDM,EmaillS,Attendance)
        db.session.add(new_students_in_meeting)
        db.session.commit()
            
        return redirect(url_for('students_in_meeting'))

    return render_template('students_in_meeting.html',form=form,meetings=meetings,students=students,students_in_meeting=students_in_meeting)



if __name__ == '__main__':
    app.run(debug=True)