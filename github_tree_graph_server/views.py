from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'github_tree_graph_server/index.html')

def githubTreeGraphServer(request):
    return render(request, 'github_tree_graph_server/github_tree_graph.html')

def authorisationSuccess(request):
    return render(request, 'github_tree_graph_server/authorisation_success.html')