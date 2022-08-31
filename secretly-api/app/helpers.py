import sendgrid
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from decouple import config
from flask import make_response, jsonify
from sendgrid.helpers.mail import Mail, Email, To, Content

# Generate JSON responses
def json_response(response_msg, severity, status_code, msg_uuid=None):
    response = make_response(
        jsonify(
            {
                'response_msg': response_msg,
                'severity': severity,
                'msg_uuid': msg_uuid
            }
        ),
        status_code
    )
    return response


# Password verification
def hash_password(password):
    argon2Hasher = PasswordHasher(
        time_cost=3, # number of iterations
        memory_cost=64 * 1024, # 64mb
        parallelism=1, # how many parallel threads to use
        hash_len=32, # the size of the derived key
        salt_len=16 # the size of the random generated salt in bytes
    )
    hash = argon2Hasher.hash(password)
    return hash


def verify_password(hash, passwd):
    try:
        ph = PasswordHasher()
        return ph.verify(hash, passwd)
    except VerifyMismatchError:
        return False

# Email sending
def send_mail(to_email, uuid):
    try:
        sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
        from_email = Email(config('SENDGRID_FROM_EMAIL'))
        to_email = To(to_email)
        subject = "You received an encrypted message!"
        content = Content('text/html', uuid)
        mail = Mail(from_email, to_email, subject, content)

        mail_json = mail.get()
        response = sg.client.mail.send.post(request_body=mail_json)
        if response.status_code == 202 or response.status_code == 200:
            return True
        else:
            return False
    except Exception:
        return False
