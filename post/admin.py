from django.contrib import admin
from .models import Post, Hashtag

# Register your models here.
admin.site.register(Post)

class HashtagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Hashtag, HashtagAdmin)


