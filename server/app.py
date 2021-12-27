import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS


BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

CUSTOMERS = [
    {
        'userid': uuid.uuid4().hex,
        'name': 'Sylvia',
        'email': 'sylvia@email.com',
        'timezone': 'UTC+9'
    },
    {
        'userid': uuid.uuid4().hex,
        'name': 'Robin',
        'email': 'robin@email.com',
        'timezone': 'UTC-6'
    },
    {
        'userid': uuid.uuid4().hex,
        'name': 'Joyce',
        'email': 'joyce@email.com',
        'timezone': 'UTC+3'
    },
    {
        'userid': uuid.uuid4().hex,
        'name': 'Ting',
        'email': 'ting@email.com',
        'timezone': 'UTC+3'
    }
]

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/customers', methods=['GET', 'POST'])
def getAllCustomers():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        CUSTOMERS.append({
            'userid': uuid.uuid4().hex,
            'name': post_data.get('name'),
            'email': post_data.get('email'),
            'timezone': post_data.get('timezone')
        })
        print(post_data)
        response_object['message'] = 'Customer added!'
    else:
        response_object['customers'] = CUSTOMERS
    return jsonify(response_object)

@app.route('/customers/<userid>', methods=['PUT', 'DELETE'])
def single_customer(userid):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_customer(userid)
        CUSTOMERS.append({
            'userid': uuid.uuid4().hex,
            'name': post_data.get('name'),
            'email': post_data.get('email'),
            'timezone': post_data.get('timezone')
        })
        response_object['message'] = 'Customer updated!'
    if request.method == 'DELETE':
        remove_customer(userid)
        response_object['message'] = 'Customer removed!'
    return jsonify(response_object)

def remove_customer(userid):
    for customer in CUSTOMERS:
        if customer['userid'] == userid:
            CUSTOMERS.remove(customer)
            return True
    return False

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False


@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
