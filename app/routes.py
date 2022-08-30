import datetime

from app import app, db, helpers, models
from flask import request, make_response, jsonify

@app.route('/api/new_message', methods=['POST'])
def new_message():
    try:
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':

            # Parse the JSON from the POST request
            data = request.get_json()[0]
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
                response = make_response(
                    jsonify(
                        {
                            'response_msg': 'Email sent!',
                            'severity': 'success',
                            'msg_uuid': new_message.uuid
                         }
                    ),
                    200
                )
                return response
            else:
                response = make_response(
                    jsonify(
                        {
                            'response_msg': 'Error sending email. You may want to deliver the UUID yourself :(',
                            'severity': 'error',
                            'msg_uuid': new_message.uuid
                        }
                    ),
                    500
                )
                return response
        else:
            response = make_response(
                jsonify(
                    {
                        'response_msg': 'Content-Type should be application/json',
                        'severity': 'error'
                     },
                ),
                400
            )
            return response
    except KeyError:
        response = make_response(
            jsonify(
                {
                    'response_msg': 'Required data missing in POST request.',
                    'severity': 'error'
                }
            ),
            400
        )
        return response


@app.route('/api/read_message', methods=['POST'])
def read_message():
    try:
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            data = request.get_json()[0]
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
                db.session.add(retrieved_msg)
                db.session.commit()

                response = make_response(
                    jsonify(
                        {
                            'response_msg': f'{retrieved_msg.message}',
                            'severity': 'success'
                         },
                    ),
                    200
                )
                return response
            else:
                response = make_response(
                    jsonify(
                        {
                            'response_msg': 'Invalid message UUID or wrong password.',
                            'severity': 'error'
                         },
                    ),
                    401
                )
                return response
        else:
            response = make_response(
                jsonify(
                    {
                        'response_msg': 'Content-Type should be application/json',
                        'severity': 'error'
                     },
                ),
                400
            )
            return response
    except KeyError:
        response = make_response(
            jsonify(
                {
                    'response_msg': 'Required data missing in POST request.',
                    'severity': 'error'
                }
            ),
            400
        )
        return response