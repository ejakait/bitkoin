from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response,RequestContext
from .forms import RegForm,LoginForm
from django.http import HttpResponseRedirect,HttpResponse
from .models import UserPr
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout


def home(request):
    context = RequestContext(request)
    return render_to_response("index.html", context,)

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/')
    else:
        form = RegForm(request.POST or None)
        if form.is_valid():
            user = User.objects.create_user( username = form.cleaned_data['username'],email = form.cleaned_data['email'],password = form.cleaned_data['password'])
            BitKoin = UserPr(user = user, email = form.cleaned_data['email'],)  
            BitKoin.save()
            return HttpResponseRedirect('/profile/')
        else:
            return render_to_response("registration_form.html",locals(),context_instance = RequestContext(request))
    
def LoginRequest(request):
    logged_in = False
    form = LoginForm(request.POST or None)
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user is not None:
            if user.is_active:
                login(request,user)
                logged_in = True
                return HttpResponseRedirect('/profile/')
            else:
                return HttpResponse("Please try and login again")
        else:
            return HttpResponse('You dont seem to have an account, please sign up to go on')
    
    else:
        return render_to_response("login.html",locals(),context_instance = RequestContext(request),)
        
def LogoutRequest(request):
    logout(request)
    return HttpResponseRedirect('/')