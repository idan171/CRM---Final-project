from logging import ERROR

from sqlalchemy.sql.elements import Null
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
from sqlalchemy import or_
from flask import  session


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
        return redirect(url_for('student_in_group'))

    return render_template('add.html',form=form)

@app.route('/edit_stu/<string:emails>', methods=['GET', 'POST'])
def edit_stu(emails):
    students_list = Student.query.all()
    form = AddForm()
    name_to_update = Student.query.get_or_404(emails)
    if request.method == "POST":

        name_to_update.firstname = request.form['firstname']
        name_to_update.lastname = request.form['lastname']
        name_to_update.pronouns = request.form['pronouns']
        name_to_update.citys = request.form['citys']
        name_to_update.addresss = request.form['addresss']
        name_to_update.nutritions = request.form['nutritions']
        name_to_update.phonenums = request.form['phonenums']
        name_to_update.schoolname = request.form['schoolname']
        name_to_update.parents = request.form['parents']
        name_to_update.details = request.form['details']

        try:
            db.session.commit()
            flash("Student Updated Successfully!")
            return render_template("list.html",form=form,name_to_update=name_to_update,students_list=students_list)

        except:
             flash("Error! Looks like there is a problem, please try again!")
             return render_template("edit_stu.html",form=form,name_to_update=name_to_update,students_list=students_list)


    return render_template('edit_stu.html',form=form,name_to_update=name_to_update)



@app.route('/edit_volingroup/<int:id>', methods=['GET', 'POST'])
def edit_volingroup(id):
    vol_in_group_list = VolunteersInGroups.query.join(Group, VolunteersInGroups.IDG==Group.id).join(Volunteers, VolunteersInGroups.IDV==Volunteers.IDV)\
    .add_columns(VolunteersInGroups.IDG,VolunteersInGroups.id, VolunteersInGroups.IDV, VolunteersInGroups.statusV, Group.id, Group.name,VolunteersInGroups.TimeS,VolunteersInGroups.TimeF,Volunteers.IDV,Volunteers.FnameV,Volunteers.SnameV,Volunteers.PronounsV,Volunteers.DateAdded,Volunteers.StatusV )\
    .filter(VolunteersInGroups.IDG == Group.id,VolunteersInGroups.IDV==Volunteers.IDV)
    
    #editvol_in_group_list = VolunteersInGroups.query.all()
    form = VolunteersInGroupsForm()
    volingro_to_update = VolunteersInGroups.query.get_or_404(id)
    if request.method == "POST":
        volingro_to_update.IDG = request.form['IDG']
        volingro_to_update.IDV = request.form['IDV']
        volingro_to_update.statusV = request.form['statusV']
      
        try:
            db.session.commit()
            flash("Student in group Updated Successfully!")
            return render_template("volunteer_in_group.html",form=form,volingro_to_update=volingro_to_update,vol_in_group_list=vol_in_group_list)

        except:
             flash("Error! Looks like there is a problem, please try again!")
             return render_template("edit_volingroup.html",form=form,volingro_to_update=volingro_to_update,vol_in_group_list=vol_in_group_list)


    return render_template('edit_volingroup.html',form=form,volingro_to_update=volingro_to_update)



@app.route('/search_volingroup', methods=['GET', 'POST'])
def search_volingroup():
    if request.method =='POST':
        form2 = request.form
        search_value = form2['volg_string']
        search = "%{0}%".format(search_value)
        results = (VolunteersInGroups.query.join(Group, VolunteersInGroups.IDG==Group.id).join(Volunteers, VolunteersInGroups.IDV==Volunteers.IDV).join(VolunteersInPoss, VolunteersInGroups.IDV==VolunteersInPoss.IDV)\
    .add_columns(VolunteersInGroups.IDG, VolunteersInGroups.IDV, VolunteersInGroups.statusV, Group.id, Group.name,VolunteersInGroups.TimeS,VolunteersInGroups.TimeF,Volunteers.IDV,Volunteers.FnameV,Volunteers.SnameV,Volunteers.PronounsV,Volunteers.DateAdded,Volunteers.StatusV,VolunteersInPoss.IDP)\
    .filter(VolunteersInGroups.IDG == Group.id,VolunteersInGroups.IDV==Volunteers.IDV)).filter(or_(VolunteersInGroups.IDV.like(search),
                                                        Group.name.like(search),
                                                        VolunteersInGroups.statusV.like(search))).all()
        return render_template('list_vol_in_group.html',searchvol_in_group_list=results,legend="Search Results")
    else:
        return redirect('/')






