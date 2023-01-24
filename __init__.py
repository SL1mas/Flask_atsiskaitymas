import os
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user, logout_user, login_user, UserMixin, login_required
import forms

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'vfv822fvfv26f5dfadsrfasdr54e6rae'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data2.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'prisijungti'
login_manager.login_message_category = 'info'


class Vartotojas(db.Model, UserMixin):
    __tablename__ = "vartotojas"
    id = db.Column(db.Integer, primary_key=True)
    vardas = db.Column("Vardas", db.String(20), nullable=False)
    el_pastas = db.Column("El. pašto adresas", db.String(100),
                          unique=True, nullable=False)
    slaptazodis = db.Column("Slaptažodis", db.String(100),
                            unique=True, nullable=False)
    # group_id = db.Column(db.Integer, db.ForeignKey('group_id'))
    # group = db.relationship('Group')


@login_manager.user_loader
def load_user(vartotojo_id):
    return Vartotojas.query.get(int(vartotojo_id))


@app.route("/register", methods=['GET', 'POST'])
def register():
    db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for('groups'))
    form = forms.RegistracijosForma()
    if form.validate_on_submit():
        koduotas_slaptazodis = bcrypt.generate_password_hash(
            form.slaptazodis.data).decode('utf-8')
        vartotojas = Vartotojas(
            vardas=form.vardas.data, el_pastas=form.el_pastas.data, slaptazodis=koduotas_slaptazodis)
        db.session.add(vartotojas)
        db.session.commit()
        flash('Sėkmingai prisiregistravote! Galite prisijungti', 'success')
        return redirect(url_for('groups'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('groups'))
    form = forms.PrisijungimoForma()
    if form.validate_on_submit():
        user = Vartotojas.query.filter_by(
            el_pastas=form.el_pastas.data).first()
        if user and bcrypt.check_password_hash(user.slaptazodis, form.slaptazodis.data):
            login_user(user, remember=form.prisiminti.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('groups'))
        else:
            flash('Prisijungti nepavyko. Patikrinkite el. paštą ir slaptažodį', 'danger')
    return render_template('login.html', title='Prisijungti', form=form)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # bill_id = db.Column(db.Integer, db.ForeignKey('bill_id'))
    # bill = db.relationship("Bill", backref="group")
    # vartotojai = db.relationship("Vartotojas")

    def __init__(self, group_id, name, bill_id=None):
        self.group_id = group_id
        self.name = name
        self.bill_id = bill_id


class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    # group_id = db.Column(db.Integer, db.ForeignKey('group_id'))
    # group = db.relationship("Group")


@app.route("/groups")
@login_required
def groups():
    groups = Group.query.all()
    return render_template("groups.html", groups=groups)


@app.route("/bills")
@login_required
def bills():
    bills = Bill.query.all()
    return render_template("bills.html", bills=bills)


@app.route("/bill/<int:id>", methods=['GET', 'POST'])
@login_required
def bill(id):
    db.create_all()
    group = Group.query.get(id)
    bills = Bill.query.all()
    form = forms.AddBillForma()
    if form.validate_on_submit():
        bill = Bill(amount=form.amount.data, description=form.description.data)
        db.session.add(bill)
        db.session.commit()
        flash('Įrašas įvestas sėkmingai!', 'success')
        return redirect(url_for('groups'))
    return render_template('bill.html', group=group, bills=bills, form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(port=8000, debug=True)
