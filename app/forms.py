from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    visit_select = SelectField('visit_select',
                                 choices=[(None, ''), ('theft','Theft'),('reason','Other Reason')],
                                 validators=[DataRequired()]
                                 )
    visit_description = TextAreaField('visit_description', validators=[DataRequired()])