@app.route('/search_stuingroup', methods=['GET', 'POST'])
def search_stuingroup():
    

    
    if request.method =='POST':
        form1 = request.form
        search_value = form1['vol_string']
        search = "%{0}%".format(search_value)
        results = (StudentInGroup.query.join(Group, StudentInGroup.group_id==Group.id)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg )\
        .filter(StudentInGroup.group_id == Group.id)).filter(or_(StudentInGroup.student_emails.like(search),Group.name.like(search),
                                            StudentInGroup.statusg.like(search))).all()
        return render_template('list_stu_in_group.html',searchstu_in_group_list=results,legend="Search Results")
    else:
        return redirect('/')


@app.route('/edit_volunteer/<int:IDV>', methods=['GET', 'POST'])
def edit_volunteer(IDV):
  #  volunteers_poss_list = VolunteersInPoss.query.join(Volunteers, VolunteersInPoss.IDV==Volunteers.IDV).join(Poss, VolunteersInPoss.IDP==Poss.IDP)\
   # .add_columns(VolunteersInPoss.IDP, Poss.PossName, VolunteersInPoss.TimeS, Volunteers.IDV, Volunteers.FnameV, Volunteers.SnameV,Volunteers.StatusV)\
    #.filter(VolunteersInPoss.IDV==Volunteers.IDV,VolunteersInPoss.IDP==Poss.IDP)
    volunteers_poss_list2 = Volunteers.query.join(VolunteersInPoss, Volunteers.IDV==VolunteersInPoss.IDV, isouter=True).join(Poss, VolunteersInPoss.IDP==Poss.IDP,isouter=True)\
    .add_columns(VolunteersInPoss.IDP, VolunteersInPoss.id, Poss.PossName, VolunteersInPoss.TimeS, VolunteersInPoss.Statusvp, Volunteers.IDV, Volunteers.FnameV, Volunteers.SnameV,Volunteers.StatusV)\
   
    volunteers_list = Volunteers.query.all()
    form = AddVolunteerForm()
    vol_to_update = Volunteers.query.get_or_404(IDV)
    if request.method == "POST":
        vol_to_update.FnameV = request.form['FnameV']
        vol_to_update.SnameV = request.form['SnameV']
        vol_to_update.DateOfBirthV = request.form['DateOfBirthV']
        vol_to_update.PronounsV = request.form['PronounsV']
        vol_to_update.CityV = request.form['CityV']
        vol_to_update.AdressV = request.form['AdressV']
        vol_to_update.NutritionV = request.form['NutritionV']
        vol_to_update.PhoneNumV = request.form['PhoneNumV']
        vol_to_update.StatusV = request.form['StatusV']
        try:
            db.session.commit()
            flash("Volunteer Updated Successfully!")
            return render_template("list_volunteers.html",form=form,vol_to_update=vol_to_update,volunteers_list=volunteers_list,volunteers_poss_list2=volunteers_poss_list2)

        except:
             flash("Error! Looks like there is a problem, please try again!")
             return render_template("edit_volunteer.html",form=form,vol_to_update=vol_to_update,volunteers_list=volunteers_list,volunteers_poss_list2=volunteers_poss_list2)


    return render_template('edit_volunteer.html',form=form,vol_to_update=vol_to_update)


