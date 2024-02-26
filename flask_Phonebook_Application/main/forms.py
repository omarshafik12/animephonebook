from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Email

class QueryForm(FlaskForm):
    search = StringField("Search")

#I'm just gonna put a variable for each thing in the database
class ProfileForm(FlaskForm):
    firstname = StringField("Firstname", validators=[DataRequired()])
    lastname = StringField("Lastname", validators=[DataRequired()])
    phonenumber = StringField("Phonenumber", validators=[DataRequired()])
    show = StringField("Anime", validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    abilities = StringField("abilities", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    country = StringField("Country", validators=[DataRequired()])
    post = StringField("Post Code", validators=[DataRequired()])
    
    photo = FileField(validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!') ])

    #buttons
    submit = SubmitField("Submit Profile")
    delete_image = SubmitField("Delete Image")
    delete_profile = SubmitField("Delete")