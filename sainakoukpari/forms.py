from datetime import date, datetime, timedelta
from flask_wtf import FlaskForm, RecaptchaField
from sainakoukpari.models import Contact
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, ValidationError

class ContactForm(FlaskForm):
	name = StringField('Name*', validators=[DataRequired()])
	email = StringField('Email*', validators=[DataRequired(), Email()])
	message = TextAreaField('What can we help you with?*', validators=[DataRequired(), Length(max=1000)])
	recaptcha = RecaptchaField()
	submit = SubmitField('Send message')

	def validate_email(self, email):
		user = Contact.query.filter_by(email=email.data.lower()).first()
		if user and (datetime.today().replace(microsecond=0) < datetime.strptime(user.expiry, '%Y-%m-%d %H:%M:%S')):
			raise ValidationError('Please wait 2 minutes between messages.')