@app.route('/edit_poss/<int:id>', methods=['GET', 'POST'])
def edit_poss(id):
    volunteers_poss_list2 = Volunteers.query.join(VolunteersInPoss, Volunteers.IDV==VolunteersInPoss.IDV, isouter=True).join(Poss, VolunteersInPoss.IDP==Poss.IDP,isouter=True)\
    .add_columns(VolunteersInPoss.IDP, VolunteersInPoss.id, Poss.PossName, VolunteersInPoss.TimeS, VolunteersInPoss.Statusvp, Volunteers.IDV, Volunteers.FnameV, Volunteers.SnameV,Volunteers.StatusV)\
   
    volunteers_poss = VolunteersInPoss.query.all()
    form = VolunteersInPossForm()
    pos_to_update = VolunteersInPoss.query.get_or_404(id)
    if request.method == "POST":
        pos_to_update.IDP = request.form['IDP']
        pos_to_update.Statusvp = request.form['Statusvp']
   
        try:
            db.session.commit()
            flash("Volunteer Updated Successfully!")
            return render_template("list_volunteers.html",form=form,pos_to_update=pos_to_update,volunteers_poss_list2=volunteers_poss_list2,volunteers_poss=volunteers_poss)

        except:
             flash("Error! Looks like there is a problem, please try again!")
             return render_template("edit_poss.html",form=form,pos_to_update=pos_to_update,volunteers_poss_list2=volunteers_poss_list2,volunteers_poss=volunteers_poss)


    return render_template('edit_poss.html',form=form,pos_to_update=pos_to_update)




@app.route('/add_group', methods=['GET', 'POST'])
def add_group():

    form = AddGroupForm()

    if form.validate_on_submit():
        name = form.name.data
        regionorsubject = form.regionorsubject.data
        city = form.city.data
        # Add new group to database
        exists = Group.query.filter_by(name=name, regionorsubject=regionorsubject).first()
        if exists: 
            print (ERROR)
        if not exists: 
            new_group = Group(name,regionorsubject,city)
            db.session.add(new_group)
            db.session.commit()
        return redirect(url_for('list_gru'))
    return render_template('add_group.html',form=form)



@app.route('/new_condidate', methods=['GET', 'POST'])
def new_condidate():
    form = NewCondidateForm()

    if form.is_submitted():
        form.group_id.data = int(form.group_id.data)
        if form.validate():
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

    if form.is_submitted():
        form.group_id.data = int(form.group_id.data)
        if form.validate():
            group_id = form.group_id.data
            emailc = form.emailc.data
            pronounc = form.pronounc.data
            phonenumc = form.phonenumc.data
            stimes = date.today()

            #group_id_3 = Group.query.filter_by(id =form.group_id.data).all()
            #print(group_id_3)
            #print(group_id)

            # Add new group to database
            new_con = Condidate(group_id,emailc,stimes,pronounc,phonenumc)

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
    groups = Group.query.all()

    stu_in_group_list = StudentInGroup.query.join(Group, StudentInGroup.group_id==Group.id)\
    .add_columns(StudentInGroup.group_id,StudentInGroup.student_emails,StudentInGroup.id, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg )\
    .filter(StudentInGroup.group_id == Group.id)
    #.paginate(page, 1, False)

    form = AddStuGroupForm()
    
    if form.is_submitted():
        form.group_id.data = int(form.group_id.data)
        if form.validate():
            stimes = date.today()
            ftimef = ''#form.ftimef.data
            student_emails = form.student_emails.data
            group_id = form.group_id.data
            statusg = form.statusg.data
            
            new_studentingroup = StudentInGroup(stimes,ftimef,student_emails,group_id,statusg)
            db.session.add(new_studentingroup)
            db.session.commit()
            print('added')
                
            return redirect(url_for('student_in_group'))

    return render_template('student_in_group.html',form=form,stu_in_group_list=stu_in_group_list,groups=groups)

@app.route('/list_stu_in_group')
def list_stu_in_group():
    # Grab a list of students from database.
    stu_in_group_list = StudentInGroup.query.all()
    searchstu_in_group_list = StudentInGroup.query.join(Group, StudentInGroup.group_id==Group.id)\
    .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg )\
    .filter(StudentInGroup.group_id == Group.id)
    return render_template('list_stu_in_group.html',stu_in_group_list=stu_in_group_list,searchstu_in_group_list=searchstu_in_group_list)


