from django.urls import path
from .views import college_ai_assistant

urlpatterns = [
    path('', college_ai_assistant, name='college_ai_assistant' ),
]