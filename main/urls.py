from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("message/", views.MessageView.as_view(), name="message"),
    path("answer/", views.AnswerView.as_view(), name="answer"),
]