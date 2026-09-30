from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


from django.shortcuts import render
from .Serializers import RegisterSerializer
from .models import UserProfile
from django.contrib.auth.models import User


# @api_view(["post"])
# def  register(request):
#   try:
#          username=request.data.get("username")
#          email=request.data.get("email")
#          password=request.data.get("password")
#          phone=request.data.get("phone")
#          address=request.data.get("address")
#          city=request.data.get("city")
#          state=request.data.get("state")



#          if not username or not password or not email:
#            return Response(
#                {
#                "success":False,
#                "message":"username ,email,password are required",
       
#                }, status=status.HTTP_404_NOT_FOUND)

#          if User.objects.filter(email=email).exists():
#             return Response(
#                 {
#                   "success":False,
#                   "message":"Email is already exists"
#                },status=status.HTTP_400_BAD_REQUEST)

#          hashed_password=make_password(password)
#          data={
#             "username": username,
#             "email": email,
#             "password": hashed_password,
#             "phone": phone,
#             "address":address,

#             "state": state,
#             "city": city,
#          }
         
#          serializer= RegisterSerializer(
#           data=data
#          )


#          if serializer.is_valid():
#             serializer.save()
#             return Response ({
#              "success":True,
#             "message":"User Register Successfully"
#              },status=status.HTTP_201_CREATED)

    


#          return Response(
#             {
#                 "success": False,
#                 "errors": serializer.errors
#             },
#             status=status.HTTP_400_BAD_REQUEST
#         )

#   except Exception as e:
       
#        return Response({
#       "success":False,
#       "message":"Something went wrong",
#       "error":str(e)
#       },
#       status=status.HTTP_500_INTERNAL_SERVER_ERROR
#       )






@api_view(["POST"])
def register(request):

  try:
      username=request.data.get("username")
      password=request.data.get("password")
      email=request.data.get("email")
      address=request.data.get("address")
      state=request.data.get("state")
      phone=request.data.get("phone")
      city=request.data.get("city")
      if not username  or not password or not email:
       return Response({
         "message":"all field re required"
       },status=status.HTTP_404_NOT_FOUND)

      if User.objects.filter(email=email).exists():
          return Response({
         "success":False,
        "message":"User email already exits"
        
         },status=status.HTTP_400_BAD_REQUEST)
      
      hash_password=make_password(password)

      data={
     "username":username,
     "password":hash_password,
     "email":email,
     "phone":phone,
     "address":address,
     "state":state,
     "city":city

    }
      serializer=RegisterSerializer(
      data=data
    )
      if serializer.is_valid():
       serializer.save()
       return Response({
          "message":"Register Successfully",
          "success":"True"
       },status=status.HTTP_201_CREATED)

 
      return Response({
          "success":False,
          "error":serializer.error
       },status=status.HTTP_400_BAD_REQUEST)


  except Exception as e:
    return Response ({
      "success":False,
       "error":str(e),
       "message":"Internal Server Error"

    },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                


@api_view(["POST"])
def login(request):
  try:
     email=request.data.get("email")
     password=request.data.get("password")

     if not email or not password:
       return Response ({
         "success":False,
         "message":"All  fileds are required"
       },status=status.HTTP_400_BAD_REQUEST)

     user=User.objects.filter(email=email).first()
     if not user:
        return Response({
          "success":False,
          "message":"Email does not exits"
          
        },status=status.HTTP_404_NOT_FOUND)



     if not check_password(password,  user.password):
       return Response({
             "success": False,
            "message": "Invalid password"
        }, status=status.HTTP_401_UNAUTHORIZED)
     

     serializer = RegisterSerializer(user)
 

     return Response(
        {
        "success": "Login successful",
        
        "user": serializer.data,
      
        },
        status=status.HTTP_200_OK,


    )
  
  except Exception as e:
    return Response ({
      "success":False,
       "error":str(e),
       "message":"Internal Server Error"

    },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                