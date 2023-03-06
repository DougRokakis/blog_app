from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
from .forms import PostForm, EditForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

# def home(request):
#     return render(request, 'home.html', {})

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():#if a post has already been liked by this user
        post.likes.remove(request.user)#remove the like status if clicked
        liked = False #change the liked status to False
    else:#if a post hasn't already been liked by this user
        post.likes.add(request.user)#add the like status if clicked
        liked = True #change the liked status to True
    return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))

class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    # ordering = ['-id'] lazy method or sorting posts by most recent post
    ordering = ['-publication_date']

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all() #collects all of the names of the categories and stores them in the 'cat_menu' variable
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['cat_menu']= cat_menu
        return context

def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats.replace('-', ' ')) #.replace() added to aid in amending error where user adds category with spaces. Slugify is used on the html page to ensure that a hyphen is placed to erase the empty spaces and replace is used to ensure that the hyphen is then replaced with the original space when processing the post.
    return render(request, 'categories.html', {'cats':cats.title().replace('-', ' '), 'category_posts':category_posts})

class ArticleDetailView(DetailView):
    model = Post
    template_name='article_details.html'

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all() #collects all of the names of the categories and stores them in the 'cat_menu' variable
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        current_post_id = get_object_or_404(Post, id=self.kwargs['pk'])#storing the id of the post currently on.
        total_likes= current_post_id.total_likes()#uses total_likes function from models.py to take total likes from current_post_id variable

        liked = False
        if current_post_id.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['total_likes']= total_likes
        context["liked"] = liked
        return context

class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name='add_comment.html'
    # success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('article-detail', kwargs={'pk': self.kwargs['pk']})

class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name='add_post.html'
    # fields = '__all__'
    # fields = ['title', 'body']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class AddCategoryView(CreateView):
    model = Category
    # form_class = PostForm
    template_name='add_category.html'
    fields = '__all__'
    # fields = ['title', 'body']

class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'update_post.html'
    # fields = ['title', 'title_tag', 'body']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class DeletePostView(DeleteView):
    model = Post
    template_name='delete_post.html'
    success_url = reverse_lazy('home')
