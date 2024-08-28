from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, CommentSerializer, PostSerializer, ProfileSerializer, FollowSerializer
from .models import Message, Like, Post, Profile, Follow

# Foydalanuvchi ro'yxatdan o'tish
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Foydalanuvchini tizimga kirgizish
@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'message': 'Successfully logged in'}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# Foydalanuvchini tizimdan chiqarish
@api_view(['POST'])
def logout_user(request):
    logout(request)
    return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)

# Xabar yuborish (faqat autentifikatsiyadan o'tgan foydalanuvchilar uchun)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request, username):
    try:
        recipient = User.objects.get(username=username)
        content = request.data.get('content')
        if not content:
            return Response({'error': 'Message content is required'}, status=status.HTTP_400_BAD_REQUEST)
        message = Message.objects.create(
            sender=request.user, recipient=recipient, content=content
        )
        return Response({'status': 'Message sent', 'message': message.content}, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

# Foydalanuvchiga kelgan xabarlarni olish (faqat autentifikatsiyadan o'tgan foydalanuvchilar uchun)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages(request):
    messages = Message.objects.filter(recipient=request.user)
    message_list = [{'sender': msg.sender.username, 'content': msg.content, 'timestamp': msg.timestamp} for msg in messages]
    return Response({'messages': message_list}, status=status.HTTP_200_OK)

# Barcha postlarni olish
@api_view(['GET'])
def get_posts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Yangi post yaratish (faqat autentifikatsiyadan o'tgan foydalanuvchilar uchun)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Postga izoh qo'shish (faqat autentifikatsiyadan o'tgan foydalanuvchilar uchun)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Postni yoqtirish (faqat autentifikatsiyadan o'tgan foydalanuvchilar uchun)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    if not Like.objects.filter(post=post, user=request.user).exists():
        like = Like.objects.create(post=post, user=request.user)
        return Response({'message': 'Post liked'}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)

# Foydalanuvchilarni qidirish
@api_view(['GET'])
def search_users(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query)
    user_list = [{'username': user.username, 'email': user.email} for user in users]
    return Response(user_list, status=status.HTTP_200_OK)

# Postlarni qidirish
@api_view(['GET'])
def search_posts(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(content__icontains=query)
    post_list = [{'id': post.id, 'content': post.content} for post in posts]
    return Response(post_list, status=status.HTTP_200_OK)

# Do'stlar lentasini olish (faqat autentifikatsiyadan o'tgan foydalanuvchilar uchun)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_feed(request):
    try:
        friends = request.user.profile.friends.all()
        posts = Post.objects.filter(user__in=friends)
        following_users = request.user.following.values_list('followed_user', flat=True)
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

# Profilni ko'rish va tahrirlash (faqat autentifikatsiyadan o'tgan foydalanuvchilar uchun)
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Foydalanuvchini kuzatish (faqat autentifikatsiyadan o'tgan foydalanuvchilar uchun)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, username):
    try:
        followed_user = User.objects.get(username=username)
        follow, created = Follow.objects.get_or_create(user=request.user, followed_user=followed_user)
        if created:
            return Response({'status': 'Now following'}, status=status.HTTP_200_OK)
        return Response({'status': 'Already following'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

# Foydalanuvchini kuzatishni to'xtatish (faqat autentifikatsiyadan o'tgan foydalanuvchilar uchun)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, username):
    try:
        followed_user = User.objects.get(username=username)
        follow = Follow.objects.filter(user=request.user, followed_user=followed_user).first()
        if follow:
            follow.delete()
            return Response({'status': 'Unfollowed'}, status=status.HTTP_200_OK)
        return Response({'status': 'Not following'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
