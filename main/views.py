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
		if not request.user.is_anonymous:
			messages = Message.objects.filter(receiver=request.user)
			messages = MessageSerializer(messages, many=True).data
			my_messages = Message.objects.filter(sender=request.user)
			my_messages = MessageSerializer(my_messages, many=True).data
			answers = Answer.objects.filter(message_sender=request.user)
			answers = AnswerSerializer(answers, many=True).data
			context["messages"] = messages
			context["my_messages"] = my_messages
			context["answers"] = answers
			return render(request, "aindex.html", context)

		return render(request, "index.html", context)


class MessageView(View):
	def get(self, request):
		user_id = request.GET.get("user_id")
		vmessage_id = request.GET.get("vmessage_id")
		url = request.GET.get("url")
		token = url.split("=")[1] if url else user_id
		
		if vmessage_id:
			message = Message.objects.filter(id=vmessage_id).first()
			if not message:
				return HttpResponse("<h1>Message not found</h1>")
			message = MessageSerializer(message).data
			return render(request, "view-message.html", {"message": message})
		
		if not user_id and not token:
			return render(request, "send_message.html", {"warning": "user is not defined"})

		user = User.objects.filter(first_name=token).first()
		if not user:
			return render(request, "send_message.html", {"error": "Пользователь с такой ссылкой на найден", "warning": "user is not defined"})
		
		if int(user.id) == request.user.id:
			return render(request, "send_message.html", {"alert_err": "Нельзя отправить сообщение самому себе"})

		user = UserSerializer(user).data
		if request.user.is_anonymous:
			return render(request, "send_message.html", {"user": user, "warning": "You cant see answer without login"})
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
			return redirect("main:home")
		
		message = Message.objects.filter(id=message_id).first()
		message = MessageSerializer(message).data
		return render(request, "answer.html", {"message": message})

	def post(self, request):
		message_id = request.POST.get("message_id")
		message_sender_id = request.GET.get("message_sender_id")
		text = request.POST.get("text")
		
		if not text:
			return render(request, "answer.html", {"error": "Ответ должен быть больше 0 символов"})

		message = Message.objects.filter(id=message_id).first()
		if not message:
			return HttpResponse("message not found")

		Answer.objects.create(message=message, text=text, message_sender=message.sender)
		message.is_answered = True
		message.save()
		return redirect("main:home")