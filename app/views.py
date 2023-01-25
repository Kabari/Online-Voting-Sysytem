from app import app
from .models import VotesModel,CandidateModel, UserModel,db
from flask import redirect, render_template, flash,url_for,request
from flask_login import login_required, current_user,logout_user
from flask_cors import cross_origin
import string
import json
import random


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/profile")
@login_required
def profile():
    prez = CandidateModel.query.filter_by(post="President").all()
    vice = CandidateModel.query.filter_by(post="Vice-President").all()
    sec_gen = CandidateModel.query.filter_by(post="Secretary-General").all()
    trez = CandidateModel.query.filter_by(post="Treasurer").all()
    fin_sec = CandidateModel.query.filter_by(post="Financial-Secretary").all()
    voter = VotesModel.query.filter_by(mat_no=current_user.mat_no).first()
    return render_template("profile.html",name=current_user.name,prez=prez,vice=vice,sec_gen=sec_gen,trez=trez,fin_sec=fin_sec,voter=voter)

@app.route("/profile", methods=["POST"])
def post_vote():
    president = request.form.get('president')
    vicepresident = request.form.get('vice-president')
    secretarygeneral = request.form.get('secretary-general')
    treasurer = request.form.get('treasurer')
    financialsecretary = request.form.get('financial-secretary')

    voted = VotesModel.query.filter_by(mat_no=current_user.mat_no).first()
    if not voted:
        voter = VotesModel(mat_no=current_user.mat_no,voter_id=current_user.id,post_1=int(president),post_2=int(vicepresident),post_3=int(secretarygeneral), post_4=int(treasurer), post_5=int(financialsecretary))
        db.session.add(voter)
        db.session.commit()
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('profile'))
    

@app.route("/candidate")
def candidate():
    prez = CandidateModel.query.filter_by(post="President").all()
    vice = CandidateModel.query.filter_by(post="Vice-President").all()
    sec_gen = CandidateModel.query.filter_by(post="Secretary-General").all()
    trez = CandidateModel.query.filter_by(post="Treasurer").all()
    fin_sec = CandidateModel.query.filter_by(post="Financial-Secretary").all()
    return render_template("candidate.html",prez=prez,vice=vice,sec_gen=sec_gen,trez=trez,fin_sec=fin_sec)

@app.route("/candidate_register")
@login_required
def candidate_register():
    if current_user.admin !=1:
        logout_user()
        flash('You do not have required authorization')
        return redirect(url_for('auth.login'))
    else:
        return render_template("candidate_register.html")

@app.route("/candidate_register", methods=["POST"])
def candidate_post():
    mat_no = request.form.get('mat_no')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    batch = request.form.get('batch')
    course = request.form.get('course')
    department = request.form.get('department')
    post = request.form.get('post')
    pic_path = request.form.get('pic_path')
    agenda = request.form.get('agenda')
    
    # roll_no = UserModel.query.filter_by(mat_no =mat_no).first()
    cand = CandidateModel.query.filter_by(mat_no = mat_no).first()

    error = False

    # if not 10000000 <= roll_no <= 99999999:
    #     flash('Roll Number is not valid. Should be 8 digits.','error')
    #     error = True

    if cand:
        flash('Candidate has already been registered.','error')
        return redirect(url_for('candidate_register'))
    
    if not set(first_name).issubset(string.ascii_letters + " "):
        flash('Name can only contain alphabets.','error')
        error = True
    
    if not set(last_name).issubset(string.ascii_letters + " "):
        flash('Name can only contain alphabets.','error')
        error = True

    if not first_name and not last_name:
        flash('Name cannot be left blank.','error')
        error = True

    if not batch and not course and not department:
        flash('Please fill in all the details. Batch, Course and Department information is neccessary.','error')
        error = True
    
    if error:
        return redirect(url_for('candidate_register'))
    else:
        candidate = CandidateModel(mat_no=mat_no, first_name=first_name,last_name=last_name,batch=batch,course=course,department=department,post=post,pic_path=pic_path,agenda=agenda)
        db.session.add(candidate)
        db.session.commit()
        flash('Candidate successfully registered.','success')
        return redirect(url_for('candidate_register'))

