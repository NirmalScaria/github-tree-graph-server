from django.shortcuts import render
from django.http import HttpResponse
import requests
import os
def index(request):
    return render(request, 'github_tree_graph_server/index.html')

def githubTreeGraphServer(request):
    return render(request, 'github_tree_graph_server/github_tree_graph.html')

def authorisationSuccess(request):
    return render(request, 'github_tree_graph_server/authorisation_success.html')

def authorizeCode(request):
    code = request.GET.get('code')
    clientId = "91ddd618eba025e4104e"
    redirectUrl = "https://scaria.dev/github-tree-graph/success/"
    requestUrl = "https://github.com/login/oauth/access_token"
    requestBody = {
        "client_id": clientId,
        "client_secret": os.environ.get("GITHUB_CLIENT_SECRET"),
        "code": code,
        "redirect_uri": redirectUrl
    }
    headers = {
        "Accept": "application/json"
    }
    response = requests.post(requestUrl, data=requestBody, headers=headers)
    # accessToken = response.json()['access_token']
    responseText = response.text
    return(HttpResponse(responseText))
