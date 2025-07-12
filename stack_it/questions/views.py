from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Question

@login_required
def ask_question(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        tags = request.POST.get('tags')
        Question.objects.create(
            title=title,
            description=description,
            tags=tags,
            author=request.user
        )
        return redirect('landing')
    return render(request, 'ask_question.html')