from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

from user import User

client = MongoClient("mongodb+srv://olasubomiwilliams1:olasubomi2001@cluster0.gbbcxlv.mongodb.net/?retryWrites=true&w=majority")
database_chat = client.get_database('SubomiChatDB')
users_collection = database_chat.get_collection('users')
rooms_collection = database_chat.get_collection('rooms')
rooms_members = database_chat.get_collection('room_members')

def save_user(username, email, password):
    pass_hash = generate_password_hash(password)
    users_collection.insert_one({'_id': username, 'email': email, 'password':pass_hash})
    
def get_user(username):
    user_data = users_collection.find_one({'_id': username})
    return User(user_data['_id'], user_data['email'], user_data['password']) if user_data else None

def save_room(room_name, created_by):
    room_id = rooms_collection.insert_one(
        {'room_name': room_name, 'created_by': created_by, 'created_at': datetime.now()}).inserted_id
    add_room_member(room_id, room_name, created_by, created_by, is_admin=True)
    return room_id

def update_room(room_id, room_name):
    rooms_collection.update_one({'_id':ObjectId(room_id)}, {'$set': {'room_name':room_name}})

def get_room(room_id):
    return rooms_collection.find_one({'_id': ObjectId(room_id)})

def add_room_member(room_id, room_name, username, added_by, is_admin=False):
    rooms_members.insert_one({'_id' : {'room_id':ObjectId(room_id), 'username':username},
                              'room_name':room_name, 'added_by':added_by,
                              'added_at':datetime.now(), 'is_admin':is_admin})

def add_room_members(room_id, room_name, usernames, added_by):
    rooms_members.insert_many([{'_id' : {'room_id':ObjectId(room_id), 'username':username},
                              'room_name':room_name, 'added_by':added_by,
                              'added_at':datetime.now(), 'is_admin':False} for username in usernames])

def remove_room_members(room_id, usernames):
    rooms_members.delete_many({'_id': {'$in': [{'room_id': room_id, 'username':username} for username in usernames]}})

def get_room_members(room_id):
    return list(rooms_members.find({'_id.room_id':ObjectId(room_id)}))

def get_room_for_user(username):
    return list(rooms_members.find({'_id.username': username}))

def is_room_member(room_id, username):
    return rooms_members.collection.count_documents({'_id': {'room_id':ObjectId(room_id), 'username':username}})

def is_room_admin(room_id, username):
    return rooms_members.count_documents({'_id': {'room_id':ObjectId(room_id), 'username':username}, "is_admin":True})

# save_user('Subomi', 'subomi123@gmail.com', 'test')
