from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator
#from . import models
from app.models import Profile, Tag, Question, QuestionLike, Answer, AnswerLike

def paginate(objects_list, request, per_page=10):
    if isinstance(per_page, int) == False or per_page < 0: per_page = 10
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page

@require_GET
def index(request):
    recent_questions = Question.objects.get_recent()
    page = paginate(recent_questions, request, 4)
    popular_tags = Tag.objects.popular_tags()
    context = {'is_auth': False, 'page': page, 'popular_tags': popular_tags}
    return render(request, 'index.html', context=context)

def hot(request):
    hot_questions = Question.objects.get_hot()
    page = paginate(hot_questions, request, 4)
    popular_tags = Tag.objects.popular_tags()
    context = {'is_auth': False, 'page': page, 'popular_tags': popular_tags}
    return render(request, 'hot_questions.html', context=context)

def question(request, question_id: int):
    question_item = get_object_or_404(Question, pk=question_id)
    answers = Answer.objects.by_question(question_id).values()
    page = paginate(answers, request, 4)
    popular_tags = Tag.objects.popular_tags()
    context = {'question': question_item, 'is_auth': False, 'page': page, 'popular_tags': popular_tags}
    return render(request, 'question.html', context=context)

def ask(request):
    return render(request, 'ask.html')

def login(request):
    context = {'is_auth': False}
    return render(request, 'login.html', context=context)

def signup(request):
    context = {'is_auth': False}
    return render(request, 'signup.html', context=context)

def settings(request):
    context = {'is_auth': False}
    return render(request, 'settings.html', context=context)

def tag(request, tag_name: str):
    questions = Question.objects.by_tag(tag_name)
    page = paginate(questions, request, 4)
    popular_tags = Tag.objects.popular_tags()
    context = {'is_auth': False, 'tag': tag_name, 'page': page, 'popular_tags': popular_tags}
    return render(request, 'tag.html', context=context)
