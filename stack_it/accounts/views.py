from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, LoginForm
from questions.models import Question
from django.core.paginator import Paginator
from django.db.models import Count, Q, Sum, F, Value as V
from django.db.models.functions import Coalesce
from questions.models import Vote
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models.manager import Manager
    from django.db.models.query import QuerySet


def landing(request):

    q = request.GET.get('q', '')
    tag = request.GET.get('tag', '')
    sort = request.GET.get('sort', 'new')

    questions = Question.objects.all()  # type: ignore

    if q:
        questions = questions.filter(title__icontains=q)
    if tag:
        questions = questions.filter(tags__icontains=tag)

    # Annotate with net votes and answer count
    questions = questions.annotate(
        upvotes=Coalesce(Sum('vote__value', filter=Q(vote__vote_type='question', vote__value=1)), V(0)),
        downvotes=Coalesce(Sum('vote__value', filter=Q(vote__vote_type='question', vote__value=-1)), V(0)),
        answer_count=Coalesce(Count('answers'), V(0))
    )
    
    # Add net votes calculation
    for question in questions:
        question.net_votes = question.upvotes - abs(question.downvotes)

    # Sorting
    if sort == 'new':
        questions = questions.order_by('-created_at')
    elif sort == 'old':
        questions = questions.order_by('created_at')
    elif sort == 'upvotes':
        questions = questions.order_by('-upvotes')
    elif sort == 'downvotes':
        questions = questions.order_by('upvotes')

    paginator = Paginator(questions, 10)
    page_number = request.GET.get('page')
    questions_page = paginator.get_page(page_number)

    # For tag display
    for q in questions_page:
        q.tags_list = [t.strip() for t in q.tags.split(',') if t.strip()]

    # For pagination links
    querystring = ''
    for key in ['q', 'tag', 'sort']:
        value = request.GET.get(key)
        if value:
            querystring += f'&{key}={value}'

    user_votes = {}
    if request.user.is_authenticated:
        votes = Vote.objects.filter(  # type: ignore
            user=request.user,
            vote_type='question',
            question__in=[q.id for q in questions_page]
        )
        user_votes = {v.question_id: v.value for v in votes}

    return render(request, 'landing.html', {
        'username': request.user.username if request.user.is_authenticated else None,
        'questions': questions_page,
        'querystring': querystring,
        'user_votes': user_votes,
    })

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'user'  # Ensure role is always 'user'
            user.save()
            login(request, user)
            return redirect('landing')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('landing')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('landing')