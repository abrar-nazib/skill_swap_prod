from . import views
from django.urls import path
app_name = 'blog'
urlpatterns = [
    path("", views.home, name="home"),
    path("profile", views.profile, name="profile"),
    path("profile/<int:id>", views.profile, name="specific_profile"),
    path("updateProfile", views.updateProfile, name="updateProfile"),
    path("home", views.home, name="home"),
    path('feed', views.index, name='index'),
    path('add', views.add, name='add'),
    path('faculty', views.faculty, name='faculty'),
    path('categories', views.categories, name='categories'),
    path('articles/<str:id>', views.singleArt, name='singleArt'),
    path('bookmarks', views.bookmarks, name= "bookmarks"),
    path('category/<str:name>', views.category, name = 'category'),
    path('update/<str:id>', views.update, name= "update"),
    # APIs
    path('save/<str:id>', views.save, name="save"),
    path('category/save/<str:id>', views.save, name="save"),
    path('vote/<str:id>', views.voting, name='vote'),
    path('category/vote/<str:id>', views.voting, name='vote'),
    path('delete/<str:id>', views.delete, name='delete'),
    path('category/delete/<str:id>', views.delete, name='delete'),
    path('articles/comment/<str:id>', views.addComment, name='addComment'),
    
]
