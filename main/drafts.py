class MessageView(View):
	def get(self, request):
		user_id = request.GET.get("user_id")
		vmessage_id = request.GET.get("vmessage_id")
		url = request.GET.get("url")
		try:
			token = url.split("=")[1] if url else user_id
		except:
			return render(request, "send_message.html", {"error": "Пользователь с такой ссылкой на найден", "warning": "user is not defined"})
		
		
		if vmessage_id:
			message = Message.objects.filter(id=vmessage_id).first()
			if not message:
				return HttpResponse("<h1>Message not found</h1>")
			
			message = MessageSerializer(message).data
			if message["is_answered"]:
				answer = Answer.objects.filter(message_id=message["id"]).first()
				answer.is_seen = True
				answer.save()
				answer = AnswerSerializer(answer).data
				message["answer"] = answer
			message["is_my"] = True if message["sender"] == request.user.id else False
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
		