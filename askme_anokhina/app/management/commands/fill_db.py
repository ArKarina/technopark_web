from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from app.models import Profile, Tag, Question, QuestionLike, Answer, AnswerLike
from random import choice, sample, randint
from faker import Faker

faker = Faker()


class Command(BaseCommand):
    help = 'Fill DataBase Python'

    def add_arguments(self, parser):
        parser.add_argument('-ratio', type=int)
        parser.add_argument('-users', type=int)
        parser.add_argument('-tags', type=int)
        parser.add_argument('-questions', type=int)
        parser.add_argument('-answers', type=int)
        parser.add_argument('-likes', type=int)

    def handle(self, *args, **options):
        if options['ratio']:
            self.fill_db(options['ratio'])

        if options['users']:
            self.fill_profiles(options['users'])

        if options['tags']:
            self.fill_tags(options['tags'])

        if options['questions']:
            self.fill_questions(options['questions'])

        if options['answers']:
            self.fill_answers(options['answers'])

        if options['likes']:
            self.fill_questions_likes(options['likes'])
            self.fill_answers_likes(options['likes'])

        self.stdout.write(self.style.SUCCESS('Data creation was successful'))

    @staticmethod
    def fill_profiles(n, avatar_n=5):
        for i in range(n):
            try:
                Profile.objects.create(
                    user=User.objects.create_user(
                        username=faker.user_name(),
                        email=faker.email(),
                        password=faker.password() 
                    ),
                    avatar="static/img/avatar_" + str(i % avatar_n) + ".jpg",
                )
            except Exception:
                pass

    @staticmethod
    def fill_tags(n):
        for i in range(n):
            Tag.objects.create(name=faker.word())

    @staticmethod
    def fill_questions(n, max_tags=10):
        profile_ids = list(Profile.objects.values_list('id', flat=True))
        tag_ids = list(Tag.objects.values_list('id', flat=True))

        for i in range(n):
            try:
                tags_list = sample(tag_ids, randint(1, max_tags))
                Question.objects.create(
                    title=faker.sentence()[:-1] + '?',
                    text=faker.text(),
                    author=Profile.objects.get(pk=choice(profile_ids)),
                    creation_date=faker.date()
                ).tags.set(tags_list)
            except Exception:
                pass

    @staticmethod
    def fill_answers(n):
        profile_ids = list(Profile.objects.values_list('id', flat=True))
        question_ids = list(Question.objects.values_list('id', flat=True))
        statuses = ['c', 'i']
        for i in range(n):
            try:
                Answer.objects.create(
                    question=Question.objects.get(pk=choice(question_ids)),
                    title=faker.sentence(),
                    text=faker.text(),
                    author=Profile.objects.get(pk=choice(profile_ids)),
                    creation_date=faker.date(),
                    status=choice(statuses)
                )
            except Exception:
                pass

    @staticmethod
    def fill_questions_likes(n):
        profile_ids = list(Profile.objects.values_list('id', flat=True))
        question_ids = list(Question.objects.values_list('id', flat=True))

        for i in range(n):
            try:
                like = QuestionLike(
                    question=Question.objects.get(pk=choice(question_ids)),
                    profile=Profile.objects.get(pk=choice(profile_ids)),
                    like_flag=choice([True, False])
                )
                like.save()
            except Exception:
                pass

    @staticmethod
    def fill_answers_likes(n):
        profile_ids = list(Profile.objects.values_list('id', flat=True))
        answer_ids = list(Answer.objects.values_list('id', flat=True))

        for i in range(n):
            try:
                like = AnswerLike(
                    answer=Answer.objects.get(pk=choice(answer_ids)),
                    profile=Profile.objects.get(pk=choice(profile_ids)),
                    like_flag=choice([True, False])
                )
                like.save()
            except Exception:
                pass

    def fill_db(self, n):
        self.fill_profiles(n)
        self.fill_tags(n)
        self.fill_questions(n*10)
        self.fill_answers(n*100)
        self.fill_questions_likes(n*200)
        self.fill_answers_likes(n*200)