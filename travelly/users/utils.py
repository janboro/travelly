import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from travelly import mail

def save_picture(form_picture):
    #generating a random hex as a new file name
    random_hex = secrets.token_hex(8)
    #extracting the file extension from uploaded file
    _, f_ext = os.path.splitext(form_picture.filename)
    #creating a new picture filename to be stored in our database
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    
    #resizing the picture to 125px by 125px
    output_size = (125,125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)

    img.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                sender='noreply@demo.com',
                recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:

{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this email and no changes will be made
'''
    mail.send(msg)