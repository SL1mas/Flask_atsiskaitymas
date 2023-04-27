from models import db, Group

db.create_all()

group1 = Group("Trip to Wonderland")
group2 = Group("Trip to Latvia")
group3 = Group("Trip to Estija")
group4 = Group("Trip to Space")
group5 = Group("Trip to Mountains")
group6 = Group("Trip to USA")
group7 = Group("Trip to Waterfall")
group8 = Group("Trip to Island")
group9 = Group("Trip to Nowhere")
group10 = Group("Trip to Disneyland")

db.session.add_all([group1, group2, group3, group4, group5,
                   group6, group7, group8, group9, group10])
db.session.commit()
