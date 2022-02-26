from faker import Faker
from main import db, UserModel, PostModel
from random import randint
import hashlib
from tqdm import tqdm

db.create_all()

fake=Faker()

string="arsena123"
encoded=string.encode()
result = hashlib.sha256(encoded)

print("Hexadecimal equivalent: ",result.hexdigest(), len(result.hexdigest()))


for i in tqdm(range (1,200)):
    user=UserModel(username=fake.name(),email=fake.email(),password=result.hexdigest())
    db.session.add(user)
    db.session.commit()

for i in tqdm(range (1,200)):
    post=PostModel(title=fake.paragraph(nb_sentences=1), body=fake.text(), user_id=randint(1,200))
    db.session.add(post)
    db.session.commit()

