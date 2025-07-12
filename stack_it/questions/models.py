from django.db import models
from django.conf import settings

class Question(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()  # Will store HTML from rich text editor
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=200)  # Comma-separated tags for simplicity

    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()  # HTML from rich text editor
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.author.username} on {self.question.title}"

class Vote(models.Model):
    VOTE_TYPE = (
        ('question', 'Question'),
        ('answer', 'Answer'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=VOTE_TYPE)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
    value = models.SmallIntegerField()  # +1 for upvote, -1 for downvote

    class Meta:
        unique_together = ('user', 'vote_type', 'question', 'answer')