from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Stock, Watchlist, User
from .serializers import StockSerializer
import json
# Add this import at the top of your views.py file
from rest_framework.authtoken.models import Token

from django.contrib.auth.hashers import make_password

# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import User  # Ensure the User model exists
import json



def home(request):
    return HttpResponse("Hello...")

def stock_list(request):
    stocks = Stock.objects.all().values('stock_code', 'stock_name', 'stock_price')
    return JsonResponse(list(stocks), safe=False)

class StockListView(generics.ListAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

@api_view(['POST'])
def add_to_watchlist(request):
    stock_id = request.data.get('stock_id')
    user = request.user  # Assumes user is authenticated
    try:
        stock = Stock.objects.get(id=stock_id)
        Watchlist.objects.create(user=user, stock=stock)
        return Response({"message": "Stock added to watchlist"}, status=status.HTTP_201_CREATED)
    except Stock.DoesNotExist:
        return Response({"error": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
# views.py
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import User
from .serializers import LoginSerializer, BalanceSerializer
import json

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        full_name = data.get('fullName')
        username = data.get('username')
        emailID = data.get('emailID')
        password = data.get('password')
        re_password = data.get('rePassword')
        gender = data.get('gender')
        age = data.get('age')

        if password != re_password:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

        hashed_password = make_password(password)
        try:
            user = User.objects.create(
                full_name=full_name,
                username=username,
                emailID=emailID,
                password=hashed_password,
                gender=gender,
                age=age,
                balance=1000000  # Initial balance
            )
            return JsonResponse({'message': 'User created successfully'}, status=201)
        except IntegrityError:
            return JsonResponse({'error': 'Username or Email already exists'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)


from rest_framework.authtoken.models import Token  # Ensure this import is at the top

from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import LoginSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow all users to access this endpoint

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key, "message": "Login successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BalanceView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = BalanceSerializer(request.user)
        return Response(serializer.data, status=200)



from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class PasswordResetView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            reset_url = f'http://localhost:3000/reset-password/{token}'
            
            send_mail(
                'Password Reset',
                f'Click here to reset your password: {reset_url}',
                'from@example.com',
                [email],
                fail_silently=False,
            )
            return Response({"message": "Password reset email sent!"}, status=200)
        except User.DoesNotExist:
            return Response({"error": "User with that email does not exist"}, status=400)
