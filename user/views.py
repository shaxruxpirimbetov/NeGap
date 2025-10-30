from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout


class RegisterView(View):
	def get(self, request):
		return render(request, "auth/register.html")
	
	def post(self, request):
		username = request.POST.get("username")
		password = request.POST.get("password")
		
		if not all([username, password]):
			return render(request, "form.html", {"error": "username and password are refunded"})
		
		user = User.objects.filter(username=username).first()
		if user:
			return render(request, "auth/register.html", {"error": "username already exists"})
		user = User.objects.create_user(username=username, password=password)
		login(request, user)
		return redirect("main:home")


class LoginView(View):
	def get(self, request):
		return render(request, "auth/login.html")

	def post(self, request):
		username = request.POST.get("username")
		password = request.POST.get("password")
		
		if not all([username, password]):
			return render(request, "auth/login.html", {"error": "username and password are refunded"})
		
		user = User.objects.filter(username=username).first()
		if not user:
			return render(request, "auth/login.html", {"error": "user not found"})
		
		if check_password(password, user.password):
			login(request, user)
			return redirect("main:home")

		return render(request, "auth/login.html", {"error": "password not match"})


class LogoutView(View):
	def get(self, request):
		return render(request, "confirm.html", {"message": "Logout?"})

	def post(self, request):
		logout(request)
		return redirect("main:home")