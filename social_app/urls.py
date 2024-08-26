from django.urls import path, re_path  # URL path va regex path uchun
from . import views  # Ro'yxatdan o'tish viewlarini import qilamiz

urlpatterns = [
    path('register/', views.register, name='register'),  # Ro'yxatdan o'tish
    path('login/', views.login_user, name='login'),  # Login qilish
    path('logout/', views.logout_user, name='logout'),  # Logout qilish
    path('send_message/<slug:username>/', views.send_message, name='send_message'),  # Xabar yuborish
    path('get_messages/', views.get_messages, name='get_messages'),  # Xabarlarni olish
    path('posts/', views.get_posts, name='get_posts'),  # Barcha postlarni olish
    path('posts/create/', views.create_post, name='create_post'),  # Yangi post yaratish
    path('posts/<int:post_id>/comment/', views.add_comment, name='add_comment'),  # Postga izoh qoldirish
    path('posts/<int:post_id>/like/', views.like_post, name='like_post'),  # Postga like qo'shish
    path('search/users/', views.search_users, name='search_users'),  # Foydalanuvchilarni qidirish
    path('search/posts/', views.search_posts, name='search_posts'),  # Postlarni qidirish
    path('feed/', views.get_feed, name='get_feed'),  # Yangiliklar lentasi
    path('profile/', views.profile_view, name='profile_view'),  # Foydalanuvchi profilini ko'rsatish
    path('follow/<slug:username>/', views.follow_user, name='follow_user'),  # Foydalanuvchini kuzatishni boshlash
    path('unfollow/<slug:username>/', views.unfollow_user, name='unfollow_user'),  # Foydalanuvchini kuzatishni to'xtatish
]

