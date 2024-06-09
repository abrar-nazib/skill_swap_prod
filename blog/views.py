import json
import datetime
import time
from webbrowser import get
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import CreateArt
from .models import Article, Comment
from django.contrib import messages
import markdown2
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.contrib.auth import get_user_model
from django.db.models import Q
from accounts.forms import StudentProfileForm, FacultyProfileForm



def get_markdown_edit_user(user):
  if user.education:
    user.education = markdown2.markdown(user.education, extras=['tables'])
  if user.experience:
    user.experience = markdown2.markdown(user.experience, extras=['tables'])
  if user.research_activities:
    user.research_activities = markdown2.markdown(user.research_activities, extras=['tables'])
  if user.membership:
    user.membership = markdown2.markdown(user.membership, extras=['tables'])
  if user.publication:
    user.publication = markdown2.markdown(user.publication, extras=['tables'])
  if user.award:
    user.award = markdown2.markdown(user.award, extras=['tables'])
  if user.contact:
    user.contact = markdown2.markdown(user.contact, extras=['tables'])
  return user

def home(request):
  allArticles = Article.objects.all().order_by('-upvote')

  return render(request, 'home.html', {
    "title": "Home",
    "articles": allArticles[:3]
  })

def faculty(reqest):
  facultyUsers = get_user_model().objects.filter(is_faculty = True)
  return render(reqest, 'faculty.html', {
    'members': facultyUsers,
    "title": "Faculty Members"
  })

def profile(request, id=None):
  if id :
    # Check if any user is found with the id
    try:
      user = get_user_model().objects.get(pk = id)
    except:
      # 404
      return render(request, '404.html')
    allArticles = Article.objects.filter(owner = user)
    print(user)
    return render(request, 'profile.html', {
      "title": user.username,
      "articles": allArticles,
      "user": get_markdown_edit_user(user)
    })
  else:
    allArticles = Article.objects.filter(owner = request.user)
    print(request.user)
    return render(request, 'profile.html', {
      "title": request.user.username,
      "articles": allArticles,
      "user": get_markdown_edit_user(request.user)
    })
    
    
@login_required
def updateProfile(request):

  # update profile
  if request.method == 'POST':
    if request.user.is_faculty:
      form = FacultyProfileForm(request.POST, request.FILES, instance=request.user)
    else:
      form = StudentProfileForm(request.POST, request.FILES, instance=request.user)
    if form.is_valid():
      form.save()
      messages.success(request, 'Profile Updated successfully ^_^')
      return HttpResponseRedirect(reverse('blog:profile'))
  else:
    if request.user.is_faculty:
      form = FacultyProfileForm(instance=request.user)
    else:
      form = StudentProfileForm(instance=request.user)
  
  return render(request, 'update_profile.html', {
    'form': form
  })
  
# Create your views here.
def index(request):
  if 'q' in request.GET and request.GET['q'] != '':
    q = request.GET['q']
    mutliQ = Q(Q(title__icontains = q) | Q(desc__icontains = q))
    articles = Article.objects.filter(mutliQ)
    message = f"All You need About \"{q}\""
  else :
    articles = Article.objects.all()
    message = False
  return render(request, 'index.html', {
    'articles': articles,
    'search': message,
  })

@login_required
def add(request):
  if request.method == "POST":
    form = CreateArt(request.POST, request.FILES)
    if form.is_valid():
      data = form.cleaned_data
      article = Article(owner = request.user, title = data['title'], artImage = data['artImage'], content = data['content'], desc = data['desc'], category = data['category'])
      article.save()
      messages.success(request, 'Article added successfully ^_^')
      return HttpResponseRedirect(reverse('blog:index'))
    
    return render(request, 'add.html', {
      'error': 'Not valid Data!',
      'form': CreateArt(),
      'mode': 'Create',
      })
    
  return render(request, 'add.html', {
    'form': CreateArt(),
    'mode': 'Create',
  })

def categories(request):
  return render(request, 'categories.html')

# single post
def singleArt(request, id):
  art = Article.objects.get(pk= id)
  comments = Comment.objects.filter(article = art).all()
  return render(request, 'singleArt.html', {
    'post': art,
    'content': markdown2.markdown(art.content,extras=['tables', 'fenced-code-blocks']),
    'comments': comments,
  })
  
  
  
# handle 404
def error404(request, exception):
  return render(request, '404.html')

@login_required
@csrf_exempt
def save(request, id):
  if request.method == "POST":
    getArticle = Article.objects.get(pk = id)
    if request.user in getArticle.bookmarks.all():
      getArticle.bookmarks.remove(request.user)
      return JsonResponse({"message": "removed"})
    else:
      getArticle.bookmarks.add(request.user)
      return JsonResponse({"message": "added"})
    

@login_required
def bookmarks(request):
  return render(request, 'bookmarks.html', {
    'postsMarked': Article.objects.filter(bookmarks = request.user).all(),
  })
  

def category(request, name):
  targetArticles = []
  allArticles = Article.objects.all()
  for art in allArticles:
    for cat in art.category:
      if (cat == name):
        targetArticles.append(art)
  
  return render(request, 'category.html', {
    'title': name,
    'targetArticle': targetArticles,
  })
  
@login_required 
@csrf_exempt
def voting(request, id):
  targtArticle = Article.objects.get(pk = id)
  if request.user.is_authenticated:
    if request.method == "PUT":
      if request.user in targtArticle.upvote.all():
        targtArticle.upvote.remove(request.user)
        return JsonResponse({'messege': 'downvote', 'count': targtArticle.upvote.count()})
      else:
        targtArticle.upvote.add(request.user)
        return JsonResponse({'messege': 'upvote', 'count': targtArticle.upvote.count()})
  
  else:
    return HttpResponseRedirect(reverse('index'))
  
  
  
@login_required
@csrf_exempt
def delete(request, id):
  targtArticle = Article.objects.get(pk = id)
  if request.user.is_authenticated and targtArticle.owner == request.user:
    if request.method == "POST":
      targtArticle.delete()
    return JsonResponse({'message': 'deleted'})
  else:
    return HttpResponseRedirect(reverse('index'))
    
@login_required
def update(request, id):
  targetArticle = Article.objects.get(pk = id)
  form = CreateArt(instance=targetArticle)
  if request.method == "POST":
    form = CreateArt(request.POST, request.FILES, instance=targetArticle)
    if form.is_valid():
      form.save()
      messages.success(request, 'Article Updated successfully ^_^')
      return HttpResponseRedirect(reverse('blog:index'))
    else:
      return render(request, 'add.html', {
        'form': form,
        'mode': 'Update',
        })
  return render(request, 'add.html', {
    'form': form,
    'mode': 'Update',
  })


@login_required
@csrf_exempt
def addComment(request, id):
  if request.user.is_authenticated:
    if request.method == "POST":
      targetArticle = Article.objects.get(pk = id)
      data = json.loads(request.body)
      content = data.get('comment')
      if content == '':
        return HttpResponseRedirect(reverse('blog:singleArt', kwargs={'id':id}))
      newComment = Comment(owner = request.user, article = targetArticle, content = content)
      newComment.save()
      return JsonResponse({
        'content': newComment.content, 
        'owner': request.user.username, 
        'created': newComment.created, 
        'numbComments': Comment.objects.filter(article = targetArticle).count()
        })
  return HttpResponseRedirect(reverse('blog:singleArt', kwargs={'id':id}))