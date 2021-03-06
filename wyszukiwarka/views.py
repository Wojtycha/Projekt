from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from .models import Klienci

def addUser(request):
   return render(request, 'addUser.html') 

def loginUser(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)
      if form.is_valid():
         user = form.get_user()
         login(request,user)
         return redirect('search/')
      else:
         messages.info(request, 'Login lub hasło się nie zgadzają')
   else:
      form = AuthenticationForm()
   return render(request, 'login.html')


def searchBar(request):
   result = Klienci.objects.all()

   if request.method == 'POST':
      query = request.POST['search']

      if query:

         match = Klienci.objects.filter(
            Q(Numer_klienta__icontains = query) |
            Q(Imię__icontains = query) |
            Q(Nazwisko__icontains = query)
         )

         if match:
            return render(request, 'searchBar.html', {'sr':match, 'Klienci':result})
         else:
            messages.error(request, 'Nie znaleziono danych.')
      else:
         return redirect('search')


   return render(request, 'searchBar.html', {'Klienci':result})
