import datetime
import jwt
import os
from app import app, db, helpers, models
from app.templates import emails
from decouple import config
from flask import request, render_template, make_response, jsonify
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
            current_user = models.User.query.filter_by(id=str(data['public_id'])).first()

            if current_user == None:
                return helpers.json_response('Invalid Authentication Token!', 'error', 401)

            if not current_user.is_active:
                return helpers.json_response('Account activation required.', 'error', 403)

        except Exception as e:
            return helpers.json_response(str(e), 'error', 500)

        return f(current_user)

    return decorated


@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':

            # Parse the JSON from the POST request
            data = request.get_json()
            email = data['email']
            first_name = data['first_name']
            last_name = data['last_name']
            password = data['password']

            passwd_hash = helpers.hash_password(password)

            # Check if a user with the same email already exists
            user = models.User.query.filter_by(email=email).first()
            if user != None:
                return helpers.json_response('Email already registered!', 'error', 400)

            new_user = models.User(email=email, passwd_hash=passwd_hash, first_name=first_name, last_name=last_name)
            new_user.addToDB()

            # Send account activation Link
            uuid = new_user.activation_uuid
            content = emails.activation_email(uuid)
            sg_response = helpers.send_mail(to_email=new_user.email, subject='Activate your account.', content=content)
            if sg_response:
                return helpers.json_response('Check your email for the activation link.', 'success', 200)
            else:
                # If the email fails to send, delete the user from the database
                models.User.query.filter_by(id=new_user.id).delete()
                db.commit()
                return helpers.json_response('Error sending email, try registering again later.', 'error', 500, msg_uuid=new_message.uuid)

    except KeyError:
        return helpers.json_response('Required data missing in POST request.', 'error', 400)


@app.route('/api/activate/<uuid>', methods=['GET'])
def activate_account(uuid):
    db_user = models.User.query.filter_by(activation_uuid=uuid).first()

    if db_user and db_user.is_active == False:
        db_user.is_active = True
        db.session.commit()
        app_url = config('APP_URL')
        return render_template('activation.html', state='success', app_url=app_url)

    else:
        return render_template('activation.html', state='error', app_url=config('APP_URL'))


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

                    return helpers.json_response('Login successful!', 'success', 200, token=token, email=user.email,
                                                 first_name=user.first_name, last_name=user.last_name)

            return helpers.json_response('Invalid email or password!', 'error', 401)
    except KeyError:
        return helpers.json_response('Required data missing in POST request.', 'error', 400)


@app.route('/api/user_profile', methods=['POST'])
@token_required
def user_profile(currentUser):
    content_type = request.headers.get('Content-Type')

    if request.method == 'POST':

        try:
            # Update User Data
            if content_type == 'application/json':

                # Parse the JSON from the POST request
                data = request.get_json()
                email = data['email']
                first_name = data['first_name']
                last_name = data['last_name']
                email_changed = False
                # TODO - Fix optional password field

                if currentUser.email != email:
                    email_changed = True
                    currentUser.email = email
                    currentUser.is_active = False
                    currentUser.activation_uuid = os.urandom(8).hex()

                    # Send account activation Link
                    uuid = currentUser.activation_uuid
                    content = emails.activation_email(uuid)
                    helpers.send_mail(to_email=currentUser.email, subject='Activate your account.', content=content)

                if currentUser.first_name != first_name:
                    currentUser.first_name = first_name

                if currentUser.last_name != last_name:
                    currentUser.last_name = last_name

                db.session.commit()
                if email_changed:
                    return helpers.json_response('You\'re email was changed, please log out and check your inbox for the activation link.', 'success', 200)
                else:
                    return helpers.json_response('Profile data updated.', 'success', 200)
            else:
                return helpers.json_response('Content-Type should be application/json', 'error', 400)
        except KeyError:
            return helpers.json_response('Required data missing in POST request.', 'error', 400)


@app.route('/api/user_profile/messages', methods=['GET'])
@token_required
def get_messages(current_user):
    try:
        messages = models.Message.query.filter_by(user_id=current_user.id).all()

        return helpers.json_response('', 'success', 200, user_messages=[message.serialized for message in messages])

    except KeyError:
        return helpers.json_response('Required data missing in POST request.', 'error', 400)

@app.route('/api/new_message', methods=['POST'])
@token_required
def new_message(current_user):
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
            new_message = models.Message(message_txt=message, passwd_hash=passwd_hash, user_id=current_user.id, to_email=to_email)
            new_message.addToDB()

            # Send email with message.uuid
            subject = "You received a new message!"
            content = emails.message_email(new_message.uuid)
            sg_response = helpers.send_mail(to_email=to_email, subject=subject, content=content)
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
                retrieved_msg.is_read = True
                retrieved_msg.read_date = datetime.datetime.now()
                # db.session.add(retrieved_msg)
                db.session.commit()

                return helpers.json_response(retrieved_msg.message, 'success', 200, retrieved_msg.uuid)

            else:
                return helpers.json_response('Invalid UUID or wrong password.', 'error', 401)
        else:
            return helpers.json_response('Content-Type should be application/json', 'error', 400)

    except KeyError:
        print(request.get_json())
        return helpers.json_response('Required data missing in POST request.', 'error', 400)
