from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_HOST'] = os.environ.get('DB_HOST')
app.config['MYSQL_USER'] = os.environ.get('DB_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('DB_PASS')
app.config['MYSQL_DB'] = os.environ.get('DB_DATABASE')

mysql.init_app(app)


@app.route('/users', methods = ['POST'])
def create_user():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']

    cursor = mysql.connection.cursor()
    user = cursor.execute('''
    INSERT INTO users (name, email, password)
    VALUES (%s, %s, %s)
    ''', (name, email, password))

    mysql.connection.commit()

    return jsonify({'message': 'User created successfully.'}), 201


@app.route('/users/<int:id>', methods = ['GET'])
def get_user(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE id = %s', (id,))

    user = cursor.fetchone()

    return jsonify({'user': user}), 200


@app.route('/users', methods = ['GET'])
def get_users():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users')

    users = cursor.fetchall()
    
    return jsonify({'number of users': len(users), 'user': users}), 200


@app.route('/users/<int:id>', methods = ['PATCH'])
def update_user(id):
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']

    cursor = mysql.connection.cursor()
    user = cursor.execute('UPDATE users SET name = %s, email = %s, password = %s WHERE id = %s', 
                   (name, email, password, id))
    
    mysql.connection.commit()

    if not user:
        raise Exception(f'''User ID {id} not found''')

    return jsonify({'message': 'User updated successfully.'}), 200


@app.route('/users/<int:id>', methods = ['DELETE'])
def delete_user(id):
    cursor = mysql.connection.cursor()
    user = cursor.execute('DELETE FROM users WHERE id = %s', (id,))
    
    if not user:
        raise Exception(f'''User ID {id} not found''')

    mysql.connection.commit()

    return jsonify({'message': 'User deleted successfully.'}), 200


if __name__ == '__main__':
    app.run(debug=True)