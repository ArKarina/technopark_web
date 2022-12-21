from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import auth
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
#from . import models
from app.forms import *
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

    if request.method == 'GET':
        answer_form = AnswerForm()
    elif request.method == 'POST':
        answer_form = AnswerForm(data=request.POST)
        if answer_form.is_valid():
            answer = Answer.objects.create(text=request.POST.get('text'),
                                            author=request.user.profile,
                                            question=question_item)
            answer.save()
            print(answer)
            if answer:
                return redirect(reverse('question', args=[answer.question.id]))
            else:
                answer_form.add_error(field=None, error='Failed to add answer!')
            
    
    context = {'question': question_item, 'page': page, 'popular_tags': popular_tags, 'form': answer_form}
    return render(request, 'question.html', context=context)


@login_required(login_url="/login")
def ask(request):
    print(request.POST)
    if request.method == 'GET':
        question_form = QuestionForm()
    elif request.method == 'POST':
        question_form = QuestionForm(data=request.POST)
        if question_form.is_valid():
            question = Question.objects.create(title=request.POST.get('title'),
                                            text=request.POST.get('text'),
                                            author=request.user.profile)
            question.tags.set(request.POST.get('tags'))
            question.save()
            print(question)

            if question:
                return redirect(reverse('question', args=[question.id]))
            else:
                question_form.add_error(field=None, error='Failed to create question!')
                return redirect(reverse('ask'))

    return render(request, 'ask.html', {'form' : question_form})


def login(request):
    print(request.GET)
    print(request.POST)

    if request.method == 'GET':
        user_form = LoginForm()
    elif request.method == 'POST':
        user_form = LoginForm(data=request.POST)
        if user_form.is_valid():
            user = auth.authenticate(**user_form.cleaned_data)       
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))
            else:
                user_form.add_error(field=None, error='Wrong username or password!')

    return render(request, "login.html", {'form': user_form})


def signup(request):
    if request.method == 'GET':
        user_form = RegistrationForm()

    if request.method == 'POST':
        user_form = RegistrationForm(data=request.POST)
        if user_form.is_valid():
            try:
                user = user_form.save()
            except:
                user = None
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))
            else:
                user_form.add_error(field=None, error='User saving error!')

    context = {'is_auth': False, 'form' : user_form}
    return render(request, 'signup.html', context=context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@require_http_methods(['GET', 'POST'])
def settings(request):
    print(request.GET)
    print(request.POST)
    popular_tags = Tag.objects.popular_tags()
    if request.method == 'GET':
        initial_data = model_to_dict(request.user)
        form = SettingsForm(initial=initial_data)
        #form = SettingsForm()
    elif request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('settings'))
        else:
            form.add_error(field=None, error='Failed to update profile!')
    else:
        form = None

    content = {'form': form, 'tags': popular_tags}

    return render(request, 'settings.html', content)


def tag(request, tag_name: str):
    questions = Question.objects.by_tag(tag_name)
    page = paginate(questions, request, 4)
    popular_tags = Tag.objects.popular_tags()
    context = {'is_auth': False, 'tag': tag_name, 'page': page, 'popular_tags': popular_tags}
    return render(request, 'tag.html', context=context)


@login_required
@require_POST
def likeQuestion(request):
    print(request.POST)
    question_id = request.POST['question_id']
    question = Question.objects.get(id=question_id)

    if request.POST['action'] == "like": action = True
    else: action = False

    try:
        like = QuestionLike.objects.get(question=question, profile=request.user.profile)
        print('1: ', question.rating)
        if like.like_flag == action:
            return JsonResponse({'new_rating': like.delete()})

        print('2: ', question.rating)
        like.change_like_flag()
        like.save()
        print('3: ', question.rating)
        return JsonResponse({'new_rating': question.rating})

    except QuestionLike.DoesNotExist:
        like = QuestionLike.objects.create(question=question, profile=request.user.profile, like_flag=action)
        like.save()
        return JsonResponse({'new_rating': question.rating})


@login_required
@require_POST
def likeAnswer(request):
    print(request.POST)
    answer_id = request.POST['answer_id']
    answer = Answer.objects.get(id=answer_id)

    if request.POST['action'] == "like": action = True
    else: action = False

    try:
        like = AnswerLike.objects.get(answer=answer, profile=request.user.profile)
        print('1: ', answer.rating)
        if like.like_flag == action:
            return JsonResponse({'new_rating': like.delete()})

        print('2: ', answer.rating)
        like.change_like_flag()
        like.save()
        print('3: ', answer.rating)
        return JsonResponse({'new_rating': answer.rating})

    except AnswerLike.DoesNotExist:
        like = AnswerLike.objects.create(answer=answer, profile=request.user.profile, like_flag=action)
        like.save()
        return JsonResponse({'new_rating': answer.rating})


@login_required
@require_POST
def correctAnswer(request):
    print(request.POST)
    answer_id = request.POST['answer_id']
    answer = Answer.objects.get(id=answer_id)
    if answer.question.author == request.user.profile:
        answer.change_status()
        answer.save()
        return HttpResponse({'new_status': answer.status})