@app.route('/edit_stuingroup/<int:id>', methods=['GET', 'POST'])
def edit_stuingroup(id):
    stu_in_group_list = StudentInGroup.query.join(Group, StudentInGroup.group_id==Group.id)\
    .add_columns(StudentInGroup.group_id,StudentInGroup.student_emails,StudentInGroup.id, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg )\
    .filter(StudentInGroup.group_id == Group.id)

    form = AddStuGroupForm()
    line_to_update = StudentInGroup.query.get_or_404(id)
    if request.method == "POST":
        line_to_update.group_id = request.form['group_id']
        line_to_update.student_emails = request.form['student_emails']
        line_to_update.statusg = request.form['statusg']

        try:
            db.session.commit()
            flash("Student in Group Updated Successfully!")
            return render_template("student_in_group.html",form=form,line_to_update=line_to_update,stu_in_group_list=stu_in_group_list)

        except:
             flash("Error! Looks like there is a problem, please try again!")
             return render_template("edit_stuingroup.html",form=form,line_to_update=line_to_update,stu_in_group_list=stu_in_group_list)


    return render_template('edit_stuingroup.html', form=form,line_to_update=line_to_update)

@app.route('/list')
def list_stu():
    # Grab a list of students from database.
    students_list = Student.query.all()
    return render_template('list.html',students_list=students_list)

#read with filter:  students = Student.query.filter_by(citys = 'Ramat Gan').all()
#read without filter:     students = Student.query.all()

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method =='POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        results = Student.query.filter(or_(Student.firstname.like(search),
                                            Student.phonenums.like(search))).all()
        return render_template('list.html',students_list=results,legend="Search Results")
    else:
        return redirect('/')

        # חיפוש רק לפי שדה אחד. בדוגמא למעלה זה חיפוש בכמה שדות
        #results = Student.query.filter(Student.firstname.like(search)).all()
@app.route('/search_volunteer', methods=['GET', 'POST'])
def search_volunteer():
    if request.method =='POST':
        form = request.form
        search_value = form['vol_string']
        search = "%{0}%".format(search_value)
        results = (Volunteers.query.join(VolunteersInPoss, Volunteers.IDV==VolunteersInPoss.IDV, isouter=True).join(Poss, VolunteersInPoss.IDP==Poss.IDP,isouter=True)\
    .add_columns(VolunteersInPoss.IDP,VolunteersInPoss.id, Poss.PossName, VolunteersInPoss.TimeS,VolunteersInPoss.Statusvp, Volunteers.IDV, Volunteers.FnameV, Volunteers.SnameV,Volunteers.StatusV)).filter(or_(Volunteers.FnameV.like(search),
                                            Volunteers.SnameV.like(search),
                                            Poss.PossName.like(search),
                                            VolunteersInPoss.Statusvp.like(search),
                                            Volunteers.IDV.like(search),
                                            Volunteers.CityV.like(search))).all()
        return render_template('list_volunteers.html',volunteers_poss_list2=results,legend="Search Results")
    else:
        return redirect('/')


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

    volunteers_poss_list2 = Volunteers.query.join(VolunteersInPoss, Volunteers.IDV==VolunteersInPoss.IDV, isouter=True).join(Poss, VolunteersInPoss.IDP==Poss.IDP,isouter=True)\
    .add_columns(VolunteersInPoss.IDP, VolunteersInPoss.id, Poss.PossName, VolunteersInPoss.TimeS, VolunteersInPoss.Statusvp, Volunteers.IDV, Volunteers.FnameV, Volunteers.SnameV,Volunteers.StatusV)\
    # .filter(Volunteers.IDV==VolunteersInPoss.IDV)

    #volunteers_poss_list = VolunteersInPoss.query.join(Volunteers, VolunteersInPoss.IDV==Volunteers.IDV).join(Poss, VolunteersInPoss.IDP==Poss.IDP)\
    #.add_columns(VolunteersInPoss.IDP, Poss.PossName, VolunteersInPoss.TimeS, Volunteers.IDV, Volunteers.FnameV, Volunteers.SnameV,Volunteers.StatusV)\
    #.filter(VolunteersInPoss.IDV==Volunteers.IDV,VolunteersInPoss.IDP==Poss.IDP)

    searchvol_in_group_list = VolunteersInGroups.query.join(Group, VolunteersInGroups.IDG==Group.id).join(Volunteers, VolunteersInGroups.IDV==Volunteers.IDV).join(VolunteersInPoss, VolunteersInGroups.IDV==VolunteersInPoss.IDV)\
    .add_columns(VolunteersInGroups.IDG, VolunteersInGroups.IDV, VolunteersInGroups.statusV, Group.id, Group.name,VolunteersInGroups.TimeS,VolunteersInGroups.TimeF,Volunteers.IDV,Volunteers.FnameV,Volunteers.SnameV,Volunteers.PronounsV,Volunteers.DateAdded,Volunteers.StatusV,VolunteersInPoss.IDP )\
    .filter(VolunteersInGroups.IDG == Group.id,VolunteersInGroups.IDV==Volunteers.IDV)
    return render_template('list_volunteers.html',volunteers_list=volunteers_list,searchvol_in_group_list=searchvol_in_group_list,volunteers_poss_list2=volunteers_poss_list2)

