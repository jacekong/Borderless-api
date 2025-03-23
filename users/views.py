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

'''
    Api, for mobile devices
'''
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



'''
    Web, User Authentication
'''
from django.views import View
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

class UserAuth(View):
    template_name = 'account/login.html'
    def get(self, request):
         return render(request, self.template_name, {})
     
    def post(self, request):
        if request.method == "POST":
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(request, email=email, password=password)

            if user is not None and user.check_password(password):
                login(request, user)
                # Redirect to a success page.
                return redirect('home')
            else:
                # Return an 'invalid login' error message.
                messages.success(request, ("Wrong credential, please try again...~..~"))
                return redirect('login')
        else:
            return render(request, self.template_name, {})
        
def logout_user(request):
    logout(request)
    return redirect('login')

class WebGetSearchForm(LoginRequiredMixin, View):
    template = 'account/search_friend.html'
    
    def get(self, request):
        return render(request, self.template, {})

class WebSearchFriend(LoginRequiredMixin, View):
    
    def get(self, request):
        query = request.GET.get('query', '')
        print(query)
        friends = None
        if query:
            friends = CustomUser.objects.filter(Q(username__icontains=query) | Q(user_id__icontains=query))
        return render(request, 'account/search_friend.html', {'friends': friends})
            