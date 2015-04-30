import flask
from MookAPI import db
import datetime
import bson

class ItemToSync(db.Document):

	### PROPERTIES

	## A counter to depile items in the right order
	queue_position = db.SequenceField()

	## ObjectId of the item on the central server
	distant_id = db.ObjectIdField()

	## Class of the item
	class_name = db.StringField()

	## Action to perform (delete local or fetch new version of distant)
	action = db.StringField(choices=('update', 'delete'))

	## URL to fetch update info (null if action == 'delete')
	url = db.StringField()

	errors = db.ListField(db.StringField())