@app.route('/add_poss', methods=['GET', 'POST'])
def add_poss():

    poss_list = Poss.query.all()

    form = AddPossForm()

    if form.validate_on_submit():
        PossName = form.PossName.data
        PossDescription = form.PossDescription.data
        AddTime = date.today()
        exists = Poss.query.filter_by(PossName=PossName).first()
        if exists: 
            print (ERROR)
        # Add new poss to database
        if not exists: 
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
    
    vol_in_group_list = VolunteersInGroups.query.join(Group, VolunteersInGroups.IDG==Group.id).join(Volunteers, VolunteersInGroups.IDV==Volunteers.IDV)\
    .add_columns(VolunteersInGroups.IDG, VolunteersInGroups.IDV, VolunteersInGroups.statusV, Group.id, Group.name,VolunteersInGroups.TimeS,VolunteersInGroups.TimeF,Volunteers.IDV,Volunteers.FnameV,Volunteers.SnameV,Volunteers.PronounsV,Volunteers.DateAdded,Volunteers.StatusV )\
    .filter(VolunteersInGroups.IDG == Group.id,VolunteersInGroups.IDV==Volunteers.IDV)
   
    vol_in_group_list2 = Volunteers.query.join(VolunteersInGroups, Volunteers.IDV==VolunteersInGroups.IDV, isouter=True).join(VolunteersInPoss, Volunteers.IDV==VolunteersInPoss.IDV, isouter=True)\
    .add_columns(VolunteersInGroups.IDG, VolunteersInGroups.TimeS,VolunteersInGroups.TimeF,Volunteers.IDV,VolunteersInPoss.IDP,VolunteersInPoss.Statusvp,Volunteers.FnameV,Volunteers.SnameV,Volunteers.PronounsV,Volunteers.DateAdded,Volunteers.CityV,Volunteers.PhoneNumV,Volunteers.StatusV )\
    .filter(VolunteersInGroups.IDG == None, VolunteersInPoss.IDP == 1, VolunteersInPoss.Statusvp == 'פעיל',Volunteers.StatusV == 'פעיל')


    form = VolunteersInGroupsForm()

    if form.is_submitted():
        form.IDG.data = int(form.IDG.data)
        if form.validate():        
            IDV = form.IDV.data
            IDG = form.IDG.data
            TimeS = date.today()
            TimeF = form.TimeF.data
            statusV = form.statusV.data
            # Add new "Volunteers In Groups" to database
            new_volunteer_in_groups = VolunteersInGroups(IDV,IDG,TimeS,TimeF,statusV)
            db.session.add(new_volunteer_in_groups)
            db.session.commit()

            return redirect(url_for('volunteer_in_group'))
        
    return render_template('volunteer_in_group.html',form=form,volunteer_in_group=volunteer_in_group,group=group,volunteers_list=volunteers_list,vol_in_group_list=vol_in_group_list,vol_in_group_list2=vol_in_group_list2)



