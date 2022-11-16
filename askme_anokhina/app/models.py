from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, null=True, default='img/avatar_1.jpg', upload_to='static/img/%y/%m/%d/', verbose_name='avatar')

    def __str__(self):
        return self.user.username

class TagManager(models.Manager):
    def popular_tags(self):
        return self.order_by('-questions')[:5]

class Tag(models.Model):
    name = models.CharField(max_length=50)

    objects = TagManager()

    def __str__(self):
        return self.name

class QuestionLike(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    like_flag = models.BooleanField(default=True, verbose_name='like_dislike')

    def __str__(self):
        if self.like_flag: action = 'liked'
        else: action = 'disliked'
        return f"{self.profile.user.username} {action} {self.question.title}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            if self.like_flag: self.question.rating += 1
            else: self.question.rating -= 1
            self.question.save()
        super(QuestionLike, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.like_flag: self.question.rating -= 1
        else: self.question.rating += 1
        self.question.save()
        super(QuestionLike, self).delete(*args, **kwargs)
    
    def change_like_flag(self):
        if self.like_flag: self.question.rating += 2
        else: self.question.rating -= 2
        self.like_flag = not self.like_flag
        self.save()
        self.question.save()

class QuestionManager(models.Manager):
    def by_tag(self, tag: str):
        return self.filter(tags__name=tag).order_by('-creation_date')

    def get_hot(self):
        return self.order_by('-rating', '-creation_date')

    def get_recent(self):
        return self.order_by('-creation_date')

class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(null=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='questions')
    creation_date = models.DateField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, verbose_name='tags', related_name='questions')
    rating = models.IntegerField(default=0)

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def number_of_answers(self):
        return Answer.objects.filter(question_id=self.id).count()

class AnswerLike(models.Model):
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    like_flag = models.BooleanField(default=True, verbose_name='like_dislike')

    def __str__(self):
        if self.like_flag: action = 'liked'
        else: action = 'disliked'
        return f"{self.profile.user.username} {action} {self.answer.title}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            if self.like_flag: self.answer.rating += 1
            else: self.answer.rating -= 1
            self.answer.save()
        super(AnswerLike, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.like_flag: self.answer.rating -= 1
        else: self.answer.rating += 1
        self.answer.save()
        super(AnswerLike, self).delete(*args, **kwargs)
    
    def change_like_flag(self):
        if self.like_flag: self.answer.rating += 2
        else: self.answer.rating -= 2
        self.like_flag = not self.like_flag
        self.save()
        self.answer.save()

class AnswerManager(models.Manager):
    def by_question(self, pk: int):
        return self.filter(question_id=pk).order_by('-rating', '-creation_date')

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    title = models.CharField(max_length=100)
    text = models.TextField(null=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='answers')
    creation_date = models.DateField(blank=True, null=True)
    
    CORRECT = 'c'
    INCORRECT = 'i'

    STATUSES = [
        (CORRECT, 'Correct'), 
        (INCORRECT, 'Incorrect'), 
    ]
    status = models.CharField(max_length=1, choices=STATUSES)
    rating = models.IntegerField(default=0)

    objects = AnswerManager()

    def __str__(self):
        return self.title
