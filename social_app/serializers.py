from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post, Comment, Like, Profile, Follow

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Foydalanuvchi haqida ma'lumot

    class Meta:
        model = Profile
        fields = ['user', 'bio', 'profile_picture', 'location']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Parolni faqat yozish mumkin, qaytarilmaydi

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class PostSerializer(serializers.ModelSerializer):
    comments = serializers.PrimaryKeyRelatedField(many=True, queryset=Comment.objects.all())  # Har bir post bilan bog'liq izohlarni ko'rsatish
    likes = serializers.PrimaryKeyRelatedField(many=True, queryset=Like.objects.all())  # Har bir post bilan bog'liq like'larni ko'rsatish

    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'timestamp', 'comments', 'likes']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'content', 'timestamp']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'user']

class FollowSerializer(serializers.ModelSerializer):
    followed_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Kuzatilgan foydalanuvchi haqida ma'lumot

    class Meta:
        model = Follow
        fields = ['id', 'user', 'followed_user']
