from django.contrib import admin
from .models import Profile,Post,like_post,followersCount,Comment
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(like_post)
admin.site.register(Comment)
admin.site.register(followersCount)