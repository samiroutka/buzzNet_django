from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *

class LoginApi(APIView):
  def post(self, request):
    try:
      login_user = User.objects.get(name=request.data['name'])
      if login_user.password == request.data['password']:
        return Response('OK')
      else:
        return Response('PASSWORD')
    except:
      return Response('NAME')
  
class RegisterApi(APIView):
  def post(self, request):
    try:
      User.objects.get(name=request.data['name'])
      print('wrong name')
      return Response('NAME')
    except:
      User.objects.create(name = request.data['name'], password = request.data['password'])
      print('User has been created')
      return Response('OK')
