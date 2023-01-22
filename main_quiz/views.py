from django.shortcuts import render

def index(request):
    """The home page for mulipleChoice multiplication. Pass request object as parameter to render function, template as other parameter"""
    return render(request, 'main_quiz/index.html')