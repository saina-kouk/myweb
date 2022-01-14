from datetime import date, datetime, timedelta
from flask import abort, jsonify, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user
from itsdangerous import URLSafeTimedSerializer
from drone import app, db
from drone.forms import ContactForm
from drone.models import Contact
import os, random, requests

def send_email(email, subject, body, email_from, attachment = []):
    return requests.post(
        'https://api.mailgun.net/v3/'+app.config['MAILGUN_DOMAIN']+'/messages',
        auth=('api', app.config['MAILGUN_KEY']),
        files= attachment,
        data={'from': 'New Inquiry <'+email_from+'@'+app.config['MAILGUN_DOMAIN']+'>',
              'to': email,
              'subject': subject,
              'html': body})

@app.route('/', methods=['GET', 'POST'])
def default():
	return render_template('home.html')

@app.route('/home/')
@app.route('/home')
def home():
	return redirect(url_for('default'))

@app.route('/film/')
@app.route('/film')
def film():
	return render_template('film.html')

@app.route('/software/')
@app.route('/software')
def software():
	return render_template('software.html')

@app.route('/contact/', methods = ['GET', 'POST'])
@app.route('/contact', methods = ['GET', 'POST'])
def contact():
	form = ContactForm()
	if form.validate_on_submit():
		body = "<p>"+form.message.data.replace('\n', '</p>\n\n<p>')+"</p>\n\n<p>-- <br> Return email: "+form.email.data.lower()+"<br> Preferred method of contact: "+form.method.data+["<br> Preferred address: "+form.other.data, ''][form.method.data=='Email']+"</p>"
		send_email(['saina.koukpari@gmail.com'], 'New Inquiry from '+form.name.data, body, 'inquiry')
		user = Contact.query.filter_by(email=form.email.data.lower()).first()
		if not user:
			archive = Contact(
				email = form.email.data.lower(),
				expiry = str(datetime.today().replace(microsecond=0)+timedelta(minutes=2))
				)
			db.session.add(archive)
		else:
			user.expiry = str(datetime.today().replace(microsecond=0)+timedelta(minutes=2))
		db.session.commit()
		return render_template('contact.html', form=form, success=True)
	return render_template('contact.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_service_error(e):
    return render_template('errors/500.html'), 500