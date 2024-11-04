from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
# Create your views here.
def call(request):
    if request.user.is_authenticated:
        template = loader.get_template('call.html')
        return HttpResponse(render(request, 'call.html'))
    else:
        return HttpResponse(render(request, "please_login.html"))