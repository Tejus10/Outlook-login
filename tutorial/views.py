from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from tutorial.auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token, get_token
from tutorial.graph_helper import get_user
from .models import ques
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required

def home(request):
  context = initialize_context(request)

  return render(request, 'tutorial/home.html', context)

def initialize_context(request):
  context = {}
  context.update(csrf(request))
  # question = ques.objects.all()
  # context['questions'] = question
  # Check for any errors in the session
  error = request.session.pop('flash_error', None)

  if error != None:
    context['errors'] = []
    context['errors'].append(error)

  # Check for user in the session
  context['user'] = request.session.get('user', {'is_authenticated': False})
  return context  

def sign_in(request):
  # Get the sign-in URL
  sign_in_url, state = get_sign_in_url()
  # Save the expected state so we can validate in the callback
  request.session['auth_state'] = state
  # Redirect to the Azure sign-in page
  return HttpResponseRedirect(sign_in_url)

def callback(request):
  # Get the state saved in session
  expected_state = request.session.pop('auth_state', '')
  # Make the token request
  token = get_token_from_code(request.get_full_path(), expected_state)

  # Get the user's profile
  user = get_user(token)

  # Save token and user
  store_token(request, token)
  store_user(request, user)

  return HttpResponseRedirect(reverse('home'))

def sign_out(request):
  # Clear out the user and token
  remove_user_and_token(request)

  return HttpResponseRedirect(reverse('home'))  


def ask(request):
  context = initialize_context(request)
  try:
    request.session['user']
  except:
    return HttpResponseRedirect(reverse('signin'))
  else:
    return render(request, 'tutorial/ask.html', context)

def search_ques(request):
  if request.method == 'POST':
    search_text = request.POST['search_text']
    all_ques = ques.objects.filter(question__contains=search_text)
    all_ques |= ques.objects.filter(asked_by__contains=search_text)
  else:
    search_text = ''
    all_ques = []  
  
  return render(request, 'tutorial/ajax_search.html', { 'all_ques': all_ques } )    

def my_ques(request):
  context = initialize_context(request)
  try:
    request.session['user']
  except:
    return HttpResponseRedirect(reverse('signin'))
  else:
    all_ques = ques.objects.filter(asked_by=request.session['user']['name'])
    context['all_ques'] = all_ques
    return render(request, 'tutorial/my_ques.html', context )  


def all(request):
  question = ques.objects.all().order_by('-date_asked')
  context = {}
  context = initialize_context(request)
  context.update(csrf(request))
  context['questions'] = question
  return render(request, 'tutorial/all.html', context)


def sort_ques(request):
  if request.method == 'POST':
    search_text = str(request.POST['search_text'])
    if search_text=='latest':
      all_ques = ques.objects.all().order_by('-date_asked')
    elif search_text=='oldest':
      all_ques = ques.objects.all().order_by('date_asked')
    elif search_text=='mlike':
      all_ques = ques.objects.all().order_by('-likes')
    elif search_text=='llike':
      all_ques = ques.objects.all().order_by('likes')      
        
  else:
    search_text = ''
    all_ques = []  
  
  return render(request, 'tutorial/ajax_sort.html', { 'all_ques': all_ques } )  