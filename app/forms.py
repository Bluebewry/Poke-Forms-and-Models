from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class UserCreationForm(FlaskForm):
    username = StringField("Username", validators= [DataRequired()])
    email = StringField("Email", validators= [DataRequired()])
    password = PasswordField("Password", validators= [DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators= [DataRequired(), EqualTo('password')])
    submit = SubmitField()


class p_name(FlaskForm):
    search_input = StringField("Input")
    submit = SubmitField()

class LoginForm(FlaskForm):
    username = StringField("Username", validators= [DataRequired()])
    password = PasswordField("Password", validators= [DataRequired()])
    submit = SubmitField()

class PostForm(FlaskForm):
    title = StringField("Title", validators= [DataRequired()])
    img_url = StringField("Image URL", validators= [DataRequired()])
    caption = StringField("Caption", validators= [])
    submit = SubmitField()

class EditProfileForm(FlaskForm):
    username = StringField("Username", validators= [DataRequired()])
    email = StringField("Email", validators= [DataRequired()])
    password = PasswordField("Password", validators= [DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators= [DataRequired(), EqualTo('password')])
    submit = SubmitField()


class SearchForm(FlaskForm):
    s = StringField('anything can go here', validators= [DataRequired()])
    send = SubmitField()