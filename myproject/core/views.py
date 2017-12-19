from django.contrib.auth import login, authenticate
#from django.contrib.auth.forms import UserCreationForm
from core.forms import SignUpForm
from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from core.tokens import account_activation_token
from django.template.loader import render_to_string


# Create your views here.
'''
def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('home')
	else:
		form = SignUpForm()
	return render(request, 'signup.html', {'form': form})

'''

'''
def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()
			user.profile.birth_date = form.cleaned_data.get('birth_date')
			user.save()
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username = user.username, password = raw_password)
			login(request, user)
			return redirect('home')
	else:
		form = SignUpForm()

	return render(request, 'signup.html', {'form' : form})
'''

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save(commit = False)
			user.is_active = False
			user.save()
			current_site = get_current_site(request)
			subject = 'Activate Your MySite Account'
			tokenVal = account_activation_token.make_token(user)
			message = render_to_string('account_activation_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
			})
			print (message)
			#user.email_user(subject, message)
			return redirect('account_activation_sent')
	else:
		form = SignUpForm()
	return render(request, 'signup.html', {'form': form})

def account_activation_sent(request):
	return render(request, 'account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')
