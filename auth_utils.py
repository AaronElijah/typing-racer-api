import bcrypt
import csv


def get_hash(plain_text_password):
    # Hash a password for the first time
    # (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())


def check_hashed(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password, hashed_password)


def write_new_user_to_db(new_user):
    with open('demo_db.csv', 'a', newline='') as db:
        writer = csv.writer(db, delimiter=' ')
        writer.writerow(new_user)
    db.close()


def read_users_from_db():
    users = []
    with open('demo_db.csv', 'r', newline='') as db:
        reader = csv.reader(db, delimiter=' ')
        for row in reader:
            if row:
                user = {'email': row[0], 'is_verified': row[1]}
                users.append(user)
    db.close()
    return users


def write_all_users_to_db(users):
    with open('demo_db.csv', 'w', newline='') as db:
        writer = csv.writer(db, delimiter=' ')
        writer.writerows(users)
    db.close()
