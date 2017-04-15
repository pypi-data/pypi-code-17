"""A quiz that manages questions."""

import random

from itertools import groupby

from .questions.base import Question, WrongAnswer
from .questions import *


def all_questions():
    """Return a list of all question classes."""
    return list(Question.__subclasses__())


class Quiz(object):
    """Manage a session of questions and answers.

    The quiz starts off with one questions, which is stored
    as current_question. It will move on to the next Question
    if the correct answer is supplied, or if a request is made
    to move on to the next question.

    When all questions have been asked, it loops around and starts
    over again.

    The quiz keeps track of questions answered in a list of tuples,
    where each tuple contains the question, an answer supplied, and
    a boolean indicating if the answer was correct. For example:
    [(question, 'Answer text', False), (question, 'Answer Text', True)]
    """
    def __init__(self):
        """Initialise the quiz."""
        self.questions_asked = []
        self.all_questions = all_questions()
        self.prepare_questions()

    def prepare_questions(self):
        """Prepare the questions."""
        random.shuffle(self.all_questions)
        self.question_iterator = iter(self.all_questions)
        self.current_question = next(self.question_iterator)()

    def next(self):
        """Move on to the next question and return it."""
        try:
            self.current_question = next(self.question_iterator)()
        except StopIteration:
            self.prepare_questions()
        return self.current_question

    def supply_answer(self, question, answer):
        """Check the answer and move on to the next question if it's correct.

        Raises a WrongAnswer exception if the answer is incorrect.
        """
        correct_answer = False
        try:
            correct_answer = question.check_answer(answer)
            self.next()
            return correct_answer
        finally:
            self.questions_asked.append(
                (self.current_question, answer, correct_answer)
            )


    def last_answer_was_correct(self):
        """Check if the last answer was correct."""
        if self.questions_asked:
            return self.questions_asked[-1][-1]

    def get_results(self):
        """Get the score and a log of questions and answers."""
        questions_answered = {
            question.get_question_text(): [i[1:]for i in answer]
            for question, answer in groupby(self.questions_asked, key=lambda k: k[0])
        }
        number_of_questions = len(questions_answered)
        number_correct = sum(
            2 ** (1 - len(answer)) for answer in questions_answered.values()
            if answer[-1][-1]
        )
        summary = "Total score: {} of {}".format(number_correct, number_of_questions)
        results = ""
        for question, answers in questions_answered.items():
            results += '---\n\nQuestion: {}...\n\n'.format(question.split('\n', 1)[0])
            for answer in answers:
                results += 'Answer: {}\n'.format(answer[0])
                results += 'Correct: {}\n\n'.format(bool(answer[1]))

        return "{}\n\n{}".format(summary, results)
