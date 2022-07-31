from django.shortcuts import render
from django.http import HttpResponse
import pyrebase
import requests
import os
import time

firebaseConfig = {
  "apiKey": "AIzaSyAfYmATG88Dsjhe2f-Q8YrMVW1ZRvY6azA",
  "authDomain": "github-tree-graph.firebaseapp.com",
  "databaseURL": "https://github-tree-graph-default-rtdb.firebaseio.com",
  "projectId": "github-tree-graph",
  "storageBucket": "github-tree-graph.appspot.com",
  "messagingSenderId": "258623901486",
  "appId": "1:258623901486:web:ce7004507c707d4f9674bf",
  "measurementId": "G-NT7FRH0S6Q"
}

adminEmail = os.environ.get("ADMIN_EMAIL")
adminPassword = os.environ.get("ADMIN_PASSWORD")

firebase = pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()
database = firebase.database()
adminUser = authe.sign_in_with_email_and_password(adminEmail, adminPassword)

def index(request):
    return render(request, 'github_tree_graph_server/index.html')

def githubTreeGraphServer(request):
    return render(request, 'github_tree_graph_server/github_tree_graph.html')

def authorisationSuccess(request):
    return render(request, 'github_tree_graph_server/authorisation_success.html')

def authorizeCode(request):
    code = request.GET.get('code')
    clientId = "91ddd618eba025e4104e"
    redirectUrl = "https://scaria.dev/github-tree-graph/authorize/"
    requestUrl = "https://github.com/login/oauth/access_token"
    browserToken = request.GET.get('browsertoken')
    if(browserToken == None):
        return(HttpResponse('{"ERROR": "No browser token provided"}'))
    requestBody = {
        "client_id": clientId,
        "client_secret": os.environ.get("GITHUB_CLIENT_SECRET"),
        "code": code,
        "redirect_uri": redirectUrl
    }
    headers = {
        "Accept": "application/json"
    }
    response = requests.post(requestUrl, data=requestBody, headers=headers).json()
    if("access_token" not in response):
        database.child("TokenData").child(browserToken).child("isAuthenticated").set(False, adminUser['idToken'])
        database.child("TokenData").child(browserToken).child("githubToken").set("FAIL", adminUser['idToken'])
        database.child("TokenData").child(browserToken).child("time").set(int(round(time.time())), adminUser['idToken'])
        return(HttpResponse('{"ERROR": "' + str(response) + '"}'))
    accessToken = response['access_token']
    userData = getUserData(accessToken)
    database.child("TokenData").child(browserToken).child("githubToken").set(accessToken, adminUser['idToken'])
    database.child("TokenData").child(browserToken).child("isAuthenticated").set(True, adminUser['idToken'])
    database.child("TokenData").child(browserToken).child("time").set(int(round(time.time())), adminUser['idToken'])
    database.child("TokenData").child(browserToken).child("userData").set(userData, adminUser['idToken'])
    return(HttpResponse("SUCCESS"))

def getUserData(accessToken):
    requestUrl = "https://api.github.com/user"
    headers = {
        "Authorization": "token " + accessToken
    }
    response = requests.get(requestUrl, headers=headers).json()
    return(response)