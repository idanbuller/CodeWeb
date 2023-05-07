from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)
from . import views
from .views import change_password

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('AllSQLi/', views.AllSQLi, name='blog-AllSQLi'),
    path('SQLi/', views.SQLi, name='blog-SQLi'),
    path('BlindSQLi/', views.BlindSQLi, name='blog-BlindSQLi'),
    path('BruteForce/', views.BruteForce, name='blog-BruteForce'),
    path('AllXSS/', views.AllXSS, name='blog-AllXSS'),
    path('DOMBasedXSS/', views.DOMBasedXSS, name='blog-DOMBasedXSS'),
    path('ReflectedXSS/', views.ReflectedXSS, name='blog-ReflectedXSS'),
    path('PermanentXSS/', views.PermanentXSS, name='blog-PermanentXSS'),
    path('AllBonus/', views.AllBonus, name='blog-AllBonus'),
    path('UserEnumeration/', views.UserEnumeration, name='blog-UserEnumeration'),
    path('ClickJacking/', views.ClickJacking, name='blog-ClickJacking'),
    path('CSRF/', views.CSRF, name='blog-CSRF'),
    path('search/', views.search, name='blog-search'),
    path('posts/', views.posts, name='blog-posts'),
    path('change-password/', change_password, name='change_password'),
]
