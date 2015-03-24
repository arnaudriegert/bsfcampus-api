from MookAPI import db
from bson import ObjectId
import datetime
import exceptions


class ExerciseQuestion(db.DynamicEmbeddedDocument):
	"""
	Generic collection, every question type will inherit from this.
	Subclasses should override method "without_answer" in order to define the version sent to clients.
	"""
	
	meta = {
		'allow_inheritance': True,
		'abstract': True
	}

	_id = db.ObjectIdField(default=ObjectId)

	## Question text
	question_text = db.StringField(required=True)

	## Correct answer (field type depends on question type)
	correct_answer = db.DynamicField()

	def without_answer(self):
		son = self.to_mongo()
		son.pop('correct_answer', None)
		return son

	def answer_with_data(self, data):
		return ExerciseQuestionAnswer().init_with_data(data)


class ExerciseQuestionAnswer(db.DynamicEmbeddedDocument):
	"""
	Generic collection to save answers given to a question.
	Subclasses should define their own properties to store the given answer.
	They must also override method "is_correct" in order to determine whether the given answer is correct.
	"""

	meta = {
		'allow_inheritance': True,
		'abstract': True
	}

	### PROPERTIES

	## There is no property common to all types.

	### METHODS

	def init_with_data(self, data):
		"""
		This is a hack to bypass __init__ (I don't know how to use it yet).
		'data' is the form data sent by the client.
		MUST return self.
		"""

		raise exceptions.NotImplementedError("This question type has no initializer.")

	## This method needs to be overridden for each question type.
	def is_correct(self, question, parameters):
		"""
		Whether the answer is correct.
		Pass the question itself and the parameters, if any.
		"""

		raise exceptions.NotImplementedError("This question type has no correction method.")


__all__ = [
	'ExerciseQuestion',
	'ExerciseQuestionAnswer',
	'multiple_answer_mcq',
	'unique_answer_mcq'
]
