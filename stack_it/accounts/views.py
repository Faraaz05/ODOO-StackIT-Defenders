from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
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
    
    # Add net votes calculation on the paginated results
    for question in questions_page:
        question.net_votes = question.upvotes + question.downvotes
        print(f"Question {question.id}: upvotes={question.upvotes}, downvotes={question.downvotes}, net_votes={question.net_votes}")

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
    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        
        # Validation
        if not username:
            errors['username'] = 'Username is required.'
        elif len(username) < 3:
            errors['username'] = 'Username must be at least 3 characters long.'
        elif len(username) > 150:
            errors['username'] = 'Username must be 150 characters or fewer.'
        else:
            # Check if username already exists
            from .models import User
            if User.objects.filter(username=username).exists():
                errors['username'] = 'A user with that username already exists.'
        
        if not email:
            errors['email'] = 'Email is required.'
        elif '@' not in email:
            errors['email'] = 'Enter a valid email address.'
        else:
            # Check if email already exists
            from .models import User
            if User.objects.filter(email=email).exists():
                errors['email'] = 'A user with that email already exists.'
        
        if not password1:
            errors['password1'] = 'Password is required.'
        elif len(password1) < 8:
            errors['password1'] = 'Password must be at least 8 characters long.'
        else:
            try:
                validate_password(password1)
            except ValidationError as e:
                errors['password1'] = '; '.join(str(msg) for msg in e.messages)
        
        if not password2:
            errors['password2'] = 'Please confirm your password.'
        elif password1 != password2:
            errors['password2'] = 'The two password fields didn\'t match.'
        
        # If no errors, create user
        if not errors:
            from .models import User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                role='user'
            )
            login(request, user)
            return redirect('landing')
    
    return render(request, 'signup.html', {
        'errors': errors,
        'form_data': request.POST if request.method == 'POST' else {}
    })

def login_view(request):
    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        # Validation
        if not username:
            errors['username'] = 'Username is required.'
        
        if not password:
            errors['password'] = 'Password is required.'
        
        # If no validation errors, try to authenticate
        if not errors:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('landing')
            else:
                errors['general'] = 'Invalid username or password.'
    
    return render(request, 'login.html', {
        'errors': errors,
        'form_data': request.POST if request.method == 'POST' else {}
    })

def logout_view(request):
    logout(request)
    return redirect('landing')