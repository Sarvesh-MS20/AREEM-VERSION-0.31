# db/db_ops.py
from db.db import get_connection


# create user
def create_user(name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("INSERT INTO users (name) VALUES (%s) returning id;", (name,))
    user_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()
    return user_id


#saving the chat
def save_chat_history(user_id, role, message):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("INSERT INTO chat_history(user_id ,role,message) values (%s ,%s,%s);",(user_id,role,message))
    connection.commit()
    cursor.close()
    connection.close()


# getting the chat
def get_chat_history(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT role,message FROM chat_history WHERE user_id = (%s) ORDER BY id;",(user_id,))
    chat_history = cursor.fetchall()

    cursor.close()
    connection.close()
    return chat_history


#saving the memory
def save_memory(user_id,key,value):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO memory (user_id,key,value) values (%s,%s,%s);",(user_id,key,value))

    connection.commit()
    cursor.close()
    connection.close()


# getting the memory
def get_memory(user_id,key):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT value from memory WHERE user_id = (%s) and key = (%s) ;" ,(user_id,key))

    memory = cursor.fetchone()
    cursor.close()
    connection.close()
    return memory











