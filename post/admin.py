from django.contrib import admin
from .models import Post, Hashtag, Tag #관리자 페이지에서 import 이후 적힌 값들을 사용할 수 있도록 함

# Register your models here.
admin.site.register(Post)

class HashtagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(Tag, TagAdmin)

