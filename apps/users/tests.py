from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import StudentProfile

User = get_user_model()

class UserAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            'username': 'testsiswa',
            'email': 'siswa@aici.id',
            'password': 'password123',
            'role': 'SISWA'
        }

    def test_registration_creates_profile(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        user = User.objects.get(username='testsiswa')
        self.assertEqual(user.role, 'SISWA')
        
        # Verify student profile created via signal
        profile = StudentProfile.objects.filter(user=user).exists()
        self.assertTrue(profile)

    def test_login_returns_tokens(self):
        # Register first
        self.client.post(self.register_url, self.user_data)
        
        # Login
        login_data = {'username': 'testsiswa', 'password': 'password123'}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
