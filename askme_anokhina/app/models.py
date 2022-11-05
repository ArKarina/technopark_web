from django.db import models

QUESTIONS = [
    {
        'id': question_id,
        'title': f'Question #{question_id}',
        'text': f'Text of question #{question_id}',
        'rating': question_id * 2,
        'answers_number': question_id * question_id,
        'tags': ['tag' for i in range(question_id)],
    } for question_id in range(10)
]

ANSWERS = [
    {
        'id': answer_id,
        'title': f'Answer #{answer_id}',
        'text': f'Text of answer #{answer_id}',
        'rating': answer_id * 2,
    } for answer_id in range(10)
]
