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
			answers = Answer.objects.filter(receiver=request.user)
			answers = AnswerSerializer(answers, many=True).data
			context["messages"] = messages
			context["my_messages"] = my_messages
			context["answers"] = answers
			return render(request, "aindex.html", context)

		return render(request, "index.html", context)


class MessageView(View):
	def get(self, request):
		user_id = request.GET.get("user_id")
		url = request.GET.get("url")
		token = url.split("=")[1] if url else user_id

		if not user_id and not token:
			return render(request, "send_message.html", {"warning": "user is not defined"})

		print(token)
		user = User.objects.filter(first_name=token).first()
		if not user:
			return HttpResponse("User not found")

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
		answered_id = request.GET.get("answered_id")
		is_empty = request.GET.get("is_empty")

		if is_empty == "true" and message_id:
			message = Message.objects.filter(id=message_id).first()
			message = MessageSerializer(message).data
			user = User.objects.filter(id=message["receiver"]).first()
			return render(request, "answer_view.html", {"message": message, "user": user})

		if not message_id and not answered_id:
			return HttpResponse(f"<h1>message not found</h1>")

		if answered_id:
			answered = Answer.objects.filter(id=answered_id).first()
			if not answered:
				return HttpResponse("Not found 404")

			message = Message.objects.filter(id=answered.message.id).first()
			answered = AnswerSerializer(answered).data
			message = MessageSerializer(message).data
			return render(request, "answer_view.html", {"message": message, "answer": answered})

		message = Message.objects.filter(id=message_id).first()
		if not message:
			return HttpResponse("message not found")

		if not message.sender:
			return render(request, "answer_view.html", {"message": message, "is_sender_none": True})

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