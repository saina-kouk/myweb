from sainakoukpari import db

class Contact(db.Model):
	id = db.Column(
		db.Integer,
		primary_key = True
	)
	email = db.Column(
		db.String(120),
		nullable = False
	)
	expiry = db.Column(
		db.String(19),
		nullable = False
	)