@app.route('/list_vol_in_group')
def list_vol_in_group():
    # Grab a list of students from database.
    vol_in_group_list = VolunteersInGroups.query.all()
    searchvol_in_group_list = VolunteersInGroups.query.join(Group, VolunteersInGroups.IDG==Group.id).join(Volunteers, VolunteersInGroups.IDV==Volunteers.IDV).join(VolunteersInPoss, VolunteersInGroups.IDV==VolunteersInPoss.IDV)\
    .add_columns(VolunteersInGroups.IDG, VolunteersInGroups.IDV, VolunteersInGroups.statusV, Group.id, Group.name,VolunteersInGroups.TimeS,VolunteersInGroups.TimeF,Volunteers.IDV,Volunteers.FnameV,Volunteers.SnameV,Volunteers.PronounsV,Volunteers.DateAdded,Volunteers.StatusV,VolunteersInPoss.IDP )\
    .filter(VolunteersInGroups.IDG == Group.id,VolunteersInGroups.IDV==Volunteers.IDV)
    return render_template('list_vol_in_group.html',vol_in_group_list=vol_in_group_list,searchvol_in_group_list=searchvol_in_group_list)

    volunteers_group_list2 = (Volunteers.query.join(VolunteersInPoss, Volunteers.IDV==VolunteersInPoss.IDV, isouter=True)\
    .add_columns(VolunteersInPoss.IDP, VolunteersInPoss.TimeS, VolunteersInPoss.id, Volunteers.IDV, Volunteers.PronounsV, Volunteers.FnameV, Volunteers.SnameV,Volunteers.DateAdded,Volunteers.PhoneNumV)).filter_by(IDP = None).all() 

@app.route('/volunteer_documents',methods=['GET', 'POST'])
def volunteer_documents():
    Dname = VolunteerDocuments.query.all()
    volunteers_list = Volunteers.query.all()
    volunteer_and_doc = Volunteers.query.join(VolunteerDocuments, Volunteers.IDV==VolunteerDocuments.IDV, isouter=True)\
    .add_columns(Volunteers.IDV, Volunteers.FnameV, Volunteers.SnameV, Volunteers.StatusV, VolunteerDocuments.Dname,VolunteerDocuments.Document,VolunteerDocuments.DateAdded)\
    #.filter(Volunteers.IDV == VolunteerDocuments.IDV,VolunteersInGroups.IDV==Volunteers.IDV)

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
        
    return render_template('volunteer_documents.html',form=form,Dname=Dname,volunteers_list=volunteers_list,volunteer_and_doc=volunteer_and_doc)


@app.route('/search_doc', methods=['GET', 'POST'])
def search_doc():
    if request.method =='POST':
        form3 = request.form2
        search_value = form3['doc_string']
        search = "%{0}%".format(search_value)
        results = Volunteers.query.join(VolunteerDocuments, Volunteers.IDV==VolunteerDocuments.IDV, isouter=True)\
    .add_columns(Volunteers.IDV, Volunteers.FnameV, Volunteers.SnameV, Volunteers.StatusV, VolunteerDocuments.Dname,VolunteerDocuments.Document,VolunteerDocuments.DateAdded).filter(or_(VolunteerDocuments.Dname.like(search),
                                                        Volunteers.IDV.like(search))).all()
                                                       
        return render_template('volunteer_documents.html',volunteer_and_doc=results,legend="Search Results")
    else:
        return redirect('/')




@app.route('/volunteers_in_poss', methods=['GET', 'POST'])
def volunteers_in_poss():

    volunteers_in_poss = VolunteersInPoss.query.all()
    poss_list = Poss.query.all()
    volunteers_list = Volunteers.query.all()
    print ('YESS1')

    volunteers_poss_list2 = (Volunteers.query.join(VolunteersInPoss, Volunteers.IDV==VolunteersInPoss.IDV, isouter=True)\
    .add_columns(VolunteersInPoss.IDP, VolunteersInPoss.TimeS, VolunteersInPoss.id, Volunteers.IDV, Volunteers.PronounsV, Volunteers.FnameV, Volunteers.SnameV,Volunteers.DateAdded,Volunteers.PhoneNumV)).filter_by(IDP = None).all() 
    if volunteers_poss_list2: 
        print ('YESS2')
    if not volunteers_poss_list2: 
        print ('YESS3')

    form = VolunteersInPossForm()

    if form.is_submitted():
        form.IDP.data = int(form.IDP.data)
        if form.validate():
            IDV = form.IDV.data
            IDP = form.IDP.data
            TimeS = date.today()
            #TimeF = ''#form.TimeF.data
            Statusvp = form.Statusvp.data
         
            exists = VolunteersInPoss.query.filter_by(IDV=IDV, IDP=IDP, Statusvp='פעיל' ).first()
            if exists: 
                print (ERROR)
            if not exists: 
                new_volunteers_in_poss = VolunteersInPoss(IDV,IDP,TimeS,Statusvp)
                db.session.add(new_volunteers_in_poss)
                db.session.commit()
        
                return redirect(url_for('volunteers_in_poss'))

    return render_template('volunteers_in_poss.html',form=form,volunteers_in_poss=volunteers_in_poss,poss_list=poss_list,volunteers_list=volunteers_list,volunteers_poss_list2=volunteers_poss_list2)



