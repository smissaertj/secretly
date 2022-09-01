import datetime
import jwt
from app import app, db, helpers, models
from flask import request
from functools import wraps

def token_required(f):
    """ Decorator function to check if the Authorization header is passed in the request, return a 403 if missing."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]

        if not token:
            return helpers.json_response('Authentication Token Missing!', 'error', 401)

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = models.User.filter_by(id=data['user_id'])

            if current_user == None:
                return helpers.json_response('Invalid Authentication Token!', 'error', 401)

            if not current_user['is_active']:
                return helpers.json_response('Account is deactivated!', 'error', 403)

        except Exception as e:
            return helpers.json_response(str(e), 'error', 500)

        return f(current_user, *args, **kwargs)

    return decorated


# TODO - Signup/Register
@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':

            # Parse the JSON from the POST request
            data = request.get_json()
            email = data['email']
            password = data['password']

            passwd_hash = helpers.hash_password(password)

            new_user = models.User(email=email, passwd_hash=passwd_hash)
            new_user.addToDB()

            return helpers.json_response('Thank you. You can now login', 'success', 200)

    except KeyError:
        return helpers.json_response('Required data missing in POST request.', 'error', 400)

# TODO - Email Activation


# TODO - Login
@app.route('/api/login', methods=['POST'])
def login():
    try:
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':

            # Parse the JSON from the POST request
            data = request.get_json()
            email = data['email']
            password = data['password']

            user = models.User.query.filter_by(email=email).first()

            if user:
                if helpers.verify_password(user.passwd_hash, password):
                    token = jwt.encode({
                        'public_id': user.id,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
                    }, app.config['SECRET_KEY'], "HS256")

                    return helpers.json_response('Login successful!', 'success', 200, token=token)

            return helpers.json_response('Invalid email or password!', 'error', 401)
    except KeyError:
        return helpers.json_response('Required data missing in POST request.', 'error', 400)


@app.route('/api/new_message', methods=['POST'])
def new_message():
    try:
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':

            # Parse the JSON from the POST request
            data = request.get_json()
            message = data['message']
            password = data['password']
            to_email = data['to_email']

            # Hash the password
            passwd_hash = helpers.hash_password(password)

            # Create new Message instance and save data to database
            new_message = models.Message(message_txt=message, passwd_hash=passwd_hash)
            new_message.addToDB()

            # Send email with message.uuid
            sg_response = helpers.send_mail(to_email, new_message.uuid)
            if sg_response:
                return helpers.json_response('Email sent!', 'success', 200, msg_uuid=new_message.uuid)
            else:
                return helpers.json_response('Error sending email', 'error', 500, msg_uuid=new_message.uuid)
        else:
            return helpers.json_response('Content-Type should be application/json', 'error', 400)

    except KeyError:
        return helpers.json_response('Required data missing in POST request.', 'error', 400)


@app.route('/api/read_message', methods=['POST'])
def read_message():
    try:
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            data = request.get_json()
            print(data)
            uuid = data['uuid']
            password = data['password']

            retrieved_msg = models.Message.query.filter_by(uuid=uuid).first()

            # Return the message if it exists, was not opened before and the password matches the hashed password
            if retrieved_msg != None and \
                    retrieved_msg.is_read != True and \
                    helpers.verify_password(retrieved_msg.passwd_hash, password):
                # Mark the message as read
                # retrieved_msg.is_read = True
                retrieved_msg.read_date = datetime.datetime.now()
                db.session.add(retrieved_msg)
                db.session.commit()

                return helpers.json_response(retrieved_msg.message, 'success', 200, retrieved_msg.uuid)

            else:
                return helpers.json_response('Invalid message UUID or wrong password.', 'error', 401)
        else:
            return helpers.json_response('Content-Type should be application/json', 'error', 400)

    except KeyError:
        print(request.get_json())
        return helpers.json_response('Required data missing in POST request.', 'error', 400)