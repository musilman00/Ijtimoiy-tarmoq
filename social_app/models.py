from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Profil rasmi
    location = models.CharField(max_length=100, blank=True, null=True)  # Foydalanuvchi joylashuvi

    class Meta:
        db_table = "profile"  # Yaxshiroq standart nom
    def __str__(self):
        return self.user.username

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)  # So'rov qabul qilinganmi yoki yo'qmi

    class Meta:
        db_table = "friend_request"  # Yaxshiroq standart nom
    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username}"

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()  # Xabar matni
    timestamp = models.DateTimeField(auto_now_add=True)  # Xabar yuborilgan vaqt

    class Meta:
        db_table = "message"  # Yaxshiroq standart nom
    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username}"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Post yaratuvchisi
    content = models.TextField()  # Post matni
    timestamp = models.DateTimeField(auto_now_add=True)  # Post yaratilgan vaqti

    class Meta:
        db_table = "post"  # Yaxshiroq standart nom
    def __str__(self):
        return f"Post by {self.user.username}"

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)  # Izoh postga bog'lanadi
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Izoh qoldirgan foydalanuvchi
    content = models.TextField()  # Izoh matni
    timestamp = models.DateTimeField(auto_now_add=True)  # Izoh vaqti

    class Meta:
        db_table = "comment"  # Yaxshiroq standart nom
    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.id}"

class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)  # Like qilingan post
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Like qilgan foydalanuvchi

    class Meta:
        db_table = "like"  # Yaxshiroq standart nom
    def __str__(self):
        return f"{self.user.username} liked Post {self.post.id}"

class Follow(models.Model):
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)  # Kuzatuvchi foydalanuvchi
    followed_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)  # Kuzatilayotgan foydalanuvchi

    class Meta:
        unique_together = ('user', 'followed_user')  # Har bir foydalanuvchi boshqa foydalanuvchiga faqat bitta kuzatuvchini qo'shishi mumkin
        db_table = "follow"  # Yaxshiroq standart nom
    def __str__(self):
        return f"{self.user.username} follows {self.followed_user.username}"
