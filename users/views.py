from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import CustomUser
from .serializers import UserSerializer, UserUpdateSerializer
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q

# create a new user
class UserRegistView(APIView):
    permission_classes = [AllowAny]
    # method to create new user
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "success"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# search user
class UserSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        query = request.query_params.get('query', '')
        users = CustomUser.objects.filter(Q(username__icontains=query) | Q(user_id__icontains=query))
        serializer = UserSerializer(users, many=True, context={'request': request})
        
        return Response(serializer.data)

# method to update user info
@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request, *args, **kwargs):
    user = request.user

    current_user = CustomUser.objects.get(user_id=user.user_id)

    serializer = UserUpdateSerializer(current_user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()  # Save the updated user instance
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# get current user data
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def getCurrentUser(request):
    user = request.user
    
    current_user = get_object_or_404(CustomUser, id=user.id)
    serializer = UserSerializer(current_user, context={'request': request})
    
    return Response(serializer.data, status=status.HTTP_200_OK)

# @permission_classes([IsAuthenticated])
# @api_view(['GET'])
# def getAllUsers(request):
#     # user = request.user
    
#     all_users = CustomUser.objects.all()
#     serializer = UserSerializer(all_users, many=True, context={'request': request})
    
#     return Response(serializer.data, status=status.HTTP_200_OK)
    
        
        
