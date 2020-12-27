from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo
import email_validator
from model import User, Role


class ConsumerRegForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=25)])
    familyname = StringField('Family Name', validators=[DataRequired(), Length(min=3, max=25)])
    address = StringField('Address', validators=[DataRequired(), Length(min=3, max=40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm = PasswordField('Confirm', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user_check = User.query.filter_by(email=self.email.data).first()
        if user_check:
            raise ValidationError('This user has been register before or taken')


class SupplierRegForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=25)])
    PIVA = StringField('PIVA', validators=[DataRequired(), Length(min=3, max=25)])
    address = StringField('Address', validators=[DataRequired(), Length(min=3, max=40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone', validators=[DataRequired()])  # TODO find a phone validator. number
    description = StringField('Description', validators=[DataRequired(), Length(max=5000)]) # no minimum and max of 5000 characters
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    submit = SubmitField('Register')


class loginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=3, max=15), DataRequired()])
    submit = SubmitField('Login')