from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UserForm, FacultyProfileForm, StudentProfileForm, CustomUserCreationForm

# Create your views here.
def register(request):
  if request.method == 'POST':
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('/')
  else:
    form = CustomUserCreationForm()
  return render(request, 'registration/register.html', {
    'form': form
  })


@login_required
def profile(request):
  if request.user.is_faculty:
    form = FacultyProfileForm(instance=request.user)

  else:
    form = StudentProfileForm(instance=request.user)
  if request.method == 'POST':
    if request.is_faculty:
      form = FacultyProfileForm(request.POST, request.FILES, instance=request.user)
    else:
      form = StudentProfileForm(request.POST, request.FILES, instance=request.user)
    if form.is_valid():
      form.save()
  return render(request, 'profile.html', {
    'form': form
  })