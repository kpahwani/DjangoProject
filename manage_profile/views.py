from django.shortcuts import render
from django.utils import timezone
from .models import Users, Logins

# Create your views here.


def index(request):
    return render(request, 'index.html')


def sign_up(request):
    return render(request, 'sign_up.html')


def login(request):
    if request.method == 'POST':
        userObj = request.POST
        if not Users.objects.filter(email_id__exact=userObj['email'], password__exact=userObj['password']).exists():
            if Users.objects.filter(email_id__exact=userObj['email']).exists():
                userDetails = Users.objects.get(email_id__exact=userObj['email'])
                loginDetails = Logins.objects.get(user__email_id=userDetails.email_id)
                if loginDetails.failed_attempts>=3:
                    if timezone.now().min - loginDetails.last_login.min > timezone.timedelta(minutes=5):
                        loginDetails.failed_attempts = 0
                        loginDetails.last_login = timezone.now()
                        loginDetails.save()
                        return render(request, 'index.html', {'message': 'Login Failed. Try again'})
                    loginDetails.last_login = timezone.now()
                    loginDetails.save()
                    return render(request, 'index.html', {'message': 'User blocked for 5 mins'})
                else:
                    loginDetails.failed_attempts += 1
                    loginDetails.save()
                    return render(request, 'index.html', {'message': 'Login Failed. Try again'})
            else:
                return render(request, 'index.html', {'message': 'Incorrect Email/Password'})
        else:
            loginDetails = Logins(user=Users.objects.get(email_id__exact=userObj['email']),failed_attempts=0, last_login=timezone.now())
            loginDetails.save()
            return render(request, 'home.html', {'email': userObj['email']})
    else:
        return render(request, 'index.html')


def resigter(request):
    if request.method == 'POST':
        userObj = request.POST
        if not Users.objects.filter(email_id__exact=userObj['email']).exists():
            Users.objects.create(first_name=userObj['first_name'], last_name=userObj['last_name'], email_id=userObj['email'], password=userObj['password'],
                            secondary_email_id=userObj['secondary_email'], country=userObj['country'])
            return render(request, 'index.html',
                          {'message': '{} Log-in to continue'.format(userObj['email'])})
        else:
            return render(request, 'index.html', {'message': 'User with email {} already exists'.format(userObj['email'])})
    else:
        return render(request, 'index.html')
