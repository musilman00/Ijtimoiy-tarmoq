from django.urls import path
from . import views

urlpatterns = [
    # Foydalanuvchi profillarini olish va yangilash uchun URL'lar
    path('profile/<int:user_id>/', views.get_user_profile, name='get_user_profile'),  # Foydalanuvchi profilini olish
    path('profile/<int:user_id>/update/', views.update_user_profile, name='update_user_profile'),  # Foydalanuvchi profilini yangilash

    # Do'stlik so'rovlarini yuborish va qabul qilish uchun URL'lar
    path('friend-request/', views.send_friend_request, name='send_friend_request'),  # Do'stlik so'rovini yuborish
    path('friend-request/<int:request_id>/accept/', views.accept_friend_request, name='accept_friend_request'),  # Do'stlik so'rovini qabul qilish

    # Xabarlar yuborish va olish uchun URL'lar
    path('message/send/', views.send_message, name='send_message'),  # Xabar yuborish
    path('messages/', views.get_user_messages, name='get_user_messages'),  # Foydalanuvchining xabarlarini olish

    # Foydalanuvchining postlarini olish va post yaratish uchun URL'lar
    path('user/<int:user_id>/posts/', views.get_user_posts, name='get_user_posts'),  # Foydalanuvchining barcha postlarini olish
    path('post/create/', views.create_post, name='create_post'),  # Post yaratish

    # Postga izoh qoldirish va izohlarni olish uchun URL'lar
    path('post/<int:post_id>/comments/', views.get_post_comments, name='get_post_comments'),  # Postning barcha izohlarini olish
    path('comment/create/', views.create_comment, name='create_comment'),  # Postga izoh qoldirish

    # Postga like qo'yish va olish uchun URL'lar
    path('post/<int:post_id>/likes/', views.get_post_likes, name='get_post_likes'),  # Postning barcha like'larini olish
    path('like/', views.like_post, name='like_post'),  # Postga like qo'yish

    # Foydalanuvchini kuzatish va kuzatishni bekor qilish uchun URL'lar
    path('follow/', views.follow_user, name='follow_user'),  # Foydalanuvchini kuzatish
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),  # Foydalanuvchini kuzatishni bekor qilish

    # Foydalanuvchi kuzatuvchilarini va kuzatuvlarini olish uchun URL'lar
    path('user/<int:user_id>/followers/', views.get_user_followers, name='get_user_followers'),  # Foydalanuvchining barcha kuzatuvchilarini olish
    path('user/<int:user_id>/following/', views.get_user_following, name='get_user_following'),  # Foydalanuvchining kuzatayotganlarini olish

    # Login va logout uchun URL'lar
    path('login/', views.login_user, name='login_user'),  # Foydalanuvchini login qilish
    path('logout/', views.logout_user, name='logout_user'),  # Foydalanuvchini logout qilish

    # Parolni tiklash uchun URL'lar
    path('password/reset/', views.password_reset, name='password_reset'),  # Parolni tiklash
    path('/register/', views.register_user, name='register'),  # Royhatdan otish

]
