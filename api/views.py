from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse  
from .models import *
import json  
from datetime import datetime
from django.forms.models import model_to_dict
import moviepy.editor as moviepy
import os

# --------------------
def getValidDict(object):
  dict = model_to_dict(object)
  try:
    dict['avatar'] = dict['avatar'].url
  except:
    dict['avatar'] = None
  return dict

def getPostById(id, posts, user_of_avatar = False):
  for post in posts:
    if post['id'] == int(id):
      if user_of_avatar:
        post['avatar'] = str(user_of_avatar.avatar)
      else: pass
      return post

def getUpdatePosts(data, post, posts):
  for element in data:
    try:
      post[element] = json.loads(data[element])
    except: 
      post[element] = data[element]
  posts[posts.index(post)] = post
  return posts

def getAllPosts():
  allPosts = []
  for user in User.objects.all():
    allPosts = [*allPosts, *json.loads(user.posts)]
  return allPosts

def getAllUsers():
  users = list(User.objects.all())
  for user in users:
    users[users.index(user)] = getValidDict(user)
  return users

def findPostsWithTitle(title, user=False):
  posts = []
  for user in User.objects.all():
    for post in json.loads(user.posts):
      if title.lower() in post['title'].lower():
        post['user'] = {'name': user.name, 'avatar': str(user.avatar)} if user else None
        posts.append(post)
  return posts

def findExtension(path):
  return path[-6:].split('.')[1]

def getAvatars(users):
  avatars = {}
  for user in users:
    avatars[user] = str(User.objects.get(name = user).avatar)
  return avatars

# --------------------
class LoginView(APIView):
  def post(self, request):
    try:
      user = User.objects.get(name=request.data['name'])
      if user.password == request.data['password']:
        return Response(getValidDict(user))
      else:
        return Response('PASSWORD')
    except User.DoesNotExist:
      return Response('NAME')
    except Exception as error:
      print(error)
      return Response('Error')
  
class RegisterView(APIView):
  def post(self, request):
    try:
      User.objects.get(name=request.data['name'])
      return Response('NAME')
    except:
      user = User.objects.create(name = request.data['name'], password = request.data['password'])
      return Response(getValidDict(user))
    

# --------------------------
class UsersApi(APIView):
  def get(self, request):
    return Response(getAllUsers())

class UserApi(APIView):
  def get(self, request, name):
    try:
      user = User.objects.get(name = name)
      return Response(getValidDict(user))
    except Exception as error:
      if str(error) == 'User matching query does not exist.':
        return Response('Wrong user')
      else:
        print(error)
        return Response('Error')
      
  def put(self, request, name):
    try:
      user = User.objects.get(name = name)
      for element in request.data:
        if request.data[element] != 'undefined':
          user.__dict__[element] = request.data[element]
      user.save()
      return Response(getValidDict(user))
    except Exception as error:
      print(error)
      return Response('Wrong data')
      
class UserLineApi(APIView):
  def get(self, request, name):
    try:
      user = User.objects.get(name = name)
      line_of_posts = []
      for subscription in json.loads(user.subscriptions):
        subscription_user = User.objects.get(name = subscription)
        for post in json.loads(subscription_user.posts):
          if not(user.name in post['tops']) and not(user.name in post['bottoms']):
            post['user'] = {'name': subscription_user.name, 'avatar': str(subscription_user.avatar)}
            line_of_posts.append(post)
      return Response(line_of_posts)
    except Exception as error:
      if str(error) == 'User matching query does not exist.':
        return Response('Wrong user')
      else:
        print(error)
        return Response('Error')

class SearchUserApi(APIView):
  def get(self, request, name):
    searchedUsers = []
    for user in getAllUsers():
      if name in user['name']:
        searchedUsers.append(user)
    return Response(searchedUsers)
  
class SearchAvatars(APIView):
  def post(self, request):
    return Response(getAvatars(json.loads(request.body)))
      
class UserPosts(APIView):
  def get(self, request, name):
    try:
      user = User.objects.get(name = name)
      return Response(json.loads(model_to_dict(user)['posts']))
    except Exception as error:
      if str(error) == 'User matching query does not exist.':
        return Response('Wrong user')
      else:
        print(error)
        return Response('Error')
      
  def post(self, request, name):
    emptyPost = {
      'id': 1,
      'title': '',
      'content': '',
      'preview': '',
      'tops': [],
      'bottoms': [],
      'date': str(datetime.now().date())
    }
    try:
      user = User.objects.get(name=name)
      userPosts = json.loads(user.posts)
      if userPosts:
        emptyPost['id'] = list(reversed(userPosts))[0]['id'] + 1
        user.posts = json.dumps(sorted([*userPosts, emptyPost], key = lambda element: element['id']))
        user.save()
      else:
        user.posts = json.dumps([emptyPost])
        user.save()
      return Response(emptyPost)
    except Exception as error:
      if str(error) == 'User matching query does not exist.':
        return Response('Wrong user')
      else:
        print(error)
        return Response('Error')
      
class UserPost(APIView):
  def get(self, request, name, id):
    try:
      user = User.objects.get(name = name)
      return Response(getPostById(id, json.loads(user.posts), user))
    except User.DoesNotExist:
      return Response('NAME')
  
  def put(self, request, name, id):
    user = User.objects.get(name = name)
    posts = json.loads(user.posts)
    post = getPostById(id, posts)
    posts = getUpdatePosts(request.data, post, posts)
    user.posts = json.dumps(posts)
    user.save()
    return Response(posts)
  
  def delete(self, request, name, id):
    user = User.objects.get(name = name)
    posts = json.loads(user.posts)
    post = getPostById(id, posts)
    posts.pop(posts.index(post))
    user.posts = json.dumps(posts)
    user.save()
    return Response(posts)

# -----------------------------------------------------

class PostView(APIView):
  def get(self, request, title):
    getUser = False
    try:
      request.query_params['user']
      getUser = True
    except:
      pass
    return Response(findPostsWithTitle(title, getUser))

# -----------------------------------------------------

class MediaImagesView(APIView):
  def post(self, request):
    new_media = MediaImages.objects.create(media=request.data['media'])
    return Response(new_media.media.name)

class MediaVideosView(APIView):
  def post(self, request):
    new_media = MediaVideos.objects.create(media=request.data['media'])
    media_path = new_media.media.path
    media_extension = findExtension(media_path)
    video = moviepy.VideoFileClip(media_path)
    video.write_videofile(media_path.replace(media_extension, 'webm'))
    os.remove(media_path)
    new_media.media = media_path.replace(media_extension, 'webm')
    return Response(new_media.media.name)
