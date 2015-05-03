from . import *
from exercise_question.unique_answer_mcq import UniqueAnswerMCQExerciseQuestion
from exercise_question.multiple_answer_mcq import MultipleAnswerMCQExerciseQuestion
from exercise_question.right_or_wrong import RightOrWrongExerciseQuestion
from exercise_question.dropdown import DropdownExerciseQuestion
from exercise_question.ordering import OrderingExerciseQuestion
from exercise_question.categorize import CategorizeExerciseQuestion
from random import shuffle
from bson import ObjectId
import exceptions


class ExerciseResourceContent(ResourceContent):

    unique_answer_mcq_questions = db.ListField(db.EmbeddedDocumentField(UniqueAnswerMCQExerciseQuestion))
        """A (possibly empty) list of unique-answer multiple-choice questions (`UniqueAnswerMCQExerciseQuestion`)."""

    multiple_answer_mcq_questions = db.ListField(db.EmbeddedDocumentField(MultipleAnswerMCQExerciseQuestion))
        """A (possibly empty) list of multiple-answer multiple-choice questions (`MultipleAnswerMCQExerciseQuestion`)."""

    right_or_wrong_questions = db.ListField(db.EmbeddedDocumentField(RightOrWrongExerciseQuestion))
        """A (possibly empty) list of multiple-answer multiple-choice questions (`RightOrWrongExerciseQuestion`)."""

    dropdown_questions = db.ListField(db.EmbeddedDocumentField(DropdownExerciseQuestion))
        """A (possibly empty) list of dropdown questions (`DropdownExerciseQuestion`)."""

    ordering_questions = db.ListField(db.EmbeddedDocumentField(OrderingExerciseQuestion))
        """A (possibly empty) list of ordering questions (`OrderingExerciseQuestion`)."""

    categorize_questions = db.ListField(db.EmbeddedDocumentField(CategorizeExerciseQuestion))
        """A (possibly empty) list of categorizing questions (`CategorizeExerciseQuestion`)."""

    @property
    def questions(self):
        """A list of all questions, whatever their type."""

        questions = []
        questions.extend(self.unique_answer_mcq_questions)
        questions.extend(self.multiple_answer_mcq_questions)
        questions.extend(self.right_or_wrong_questions)
        questions.extend(self.dropdown_questions)
        questions.extend(self.ordering_questions)
        questions.extend(self.categorize_questions)
        
        return questions

    def question(self, question_id):
        """A getter for a question with a known `_id`."""

        oid = ObjectId(question_id)
        for question in self.questions:
            if question._id == oid:
                return question
        
        raise exceptions.KeyError("Question not found.")

    def random_questions(self, number=None):
        """
        A list of random questions.
        If `number` is not specified, it will be set to the exercise's `number_of_questions` property.
        The list will contain `number` questions, or all questions if there are not enough questions in the exercise.
        """

        if not number:
            number = self.number_of_questions

        all_questions = self.questions
        shuffle(all_questions)
        return all_questions[:number]

    number_of_questions = db.IntField()
        """The number of questions to ask from this exercise."""

    max_mistakes = db.IntField()
        """The number of mistakes authorized before failing the exercise."""

    fail_linked_resource = db.ReferenceField(Resource)
        """A resource to look again when failing the exercise."""


class ExerciseResource(Resource):
    """An exercise with a list of questions."""

    resource_content = db.EmbeddedDocumentField(ExerciseResourceContent)

    @property
    def questions(self):
        """A shorthand getter for the list of questions in the resource content."""
        return self.resource_content.questions()

    def question(self, question_id):
        """A shorthand getter for a question with a known `_id`."""
        return self.resource_content.question(question_id)

    def random_questions(self, number=None):
        """
        A shorthand getter for a list of random questions.
        See the documentation of `ExerciseResourceContent.random_questions`.
        """
        return self.resource_content.random_questions(number)
