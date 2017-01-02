# Create your views here.
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView,RedirectView 
from django.views.generic.edit import FormView

from google.appengine.api import users
from google.appengine.ext import ndb

from blog.forms import BlogForm
from blog.models import Blog

class HomeView(TemplateView):

    template_name = "blog/index.html"
    
    def dispatch(self,request,*args,**kwargs):
        return super(HomeView,self).dispatch(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        blogs = Blog.query().order(-Blog.posted)
        context['blogs'] = blogs
        return context

class CreateBlogView(FormView):
    template_name = 'blog/post.html'
    form_class = BlogForm
    #success_url = "/"
    
    def dispatch(self,request,*args,**kwargs):
        return super(CreateBlogView,self).dispatch(request,*args,**kwargs)

    def get_success_url(self, **kwargs):         
        return reverse('blog_details', args = (self.blog.key.id(),))

    def form_valid(self, form):
        print "done"
        title = form.cleaned_data['title']
        slug = form.cleaned_data['slug']
        content = form.cleaned_data['content']
        email = users.get_current_user().email()
        
        self.blog = Blog(title=title,
                    slug=slug,
                    content=content,
                    author=email)
        self.blog.put()
        return super(CreateBlogView, self).form_valid(form)

class DetailView(TemplateView):
    template_name = "blog/detail.html"

    def dispatch(self,request,*args,**kwargs):
        return super(DetailView,self).dispatch(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        blogId = kwargs['id']
        key = ndb.Key('Blog', int(blogId))
        blog = key.get() 
        print blog
        context['blog'] = blog
        return context
