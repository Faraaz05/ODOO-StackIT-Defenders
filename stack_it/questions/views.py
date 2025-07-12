from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from .models import Question, Answer, Vote
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models.manager import Manager
    from django.db.models.query import QuerySet


@login_required
def ask_question(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        tags = request.POST.get('tags')
        Question.objects.create(  # type: ignore
            title=title,
            description=description,
            tags=tags,
            author=request.user
        )
        return redirect('landing')
    return render(request, 'ask_question.html')


def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=question).annotate(  # type: ignore
        upvotes=Sum('vote__value', filter=Q(vote__vote_type='answer', vote__value=1)),
        downvotes=Sum('vote__value', filter=Q(vote__vote_type='answer', vote__value=-1))
    ).order_by('-upvotes')

    # Handle answer submission
    if request.method == 'POST' and request.user.is_authenticated:
        description = request.POST.get('description')
        if description:
            Answer.objects.create(  # type: ignore
                question=question,
                author=request.user,
                description=description
            )
            return redirect('question_detail', question_id=question.id)

    # Annotate question upvotes/downvotes
    question_upvotes = Vote.objects.filter(question=question, vote_type='question', value=1).count()  # type: ignore
    question_downvotes = Vote.objects.filter(question=question, vote_type='question', value=-1).count()  # type: ignore
    question_net_votes = question_upvotes - question_downvotes  # Subtract downvotes from upvotes
    
    # Calculate net votes for answers
    for answer in answers:
        upvotes = answer.upvotes if answer.upvotes is not None else 0
        downvotes = abs(answer.downvotes) if answer.downvotes is not None else 0  # Use absolute value for downvotes
        answer.net_votes = upvotes - downvotes  # Subtract downvotes from upvotes
    
    tags_list = [t.strip() for t in question.tags.split(',') if t.strip()]
    
    # Get user votes for answers
    answer_votes = {}
    if request.user.is_authenticated:
        answer_votes = Vote.objects.filter(  # type: ignore
            user=request.user,
            vote_type='answer',
            answer__in=answers
        )
        answer_votes = {v.answer_id: v.value for v in answer_votes}
    
    return render(request, 'question_detail.html', {
        'question': question,
        'answers': answers,
        'question_net_votes': question_net_votes,
        'tags_list': tags_list,
        'answer_votes': answer_votes,
})

@require_POST
@login_required
def vote(request):
    from .models import Question, Answer, Vote
    import json

    data = json.loads(request.body)
    vote_type = data.get('vote_type')  # 'question' or 'answer'
    obj_id = data.get('id')
    value = int(data.get('value'))  # +1 or -1

    if vote_type == 'question':
        obj = Question.objects.get(id=obj_id)  # type: ignore
        
        # Get existing vote for this user and question
        existing_vote = Vote.objects.filter(  # type: ignore
            user=request.user, 
            vote_type='question', 
            question=obj
        ).first()
        
        if existing_vote:
            if existing_vote.value == value:
                # User is clicking the same button - remove the vote
                existing_vote.delete()
                user_vote = 0
            else:
                # User is changing their vote - update it
                existing_vote.value = value
                existing_vote.save()
                user_vote = value
        else:
            # Create new vote
            Vote.objects.create(  # type: ignore
                user=request.user,
                vote_type='question',
                question=obj,
                value=value
            )
            user_vote = value
        
        upvotes = Vote.objects.filter(question=obj, vote_type='question', value=1).count()  # type: ignore
        downvotes = Vote.objects.filter(question=obj, vote_type='question', value=-1).count()  # type: ignore
        return JsonResponse({
            'upvotes': upvotes, 
            'downvotes': downvotes,
            'user_vote': user_vote
        })
    elif vote_type == 'answer':
        obj = Answer.objects.get(id=obj_id)  # type: ignore
        
        # Get existing vote for this user and answer
        existing_vote = Vote.objects.filter(  # type: ignore
            user=request.user, 
            vote_type='answer', 
            answer=obj
        ).first()
        
        if existing_vote:
            if existing_vote.value == value:
                # User is clicking the same button - remove the vote
                existing_vote.delete()
                user_vote = 0
            else:
                # User is changing their vote - update it
                existing_vote.value = value
                existing_vote.save()
                user_vote = value
        else:
            # Create new vote
            Vote.objects.create(  # type: ignore
                user=request.user,
                vote_type='answer',
                answer=obj,
                value=value
            )
            user_vote = value
        
        upvotes = Vote.objects.filter(answer=obj, vote_type='answer', value=1).count()  # type: ignore
        downvotes = Vote.objects.filter(answer=obj, vote_type='answer', value=-1).count()  # type: ignore
        return JsonResponse({
            'upvotes': upvotes, 
            'downvotes': downvotes,
            'user_vote': user_vote
        })
    return JsonResponse({'error': 'Invalid vote'}, status=400)