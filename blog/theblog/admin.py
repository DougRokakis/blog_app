from django.contrib import admin
from .models import Post, Category, Profile, Comment

admin.site.register(Post) #allows our blog post to be accessible from the admin area after migrating the server
admin.site.register(Category) #allows our categories to be accessible from the admin area after migrating the server
admin.site.register(Profile) #allows our profiles to be accessible from the admin area after migrating the server
admin.site.register(Comment) #allows our profiles to be accessible from the admin area after migrating the server
