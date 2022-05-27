from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, RadioField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class GameForm(FlaskForm):
    difficulty = RadioField('Difficulty Level', choices = ['Easy', 'Medium', 'Hard'], validators=[DataRequired()])
    submit = SubmitField('Play Game')
    
class MoveForm(FlaskForm):
    location = IntegerField('location', validators=[DataRequired(), NumberRange(min=0, max=6, message='Number must be between 0 and 6')])
    submit = SubmitField('Submit Move')
    
class NumberForm(FlaskForm):
    zero = SubmitField('0')
    one = SubmitField('1')
    two = SubmitField('2')
    three = SubmitField('3')
    four = SubmitField('4')
    five = SubmitField('5')
    six = SubmitField('6')