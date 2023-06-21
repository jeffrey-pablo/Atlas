from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from accounts.models import CustomUser

class AccountsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.accounts_index_url = reverse('accounts_index')
        self.edit_profile_form_url = reverse('edit_profile_form')
        self.edit_profile_done_url = reverse('edit_profile_done')
        self.user_data = {
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe'
        )

    def test_home_view_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome')

    def test_home_view_unauthenticated(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/')

    def test_signup_view(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

        response = self.client.post(self.signup_url, self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

        self.assertEqual(get_user_model().objects.count(), 2)

    def test_accounts_index_view_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(self.accounts_index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/accounts_index.html')

    def test_accounts_index_view_unauthenticated(self):
        response = self.client.get(self.accounts_index_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/accounts/')

    def test_edit_profile_form_view(self):
        self.client.force_login(self.user)
        response = self.client.get(self.edit_profile_form_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/edit_profile_form.html')

        new_email = 'newemail@example.com'
        new_first_name = 'Jane'
        new_last_name = 'Smith'
        response = self.client.post(self.edit_profile_form_url, {
            'email': new_email,
            'first_name': new_first_name,
            'last_name': new_last_name,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.edit_profile_done_url)

        updated_user = CustomUser.objects.get(id=self.user.id)
        self.assertEqual(updated_user.email, new_email)
        self.assertEqual(updated_user.first_name, new_first_name)
        self.assertEqual(updated_user.last_name, new_last_name)

    def test_edit_profile_done_view_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(self.edit_profile_done_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/edit_profile_done.html')

    def test_edit_profile_done_view_unauthenticated(self):
        response = self.client.get(self.edit_profile_done_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/accounts/edit-profile/done/')