@app.route('/addmeetings', methods=['GET', 'POST'])
def addmeetings():

    meetings2 = Meetings.query.all()

    form = MeetingsForm()

    if form.is_submitted():
        form.IDG.data = int(form.IDG.data)
        if form.validate():
            new_meeting = Meetings(Mdate = form.Mdate.data,
            Mtime = form.Mtime.data,
            IDG = form.IDG.data,
            Occurence = form.Occurence.data,
            Platform = form.Platform.data,
            Rate = form.Rate.data,
            Pros = form.Pros.data,
            Cons = form.Cons.data,
            DateAdded = date.today())


            # Add new Student to database
            db.session.add(new_meeting)
            db.session.commit()
            return redirect(url_for('meetings_file'))

    return render_template('meetings.html',form=form,meetings2=meetings2)


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


@app.route('/management_dashbord')
def management_dashbord():
    guides = VolunteersInPoss.query.filter_by(IDP='1').count()
    writers = VolunteersInPoss.query.filter_by(IDP='2').count()
    educations = VolunteersInPoss.query.filter_by(IDP='3').count()
    activation = VolunteersInPoss.query.filter_by(IDP='4').count()
    waiting = VolunteersInPoss.query.filter_by(IDP='5').count()

    zafon = (StudentInGroup.query.join(Group, StudentInGroup.group_id==Group.id)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.group_id == Group.id)).filter_by(regionorsubject='צפון').count()
    zafon2 = (Group.query.join(StudentInGroup, Group.id==StudentInGroup.group_id, isouter=True)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.statusg=='לא פעיל',Group.regionorsubject=='צפון')).count()
    zafon3 = (Group.query.join(StudentInGroup, Group.id==StudentInGroup.group_id, isouter=True)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.statusg!='לא פעיל',Group.regionorsubject=='צפון')).count()
    print (zafon2)
    sharon = (StudentInGroup.query.join(Group, StudentInGroup.group_id==Group.id)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.group_id == Group.id)).filter_by(regionorsubject='שרון').count()
    sharon2 = (Group.query.join(StudentInGroup, Group.id==StudentInGroup.group_id, isouter=True)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.statusg=='לא פעיל',Group.regionorsubject=='שרון')).count()
    sharon3 = (Group.query.join(StudentInGroup, Group.id==StudentInGroup.group_id, isouter=True)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.statusg!='לא פעיל',Group.regionorsubject=='שרון')).count()
    merkaz = (StudentInGroup.query.join(Group, StudentInGroup.group_id==Group.id)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.group_id == Group.id)).filter_by(regionorsubject='מרכז').count()
    merkaz2 = (Group.query.join(StudentInGroup, Group.id==StudentInGroup.group_id, isouter=True)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.statusg=='לא פעיל',Group.regionorsubject=='מרכז')).count()
    merkaz3 = (Group.query.join(StudentInGroup, Group.id==StudentInGroup.group_id, isouter=True)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.statusg!='לא פעיל',Group.regionorsubject=='מרכז')).count()
    shfela = (StudentInGroup.query.join(Group, StudentInGroup.group_id==Group.id)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.group_id == Group.id)).filter_by(regionorsubject='שפלה').count()
    shfela2 = (Group.query.join(StudentInGroup, Group.id==StudentInGroup.group_id, isouter=True)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.statusg=='לא פעיל',Group.regionorsubject=='שפלה')).count()
    shfela3 = (Group.query.join(StudentInGroup, Group.id==StudentInGroup.group_id, isouter=True)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.statusg!='לא פעיל',Group.regionorsubject=='שפלה')).count()
    darom = (StudentInGroup.query.join(Group, StudentInGroup.group_id==Group.id)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.group_id == Group.id)).filter_by(regionorsubject='דרום').count()
    darom2 = (Group.query.join(StudentInGroup, Group.id==StudentInGroup.group_id, isouter=True)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.statusg=='לא פעיל',Group.regionorsubject=='דרום')).count()
    darom3 = (Group.query.join(StudentInGroup, Group.id==StudentInGroup.group_id, isouter=True)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.statusg!='לא פעיל',Group.regionorsubject=='דרום')).count()
    trans = (StudentInGroup.query.join(Group, StudentInGroup.group_id==Group.id)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.group_id == Group.id)).filter_by(regionorsubject='תחום טרנס').count()
    trans2 = (Group.query.join(StudentInGroup, Group.id==StudentInGroup.group_id, isouter=True)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.statusg=='לא פעיל',Group.regionorsubject=='תחום טרנס')).count()
    trans3 = (Group.query.join(StudentInGroup, Group.id==StudentInGroup.group_id, isouter=True)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.statusg!='לא פעיל',Group.regionorsubject=='תחום טרנס')).count()
    datiot = (StudentInGroup.query.join(Group, StudentInGroup.group_id==Group.id)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.group_id == Group.id)).filter_by(regionorsubject='תחום דתיות').count()
    datiot2 = (Group.query.join(StudentInGroup, Group.id==StudentInGroup.group_id, isouter=True)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.statusg=='לא פעיל',Group.regionorsubject=='תחום דתיות')).count()
    datiot3 = (Group.query.join(StudentInGroup, Group.id==StudentInGroup.group_id, isouter=True)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.statusg!='לא פעיל',Group.regionorsubject=='תחום דתיות')).count()
    allwan = (StudentInGroup.query.join(Group, StudentInGroup.group_id==Group.id)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.group_id == Group.id)).filter_by(regionorsubject='תחום אלואן').count()
    allwan2 = (Group.query.join(StudentInGroup, Group.id==StudentInGroup.group_id, isouter=True)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.statusg=='לא פעיל',Group.regionorsubject=='תחום אלואן')).count()
    allwan3 = (Group.query.join(StudentInGroup, Group.id==StudentInGroup.group_id, isouter=True)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.statusg!='לא פעיל',Group.regionorsubject=='תחום אלואן')).count()
    nir = (StudentInGroup.query.join(Group, StudentInGroup.group_id==Group.id)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.group_id == Group.id)).filter_by(regionorsubject='תכנית ניר').count()
    nir2 = (Group.query.join(StudentInGroup, Group.id==StudentInGroup.group_id, isouter=True)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.statusg=='לא פעיל',Group.regionorsubject=='תכנית ניר')).count()
    nir3 = (Group.query.join(StudentInGroup, Group.id==StudentInGroup.group_id, isouter=True)\
        .add_columns(StudentInGroup.group_id, StudentInGroup.student_emails, StudentInGroup.statusg, Group.id, Group.name,StudentInGroup.stimes,StudentInGroup.ftimef, StudentInGroup.statusg,Group.regionorsubject)\
        .filter(StudentInGroup.statusg!='לא פעיל',Group.regionorsubject=='תכנית ניר')).count()
    return render_template('management_dashbord.html',guides=guides,writers=writers,educations=educations,activation=activation,waiting=waiting,zafon=zafon,sharon=sharon,merkaz=merkaz,shfela=shfela,darom=darom,trans=trans,datiot=datiot,allwan=allwan,nir=nir,zafon2=zafon2,sharon2=sharon2,merkaz2=merkaz2,shfela2=shfela2,darom2=darom2,trans2=trans2,datiot2=datiot2,allwan2=allwan2,nir2=nir2,zafon3=zafon3,sharon3=sharon3,merkaz3=merkaz3,shfela3=shfela3,darom3=darom3,trans3=trans3,datiot3=datiot3,allwan3=allwan3,nir3=nir3)

    

if __name__ == '__main__':
    app.run(debug=True)

