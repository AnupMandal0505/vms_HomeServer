from rest_framework.response import Response
from authuser.serializers.LoginSerializer import LoginSerializer
from authuser.serializers.UserSerializer import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from authuser.models import User
from rest_framework import status

class LoginAPI(viewsets.ViewSet):
    def create(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():

                phone = serializer.validated_data['phone']
                password = serializer.validated_data['password']
                role = serializer.validated_data['role'].upper()


                user = User.objects.get(phone=phone)

                # serial = UserSerializer(user, many=False).data
                if not user.groups.filter(name=role).exists():
                    return Response({"ERR": "Role not matched"})
                user = authenticate(phone=phone, password=password)
                if user is not None:
                    if Token.objects.filter(user=user).exists():
                        Token.objects.get(user=user).delete()
                    token = Token.objects.create(user=user)

                    return Response({
                        'user': UserSerializer(user, many=False).data,
                        'Token': token.key,
                    })

                else:
                    return Response({"ERR": 'Invalid phone and password'})

            else:
                return Response({'ERR':"Invalid Data"})

        except Exception as e:
            print(e)
            return Response({'ERR':"Invalid phone and password"})


class DisplayLoginAPI(viewsets.ViewSet):
    def create(self, request):
        try:
            user = User.objects.get(phone=request.data.get("phone"))

            user = authenticate(phone=request.data.get("phone"), password=request.data.get("password"))
            if user is not None:
                if Token.objects.filter(user=user).exists():
                    Token.objects.get(user=user).delete()
                token = Token.objects.create(user=user)
            
                return Response({
                    'user': UserSerializer(user, many=False).data,
                    'Token': token.key,
                },status=status.HTTP_200_OK)

            else:
                return Response({"ERR": 'Invalid phone and password'},status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(e)
            return Response({'ERR':"Invalid phone and password"})



class LogoutView(viewsets.ViewSet):
    def create(self,request):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        try:
            Token.objects.get(key=token).delete()
            return Response({'success': 'Logged out successfully'})
        except Exception as e:
            return Response({'error': 'Failed to log out'})