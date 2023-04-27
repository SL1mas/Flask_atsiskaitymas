from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from __init__ import app, db, login_manager, bcrypt
import forms
from models import User, Group, Bill


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/register", methods=['GET', 'POST'])
def register():
    db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        form.check_email(email=form.email)
        encrypted_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(
            first_name=form.name.data, email=form.email.data, password=encrypted_password)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('groups', id=current_user.id))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('groups', id=user.id))
        else:
            flash('Login failed. Check your email address and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/groups/<int:id>", methods=['GET', 'POST'])
@login_required
def groups(id):
    db.create_all()
    groups = Group.query.all()
    form = forms.AddGroupForma()
    if form.validate_on_submit():
        adding_group = Group.query.get(form.group_id.data)
        if adding_group == groups:
            current_user.groups.append(adding_group)
            db.session.add(current_user)
            db.session.commit()
            flash('Group added successfully!', 'success')
        flash('Group does not exist!', 'danger')
        return redirect(url_for('groups', id=current_user.id))
        # 2nd option
        # return redirect(request.url)
    return render_template('groups.html', groups=groups, form=form)


@app.route("/bill/<int:id>", methods=['GET', 'POST'])
@login_required
def bill(id):
    db.create_all()
    group = Group.query.get(id)
    bills = Bill.query.all()
    form = forms.AddBillForma()
    if form.validate_on_submit():
        bill = Bill(group_id=group.id, amount=form.amount.data,
                    description=form.description.data)
        db.session.add(bill)
        db.session.commit()
        flash('Bill added successfully!', 'success')
        return redirect(url_for('bill', id=group.id))
        # 2nd option
        # return redirect(request.url)
    return render_template('bill.html', group=group, bills=bills, form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('server_error.html'), 500
