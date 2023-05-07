from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.db import connection
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect



def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def DOMBasedXSS(request):
    #posts = Post.objects.all()
    if request.method == 'POST':
        post_id = request.POST.get('post')
        post = Post.objects.get(id=post_id)
        print(post_id)
        return render(request, 'blog/test.html', {'post': post})
    else:
        posts = Post.objects.all()
        return render(request, 'blog/DOMBasedXSS.html', {'posts': posts})

def ReflectedXSS(request):
    model = Post
    query = request.GET.get('q')
    results = ''
    if query:
        results = Post.objects.filter(Q(title=query) | Q(content=query))

    return render(request, 'blog/ReflectedXSS.html', {'results': results, 'query': query})

def PermanentXSS(request):
    return render(request, 'blog/PermanentXSS.html')

def AllXSS(request):
    return render(request, 'blog/AllXSS.html')

def AllSQLi(request):
    return render(request, 'blog/AllSQLi.html')

def BlindSQLi(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = None
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM auth_user WHERE username = '" + username + "'"
            )
            row = cursor.fetchone()
            if row:
                # Check the password
                print(row)
                hashed_password = row[1]
                # if check_password(password, hashed_password):
                # Return the user object
                user = User(row[0], row[1], row[2])

        # user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog-home')
        else:
            return render(request, 'blog/BlindSQLi.html', {'error': 'Invalid login credentials'})
    else:
        return render(request, 'blog/BlindSQLi.html')

def SQLi(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = None
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM auth_user WHERE username = '" + username + "'"
            )
            row = cursor.fetchone()
            if row:
                # Check the password
                hashed_password = row[1]
                # if check_password(password, hashed_password):
                # Return the user object
                user = User(row[0], row[1], row[2])

        # user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog-home')
        else:
            return render(request, 'blog/SQLi.html', {'error': 'Invalid login credentials'})
    else:
        return render(request, 'blog/SQLi.html')


def AllBonus(request):
    return render(request, 'blog/AllBonus.html')

def BruteForce(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog-BruteForce')
        else:
            return render(request, 'blog/BruteForce.html', {'error': 'Invalid login credentials'})

    return render(request, 'blog/BruteForce.html')

def UserEnumeration(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog-UserEnumeration')
        else:
            try:
                user = User.objects.get(username=username)
                messages.error(request, 'Invalid password', extra_tags='password')
            except User.DoesNotExist:
                messages.error(request, 'Invalid username', extra_tags='username')
    return render(request, 'blog/UserEnumeration.html')




def ClickJacking(request):
    return render(request, 'blog/ClickJacking.html')

def CSRF(request):

    return render(request, 'blog/CSRF.html')

def search(request):
    model = Post
    query = request.GET.get('q')
    results = 'aa'
    if query:
        results = Post.objects.filter(Q(title_icontains=query) | Q(content_icontains=query))

    return render(request, 'blog/post_list.html', {'results': results, 'query': query})

def posts(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/posts.html', context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('blog-home')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'blog/change_password.html', {'form': form})