from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField, PasswordField, DateField, RadioField, ValidationError
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo, Optional
from .models import User


class ImageFilterForm(Form):
    start_date = DateField('Start date', validators=[Optional()])
    end_date = DateField('End date', validators=[Optional()])
    sort_order = RadioField('Sort Order', choices =[('old_to_new','Old to New'),('new_to_old','New to Old')])

class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(),
                                             Length(1,64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    visit_select = SelectField('visit_select',
                                 choices=[(None, ''),
                                          ('theft','Theft'),
                                          ('injury', 'Injury'),
                                          ('damage', 'Property Damage'),
                                          ('admin', 'Admin')],
                                 validators=[DataRequired()]
                                 )
    visit_description = TextAreaField('visit_description', validators=[DataRequired(),
                                                                       Length(min=25)])


class RegistrationForm(Form):
    name = StringField('Name', validators=[DataRequired(),
                                           Length(1, 64),
                                           Regexp('^[A-Za-z][A-Za-z_.]*$', 0, "First Name, Last Name, and Underscores/periods only")
                                           ])
    email = StringField('Email', validators=[DataRequired(),
                                             Length(1,64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     EqualTo('password2', message="Passwords do not match.")])
    password2 = PasswordField('Confirm Password', validators= [DataRequired()])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')



