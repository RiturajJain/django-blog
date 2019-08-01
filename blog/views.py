from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def home(request):
    context = {
        "posts": Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {})

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'    #<app_name>.<model_name>_list.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'    #<app_name>.<model_name>_list.html
    context_object_name = 'posts'
    #ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']   #<app_name>.<model_name>_form.html

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']   #<app_name>.<model_name>_form.html

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'   #<app_name>.<model_name>_confirm_delete.html

    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        else:
            return False
