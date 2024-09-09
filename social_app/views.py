from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Profile, FriendRequest, Message, Post, Comment, Like, Follow
from .serializers import ProfileSerializer, FriendRequestSerializer, MessageSerializer, PostSerializer, CommentSerializer, LikeSerializer, FollowSerializer, UserSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string

@api_view(['POST'])
def register_user(request):
    """
    Foydalanuvchini ro'yxatdan o'tkazish
    """
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_user_profile(request, user_id):
    """
    Foydalanuvchi profilini olish
    """
    profile = get_object_or_404(Profile, user_id=user_id)
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)

@api_view(['PUT'])
def update_user_profile(request, user_id):
    """
    Foydalanuvchi profilini yangilash
    """
    profile = get_object_or_404(Profile, user_id=user_id)
    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def send_friend_request(request):
    """
    Do'stlik so'rovini yuborish
    """
    serializer = FriendRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def accept_friend_request(request, request_id):
    """
    Do'stlik so'rovini qabul qilish
    """
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    friend_request.is_accepted = True
    friend_request.save()
    return Response({'message': 'Friend request accepted'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def send_message(request):
    """
    Xabar yuborish
    """
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_messages(request):
    """
    Foydalanuvchining xabarlarini olish
    """
    user = request.user
    messages = Message.objects.filter(recipient=user)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_user_posts(request, user_id):
    """
    Foydalanuvchining postlarini olish
    """
    posts = Post.objects.filter(user_id=user_id)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_post(request):
    """
    Post yaratish
    """
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_post_comments(request, post_id):
    """
    Postga izohlarni olish
    """
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_comment(request):
    """
    Postga izoh qoldirish
    """
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_post_likes(request, post_id):
    """
    Postga like'larni olish
    """
    post = get_object_or_404(Post, id=post_id)
    likes = Like.objects.filter(post=post)
    serializer = LikeSerializer(likes, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def like_post(request):
    """
    Postga like qo'yish
    """
    serializer = LikeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def follow_user(request):
    """
    Foydalanuvchini kuzatish
    """
    serializer = FollowSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def unfollow_user(request, user_id):
    """
    Foydalanuvchini kuzatishni bekor qilish
    """
    follow = Follow.objects.filter(user=request.user, followed_user_id=user_id).first()
    if follow:
        follow.delete()
        return Response({'message': 'Unfollowed successfully'}, status=status.HTTP_200_OK)
    return Response({'error': 'Follow record not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_user_followers(request, user_id):
    """
    Foydalanuvchining kuzatuvchilarini olish
    """
    user = get_object_or_404(User, id=user_id)
    followers = user.followers.all()
    serializer = UserSerializer(followers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_user_following(request, user_id):
    """
    Foydalanuvchining kuzatayotganlarini olish
    """
    user = get_object_or_404(User, id=user_id)
    following = user.following.all()
    serializer = UserSerializer(following, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def login_user(request):
    """
    Foydalanuvchini login qilish
    """
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_user(request):
    """
    Foydalanuvchini logout qilish
    """
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def password_reset(request):
    """
    Parolni tiklash uchun token yuborish
    """
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
        reset_token = get_random_string(length=32)  # Token generatsiya qilish
        # Tokenni saqlash va email yuborish funksiyasi qo'shilishi kerak
        send_mail(
            'Password Reset Token',
            f'Your password reset token is: {reset_token}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return Response({'message': 'Password reset token sent to your email'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)
