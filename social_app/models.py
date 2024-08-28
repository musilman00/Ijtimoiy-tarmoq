from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    # Foydalanuvchi uchun profildan foydalanamiz
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)  # Foydalanuvchining bio ma'lumotlari
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Profil rasmi
    location = models.CharField(max_length=100, blank=True, null=True)  # Foydalanuvchining joylashuvi

    class Meta:
        db_table = "profile"  # Ma'lumotlar bazasida profil uchun jadval nomi
    def __str__(self):
        return self.user.username  # Profilni foydalanuvchi nomi bilan ko'rsatamiz

class FriendRequest(models.Model):
    # Do'stlik so'rovlarini saqlash uchun model
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)  # So'rov yuboruvchi foydalanuvchi
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)  # So'rov qabul qiluvchi foydalanuvchi
    is_accepted = models.BooleanField(default=False)  # So'rov qabul qilinganmi yoki yo'qmi

    class Meta:
        db_table = "friend_request"  # Ma'lumotlar bazasida do'stlik so'rovlarini saqlash uchun jadval nomi
    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username}"  # So'rov yuboruvchi va qabul qiluvchi foydalanuvchi nomlari

class Message(models.Model):
    # Xabarlarni saqlash uchun model
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)  # Xabar yuboruvchi foydalanuvchi
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)  # Xabar qabul qiluvchi foydalanuvchi
    content = models.TextField()  # Xabar matni
    timestamp = models.DateTimeField(auto_now_add=True)  # Xabar yuborilgan vaqti

    class Meta:
        db_table = "message"  # Ma'lumotlar bazasida xabarlarni saqlash uchun jadval nomi
    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username}"  # Xabar yuboruvchi va qabul qiluvchi foydalanuvchi nomlari

class Post(models.Model):
    # Postlarni saqlash uchun model
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Post yaratuvchisi
    content = models.TextField()  # Post matni
    timestamp = models.DateTimeField(auto_now_add=True)  # Post yaratilgan vaqti

    class Meta:
        db_table = "post"  # Ma'lumotlar bazasida postlarni saqlash uchun jadval nomi
    def __str__(self):
        return f"Post by {self.user.username}"  # Postni yaratgan foydalanuvchi nomi

class Comment(models.Model):
    # Izohlarni saqlash uchun model
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)  # Izoh qoldirilgan post
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Izoh qoldirgan foydalanuvchi
    content = models.TextField()  # Izoh matni
    timestamp = models.DateTimeField(auto_now_add=True)  # Izoh qoldirilgan vaqti

    class Meta:
        db_table = "comment"  # Ma'lumotlar bazasida izohlarni saqlash uchun jadval nomi
    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.id}"  # Izohni qoldirgan foydalanuvchi va post ID

class Like(models.Model):
    # Like'larni saqlash uchun model
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)  # Like qilingan post
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Like qilgan foydalanuvchi

    class Meta:
        db_table = "like"  # Ma'lumotlar bazasida like'larni saqlash uchun jadval nomi
    def __str__(self):
        return f"{self.user.username} liked Post {self.post.id}"  # Like qilgan foydalanuvchi va post ID

class Follow(models.Model):
    # Kuzatish (follow) ma'lumotlarini saqlash uchun model
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)  # Kuzatuvchi foydalanuvchi
    followed_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)  # Kuzatilayotgan foydalanuvchi

    class Meta:
        unique_together = ('user', 'followed_user')  # Har bir foydalanuvchi boshqa foydalanuvchiga faqat bitta kuzatuvchini qo'shishi mumkin
        db_table = "follow"  # Ma'lumotlar bazasida kuzatuvchi ma'lumotlarini saqlash uchun jadval nomi
    def __str__(self):
        return f"{self.user.username} follows {self.followed_user.username}"  # Kuzatuvchi va kuzatilayotgan foydalanuvchi nomlari
