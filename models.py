from __init__ import db
from flask_login import UserMixin

users_groups = db.Table('users_groups', db.metadata,
                        db.Column('group_id', db.Integer,
                                  db.ForeignKey('group.id')),
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column("First Name", db.String(100), nullable=False)
    email = db.Column("Email", db.String(100),
                      unique=True, nullable=False)
    password = db.Column("Password", db.String(100),
                         unique=True, nullable=False)
    groups = db.relationship(
        'Group', secondary=users_groups, back_populates="users")


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    users = db.relationship(
        'User', secondary=users_groups, back_populates="groups")

    def __init__(self, name):
        self.name = name


class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    group = db.relationship("Group")

    # def __init__(self, group_id, amount, description):
    #     self.group_id = group_id
    #     self.amount = amount
    #     self.description = description
