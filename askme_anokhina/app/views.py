from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator
from . import models

def paginate(objects_list, request, per_page=10):
    if isinstance(per_page, int) == False or per_page < 0: per_page = 10
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page

#@require_GET
def index(request):
    page = paginate(models.QUESTIONS, request, 4)
    context = {'is_auth': False, 'page': page}
    return render(request, 'index.html', context=context)

def question(request, question_id: int):
    question_item = models.QUESTIONS[question_id]
    page = paginate(models.ANSWERS, request, 4)
    context = {'question': question_item, 'is_auth': False, 'page': page}
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
    context = {'is_auth': False, 'questions': models.QUESTIONS, 'tag': tag_name}
    return render(request, 'tag.html', context=context)