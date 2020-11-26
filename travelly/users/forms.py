from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from travelly.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)],
                            render_kw={"placeholder": "Username"})
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)],
                            render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')],
                                    render_kw={"placeholder": "Confirm Password"})

    submit = SubmitField('Sign up')

    # def validate_field(self, field):
    #     if True:
    #         raise ValidationError('Validation Message')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
            # flash('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already used. Please choose a different one.')
            # flash('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()],
                        render_kw={"placeholder": "Password"})
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)],
                            render_kw={"placeholder": "Username"})
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Email"})
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])],
                        render_kw={"placeholder": "Add Picture"})
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')
                flash('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already used. Please choose a different one.')
                flash('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Email"})
    submit = SubmitField('Send Email')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            #we do nothing in order not to have some security issues. We don't want anyone to know
            #if a certain user exists or not
            pass


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()],
                            render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')],
                                    render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Reset Password')