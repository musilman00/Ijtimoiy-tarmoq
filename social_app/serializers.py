from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, FriendRequest, Message, Post, Comment, Like, Follow
import re

class UserSerializer(serializers.ModelSerializer):
    # User modeli uchun serializer
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # JSON formatda ko'rsatiladigan maydonlar

class ProfileSerializer(serializers.ModelSerializer):
    # Profil modeli uchun serializer
    user = UserSerializer()  # Foydalanuvchini boshqa serializer orqali ko'rsatamiz

    class Meta:
        model = Profile
        fields = ['user', 'bio', 'profile_picture', 'location']  # JSON formatda ko'rsatiladigan maydonlar

    def validate_bio(self, value):
        # Bio maydonini validatsiya qilish
        if len(value) > 300:
            raise serializers.ValidationError("Bio 300 ta belgidan oshmasligi kerak.")  # Bio uchun maksimal uzunlik
        return value

    def validate_location(self, value):
        # Location maydonini validatsiya qilish
        if not re.match(r'^[A-Za-z\s,]+$', value):
            raise serializers.ValidationError("Location faqat harflar, bo'sh joylar va verguldan iborat bo'lishi kerak.")  # Regulyar ifoda bilan tekshirish
        return value

class FriendRequestSerializer(serializers.ModelSerializer):
    # Do'stlik so'rovi modeli uchun serializer
    from_user = UserSerializer()  # So'rov yuboruvchini JSON formatda ko'rsatamiz
    to_user = UserSerializer()  # So'rov qabul qiluvchini JSON formatda ko'rsatamiz

    class Meta:
        model = FriendRequest
        fields = ['from_user', 'to_user', 'is_accepted']  # JSON formatda ko'rsatiladigan maydonlar

class MessageSerializer(serializers.ModelSerializer):
    # Xabar modeli uchun serializer
    sender = UserSerializer()  # Xabar yuboruvchini JSON formatda ko'rsatamiz
    recipient = UserSerializer()  # Xabar qabul qiluvchini JSON formatda ko'rsatamiz

    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'content', 'timestamp']  # JSON formatda ko'rsatiladigan maydonlar

    def validate_content(self, value):
        # Xabar matnini validatsiya qilish
        if not re.match(r'^[\w\s,.!?\'"-]+$', value):
            raise serializers.ValidationError("Xabar matni faqat harflar, raqamlar va belgilardan iborat bo'lishi kerak.")  # Regulyar ifoda bilan tekshirish
        return value

class PostSerializer(serializers.ModelSerializer):
    # Post modeli uchun serializer
    user = UserSerializer()  # Post yaratuvchini JSON formatda ko'rsatamiz

    class Meta:
        model = Post
        fields = ['user', 'content', 'timestamp']  # JSON formatda ko'rsatiladigan maydonlar

    def validate_content(self, value):
        # Post matnini validatsiya qilish
        if len(value) > 1000:
            raise serializers.ValidationError("Post matni 1000 ta belgidan oshmasligi kerak.")  # Post uchun maksimal uzunlik
        return value

class CommentSerializer(serializers.ModelSerializer):
    # Izoh modeli uchun serializer
    user = UserSerializer()  # Izoh qoldirgan foydalanuvchini JSON formatda ko'rsatamiz
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())  # Izoh qoldirilgan postni ko'rsatamiz

    class Meta:
        model = Comment
        fields = ['post', 'user', 'content', 'timestamp']  # JSON formatda ko'rsatiladigan maydonlar

    def validate_content(self, value):
        # Izoh matnini validatsiya qilish
        if len(value) > 500:
            raise serializers.ValidationError("Izoh matni 500 ta belgidan oshmasligi kerak.")  # Izoh uchun maksimal uzunlik
        return value

class LikeSerializer(serializers.ModelSerializer):
    # Like modeli uchun serializer
    user = UserSerializer()  # Like qilgan foydalanuvchini JSON formatda ko'rsatamiz
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())  # Like qilingan postni ko'rsatamiz

    class Meta:
        model = Like
        fields = ['post', 'user']  # JSON formatda ko'rsatiladigan maydonlar

class FollowSerializer(serializers.ModelSerializer):
    # Kuzatish (Follow) modeli uchun serializer
    user = UserSerializer()  # Kuzatuvchini JSON formatda ko'rsatamiz
    followed_user = UserSerializer()  # Kuzatilayotgan foydalanuvchini JSON formatda ko'rsatamiz

    class Meta:
        model = Follow
        fields = ['user', 'followed_user']  # JSON formatda ko'rsatiladigan maydonlar
