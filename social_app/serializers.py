from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post, Comment, Like, Profile, Follow
import re

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Foydalanuvchi haqida ma'lumot

    class Meta:
        model = Profile
        fields = ['user', 'bio', 'profile_picture', 'location']

    def validate_bio(self, value):
        # Bio uzunligi cheklangan (ixtiyoriy, 160 belgiga)
        if len(value) > 160:
            raise serializers.ValidationError(
                "Bio uzunligi 160 belgidan oshmasligi kerak."
            )
        return value

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Parolni faqat yozish mumkin, qaytarilmaydi

    def validate_password(self, value):
        # Parol uchun regax qoidalari: kamida 8 ta belgi, birta katta harf va birta raqam bo'lishi kerak
        password_regex = re.compile(r'^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$')
        
        if not password_regex.match(value):
            raise serializers.ValidationError(
                "Parol kamida 8 ta belgi, birta katta harf va birta raqamdan iborat bo'lishi kerak."
            )
        return value

    def validate_username(self, value):
        # Foydalanuvchi nomi uchun regax qoidalari: faqat alfanumerik (harflar va raqamlar)
        if not re.match(r'^[a-zA-Z0-9]+$', value):
            raise serializers.ValidationError(
                "Foydalanuvchi nomida faqat harflar va raqamlar bo'lishi kerak."
            )
        return value

    def validate_email(self, value):
        # Email manzili uchun regax qoidalari
        email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        
        if not email_regex.match(value):
            raise serializers.ValidationError(
                "Email manzili noto'g'ri formatda."
            )
        return value

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

    def validate_content(self, value):
        # Post content uchun regax qoidalari: maksimal uzunlikni cheklash (ixtiyoriy, 280 belgiga)
        if len(value) > 280:
            raise serializers.ValidationError(
                "Post uzunligi 280 belgidan oshmasligi kerak."
            )
        return value

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'content', 'timestamp']

    def validate_content(self, value):
        # Comment content uchun regax qoidalari: bo'sh bo'lmasligi kerak
        if not value.strip():
            raise serializers.ValidationError(
                "Izoh bo'sh bo'lmasligi kerak."
            )
        return value

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'user']

class FollowSerializer(serializers.ModelSerializer):
    followed_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Kuzatilgan foydalanuvchi haqida ma'lumot

    class Meta:
        model = Follow
        fields = ['id', 'user', 'followed_user']

    def validate(self, data):
        # User o'zini kuzatib bo'lmaydi
        if data['user'] == data['followed_user']:
            raise serializers.ValidationError(
                "Foydalanuvchi o'zini kuzatolmaydi."
            )
        return data
