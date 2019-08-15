from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import Post, Comment
from .forms import CommentOnPostForm
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

# Using post_detail_view instead of this to add comments section
class PostDetailView(DetailView):
    model = Post

# Adding Comment section to the Post
def post_detail_view(request, pk):

    post = get_object_or_404(Post, id=pk)
    comments = Comment.objects.filter(post=post).order_by('-date_commented')

    if request.method == "POST":

        # Update the comment
        # if 'edit' in request.POST:
        #     comment = Comment.objects.get(id=int(request.POST['edit']))
        #     form = CommentOnPostForm(instance=comment)

        if request.is_ajax():
            comment = Comment.objects.get(id=int(request.POST["id"]))
            form = CommentOnPostForm(instance=comment)

        elif 'update' in request.POST:
            comment = Comment.objects.get(id=int(request.POST['update']))
            form = CommentOnPostForm(request.POST, instance=comment)
            if request.user.is_authenticated and form.is_valid():
                form.save()
                form = CommentOnPostForm()

        # Delete the comment
        elif 'delete' in request.POST:
            comment = Comment.objects.get(id=int(request.POST['delete']))
            comment.delete()

        # Add New Comment
        else:
            form = CommentOnPostForm(request.POST)
            if request.user.is_authenticated and form.is_valid():
                form.instance.user = request.user
                form.instance.post = post
                form.save()

            else:
                messages.info(request, f'You are not logged in! Please login to comment')

            return redirect('post-detail', pk=pk)

    else:
        form = CommentOnPostForm()

    context = {
        "object": post,
        "comments": comments,
        "form": form
    }
    print("Been to Ajax");
    return render(request, 'blog/post_detail.html', context)

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
