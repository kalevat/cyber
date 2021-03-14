from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Account
from django.db import connection

def addView(request):
	valid=request.GET.get('validation')
	name=request.GET.get('user')
	vac_date=request.GET.get('vacdate')
	address=request.GET.get('email')
	b=User.objects.filter(username=name).count()
	if b==0:
		a = User.objects.create_user(f"{name}",email=f"{address}",password="1234")
		Account.objects.create(user_id=a.pk,validation=valid,date=vac_date)

	return redirect('/') 

def changeView(request):
	valid=request.POST.get('validation')
	name=request.POST.get('user')
	#b=User.objects.filter(username=name)
	#c=Account.objects.get(user_id=b[0].id)
	#c.validation=valid
	#c.save()
	sql = "UPDATE pages_account SET validation=%s WHERE user_id= (SELECT id FROM auth_user WHERE username='%s')" %(valid,name)
	cursor = connection.cursor()
	cursor.execute(sql)
	return redirect('/') 


def normalView(request):
	if request.user.is_authenticated:
		return JsonResponse({'username': request.user.username, 'validation': request.user.account.validation, 'date': request.user.account.date})
	else:
		return JsonResponse({'username': 'anonymous', 'balance': 0})


@login_required
def homePageView(request):
	a=User.objects.filter(username=request.user)
	staff=a[0].is_staff
	if staff==True:
		accounts = Account.objects.exclude()
	else:
		accounts = Account.objects.filter(user=request.user)
	return render(request, 'pages/index.html', {'accounts': accounts,'staff': staff})
