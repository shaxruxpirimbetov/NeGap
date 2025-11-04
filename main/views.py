from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from user.serializers import UserSerializer
from .models import Message, Answer
from .serializers import MessageSerializer, AnswerSerializer


class HomeView(View):
	def get(self, request):
		context = {}
		if request.user.id:
			messages = Message.objects.filter(receiver=request.user)
			messages = MessageSerializer(messages, many=True).data
			answers = Answer.objects.filter(receiver=request.user)
			answers = AnswerSerializer(answers, many=True).data
			context["messages"] = messages
			context["answers"] = answers
		return render(request, "index.html", context)


class MessageView(View):
	def get(self, request):
		user_id = request.GET.get("user_id")
		if not user_id:
			return HttpResponse("User not found")
		user = User.objects.filter(first_name=user_id).first()
		if not user:
			return HttpResponse("User not found")
		
		if int(user.id) == int(request.user.id):
			return render(request, "send_message.html", {"alert_err": "Нельзя отправить сообщение самому себе"})
		
		print(user_id, request.user.id)
		user = UserSerializer(user).data
		return render(request, "send_message.html", {"user": user})

	def post(self, request):
		user_id = request.POST.get("user_id")
		text = request.POST.get("text")

		if not text:
			return render(request, "send_message.html", {"error": "text are required"})

		user = User.objects.filter(id=user_id).first()
		if not user:
			return HttpResponse("User not found")

		Message.objects.create(sender=request.user if request.user.id else None, receiver=user, text=text)
		return redirect("main:home")


class AnswerView(View):
	def get(self, request):
		message_id = request.GET.get("message_id")
		if not message_id:
			return HttpResponse("message not found")

		message = Message.objects.filter(id=message_id).first()
		if not message:
			return HttpResponse("message not found")
		message = MessageSerializer(message).data
		return render(request, "answer.html", {"message": message})

	def post(self, request):
		message_id = request.POST.get("message_id")
		receiver_id = request.POST.get("receiver_id")
		text = request.POST.get("text")

		message = Message.objects.filter(id=message_id).first()
		if not message:
			return HttpResponse("message not found")

		Answer.objects.create(message=message, text=text, receiver_id=receiver_id)
		message.is_answered = True
		message.save()
		return redirect("main:home")