@app.route("/live_result")
def live_result():
    prez = CandidateModel.query.filter_by(post="President").all()
    vice = CandidateModel.query.filter_by(post="Vice-President").all()
    sec_gen = CandidateModel.query.filter_by(post="Secretary-General").all()
    trez = CandidateModel.query.filter_by(post="Treasurer").all()
    fin_sec = CandidateModel.query.filter_by(post="Financial-Secretary").all()
    labels=[]
    data=[]
    labels1=[]
    data1=[]
    labels2=[]
    data2=[]
    labels3=[]
    data3=[]
    labels4=[]
    data4=[]
    for candidate in prez:
        name = candidate.first_name+" "+candidate.last_name
        labels.append(name)
        vote=VotesModel.query.filter(VotesModel.post_1==candidate.mat_no).count()
        data.append(vote)
    for candidate in vice:
        name = candidate.first_name+" "+candidate.last_name
        labels1.append(name)
        vote=VotesModel.query.filter(VotesModel.post_2==candidate.mat_no).count()
        data1.append(vote)
    for candidate in sec_gen:
        name = candidate.first_name+" "+candidate.last_name
        labels2.append(name)
        vote=VotesModel.query.filter(VotesModel.post_3==candidate.mat_no).count()
        data2.append(vote)
    for candidate in trez:
        name = candidate.first_name+" "+candidate.last_name
        labels3.append(name)
        vote=VotesModel.query.filter(VotesModel.post_4==candidate.mat_no).count()
        data3.append(vote)
    for candidate in fin_sec:
        name = candidate.first_name+" "+candidate.last_name
        labels4.append(name)
        vote=VotesModel.query.filter(VotesModel.post_5==candidate.mat_no).count()
        data4.append(vote)

    return render_template('graph.html',labels=labels,data=data,labels1=labels1,data1=data1,labels2=labels2,data2=data2,labels3=labels3,data3=data3,labels4=labels4,data4=data4)


@app.route("/vote/count")
@cross_origin()
def voteCount():
    prez = CandidateModel.query.filter_by(post="President").all()
    vice = CandidateModel.query.filter_by(post="Vice-President").all()
    sec_gen = CandidateModel.query.filter_by(post="Secretary-General").all()
    trez = CandidateModel.query.filter_by(post="Treasurer").all()
    fin_sec = CandidateModel.query.filter_by(post="Financial-Secretary").all()
    labels=[]
    data=[]
    labels1=[]
    data1=[]
    labels2=[]
    data2=[]
    labels3=[]
    data3=[]
    labels4=[]
    data4=[]
    for candidate in prez:
        name = candidate.first_name+" "+candidate.last_name
        labels.append(name)
        vote=VotesModel.query.filter(VotesModel.post_1==candidate.mat_no).count()
        data.append(vote)
    for candidate in vice:
        name = candidate.first_name+" "+candidate.last_name
        labels1.append(name)
        vote=VotesModel.query.filter(VotesModel.post_2==candidate.mat_no).count()
        data1.append(vote)
    for candidate in sec_gen:
        name = candidate.first_name+" "+candidate.last_name
        labels2.append(name)
        vote=VotesModel.query.filter(VotesModel.post_3==candidate.mat_no).count()
        data2.append(vote)
    for candidate in trez:
        name = candidate.first_name+" "+candidate.last_name
        labels3.append(name)
        vote=VotesModel.query.filter(VotesModel.post_4==candidate.mat_no).count()
        data3.append(vote)
    for candidate in fin_sec:
        name = candidate.first_name+" "+candidate.last_name
        labels4.append(name)
        vote=VotesModel.query.filter(VotesModel.post_5==candidate.mat_no).count()
        data4.append(vote)

    output = {"data": data,
            "labels": labels,
            "data1": data1,
            "labels1": labels1,
            "data2": data2,
            "labels2": labels2,
            "data3": data3,
            "labels3": labels3,
            "data4": data4,
            "labels4": labels4}
    response = app.response_class(
        response=json.dumps(output),
        status=200,
        mimetype='application/json'
    )
    return response
