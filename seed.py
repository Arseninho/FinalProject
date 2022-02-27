from faker import Faker
from main import db, UserModel, PostModel
from random import randint


db.create_all()

fake=Faker()



for i in range (1,200):
    user=UserModel(username=fake.name(),email=fake.email(),password=)
    db.session.add(user)
    db.session.commit()

for i in range (1,200):
    post=PostModel(title=fake.paragraph(nb_sentences=1), body=fake.text(), user_id=randint(1,200))
    db.session.add(post)
    db.session.commit()

