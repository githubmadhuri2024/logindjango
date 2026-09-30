# from accounts.auth import check_password

# def  test_correct_password():
#       result = check_password("Test@123", "Test@123")


#       assert result is True

# def test_wrong_password():
#     result = check_password("Wrong123", "Test@123")


#     assert result is False     
# 
# 
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()
 
import pytest
from rest_framework.test import APIClient
from accounts.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_register_success(api_client):
        data = {
        "username": "jeshwik",
        "password": "Test@12345",
        "email": "jeshwik@gmail.com",
        "phone": "9876543210",
        "address": "Main Road",
        "state": "Andhra Pradesh",
        "city": "Vizianagaram"
    }
        
        response =  api_client.post(
          "/api/register/",
          data,
          format="json"

         )
        assert response.status_code == 201

        assert response.data["success"] == "True"

        assert User.objects.filter(
        email="jeshwik@gmail.com"
        ).exists()


@pytest.mark.django_db
def test_register_without_username(api_client):

    data = {
        "password": "Test@12345",
        "email": "test@gmail.com"
    }

    response = api_client.post(
        "/api/register/",
        data,
        format="json"
    )

    assert response.status_code == 404
    assert response.data["message"] == "all field re required"



@pytest.mark.django_db
def test_register_without_password(api_client):

    data = {
        "username": "testuser",
        "email": "test@gmail.com"
    }

    response = api_client.post(
        "/api/register/",
        data,
        format="json"
    )

    assert response.status_code == 404
    assert response.data["message"] == "all field re required"

@pytest.mark.django_db
def test_register_without_email(api_client):

    data = {
        "username": "testuser",
        "password": "Test@12345"
    }

    response = api_client.post(
        "/api/register/",
        data,
        format="json"
    )

    assert response.status_code == 404
    assert response.data["message"] == "all field re required"

@pytest.mark.django_db
def test_register_duplicate_email(api_client):

    User.objects.create_user(
        username="olduser",
        email="test@gmail.com",
        password="Test@12345"
    )

    data = {
        "username": "newuser",
        "password": "Test@12345",
        "email": "test@gmail.com",
        "phone": "9876543210",
        "address": "Main Road",
        "state": "Andhra Pradesh",
        "city": "Vizianagaram"
    }

    response = api_client.post(
        "/api/register/",
        data,
        format="json"
    )

    assert response.status_code == 400
    assert response.data["success"] is False
    assert response.data["message"] == "User email already exits"

@pytest.fixture
def test_user(db):
     return User.objects.create_user(
          username="jeshwik",
        email="jeshwik@gmail.com",
        password="Test@12345"
     )

@pytest.mark.django_db
def test_login_success(api_client,test_user):
     data={
          "email":"jeshwik@gmail.com",
          "password":"Test@12345"
     }
     response=api_client.post(
          "/api/login",
          data,
          format="json"
     )
     print(response.data)
     assert response.status_code == 200
     assert response.data["success"] == "Login successful"

@pytest.mark.django_db
def test_login_without_email(api_client):
    data={
         "password":"Test@12345"
    }

    response=api_client.post(
         "/api/login/",
         data,
         format="json"

    )
    print(response.data)
    assert response.status_code==400
    assert response.data["success"] is  False
    assert response.data["message"] =="all fields are required"




@pytest.mark.django_db
def test_login_without_password(api_client):

    data={
        "email":"jeshwik@gmail.com"
    }
    response=api_client.post(
        "/api/login",
        data,
        format="json"
    )
    assert response.status_code==400
    assert response.data["success"] is False
    assert response.data["message"] =="All fields are required"

@pytest.mark.django_db
def test_login_email_not_exist(api_client):

      data={
           "email": "notexist@gmail.com",
           "password": "Test@12345"
      }  


      response=api_client.post(
          "/api/login/",
          data,
          format="json"
     )

      assert response.status_code == 404
      assert response.data["success"] is False
      assert response.data["message"] == "Email does not exits"