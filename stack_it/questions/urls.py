from django.urls import path
from .views import ask_question,question_detail,vote

urlpatterns = [
    path('ask/', ask_question, name='ask_question'),
    path('<int:question_id>/', question_detail, name='question_detail'),
    path('vote/', vote, name='vote'),  # AJAX voting endpoint


]