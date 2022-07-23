#from atexit import register
from django.contrib import admin
from .models import *

# Register your models here.

# class PostAdmin(admin.ModelAdmin):
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         # extract post.id from request to filter FK dropdown 
#         # https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.formfield_for_foreignkey
#         get = str(request)
#         print('get =' + get)
#         sub1 = '/admin/network/post/'
#         sub2 = '/change/'
#         idx1 = get.index(sub1)
#         idx2 = get.index(sub2)
#         print('get =' + get + ' idx1 =' + str(idx1) + ' idx2 =' + str(idx2))
#         res = get[idx1 + len(sub1) : idx2]
#         type(res)
#         print('res =' + str(res))
#         if db_field.name == "likes":
#             kwargs["queryset"] = Like.objects.filter(post_id=res)
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)

#     # raw_id_fields = ("likes",)  -- doesn't work on FK, only on MTM

admin.site.register(User)
admin.site.register(Post)#, PostAdmin)
admin.site.register(Follower)
admin.site.register(Like)
