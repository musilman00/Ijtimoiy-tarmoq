from django.contrib import admin
from .models import Profile, FriendRequest, Message, Post, Comment, Like, Follow

admin.site.register(Profile)  # Profil modelini admin panelga qo'shish
admin.site.register(FriendRequest)  # Do'stlik so'rovlarini admin panelga qo'shish
admin.site.register(Message)  # Xabarlarni admin panelga qo'shish
admin.site.register(Post)  # Postlarni admin panelga qo'shish
admin.site.register(Comment)  # Izohlarni admin panelga qo'shish
admin.site.register(Like)  # Like'larni admin panelga qo'shish
admin.site.register(Follow)  # Kuzatishlarni admin panelga qo'shish
