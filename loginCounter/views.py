from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.http import Http404

from loginCounter.models import Users
import json

SUCCESS = 1 # success return code
ERR_BAD_CREDENTIALS = -1 # cannot find username/password pair
ERR_USER_EXISTS = -2 # trying to add a user that already exists
ERR_BAD_USERNAME = -3 # empty or longer than max username length
ERR_BAD_PASSWORD = -4 # longer than max password length
MAX_USERNAME_LENGTH = 128 # max length of username
MAX_PASSWORD_LENGTH = 128 # max length of password


def index(request):
    return HttpResponse("Hello, world. You're at the user index.")

# Create your views here.
def login(request):
    # return HttpResponse("Hello, world. This is a login.")
    # takes two arguments (username and password)
    # if can't find username, or username doesn't match password, give an error
    # else, add 1 to the counter, and direct to the next page
    data = json.loads(request.body)
    username = data['username']
    password = data['pwd']
    user = Users.objects.filter(uid=username)
    if user.count() == 0:
    	return HttpResponse(json.dumps({ 'errCode' : ERR_BAD_CREDENTIALS}), content_type="application/json")
    if user[0].pid != password:
    	return HttpResponse(json.dumps({ 'errCode' : ERR_BAD_CREDENTIALS}), content_type="application/json")
    user = Users.objects.get(uid=username)
    user.count += 1
    user.save()
    return HttpResponse(json.dumps({ 'errCode' : SUCCESS, 'count' : user.count}), content_type="application/json")

"""
def login(request):
	return render(request, 'loginCounter/client.html')
"""

"""
def add(request):
	return 1
"""

def add(request):
    # return HttpResponse("Hello, world. This is an add.")
    # if username not already in the db, add username and password, perform login
    data = json.loads(request.body)
    username = data['username']
    password = data['pwd']
    user = Users.objects.filter(uid=username)
    if user.count() != 0:
    	return HttpResponse(json.dumps({ 'errCode' : ERR_USER_EXISTS}), content_type="application/json")
    if len(username) > MAX_USERNAME_LENGTH or len(username) == 0:
    	return HttpResponse(json.dumps({ 'errCode' : ERR_BAD_USERNAME}), content_type="application/json")
    if len(password) > MAX_PASSWORD_LENGTH:
    	return HttpResponse(json.dumps({ 'errCode' : ERR_BAD_PASSWORD}), content_type="application/json")
    user = Users(uid=username, pid=password)
    user.save()
    return HttpResponse(json.dumps({ 'errCode' : SUCCESS, 'count' : user.count}), content_type="application/json")
