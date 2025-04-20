from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Product, Customer, Employee, Order
from decimal import Decimal

class ModelTests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        
        # Create test product
        self.product = Product.objects.create(
            name='Test Ski',
            description='Test Description',
            makeup='Test Makeup',
            size='170cm',
            price=Decimal('599.99'),
            stock_status=10
        )
        
        # Create test customer
        self.customer = Customer.objects.create(
            user=self.user,
            order_history='Test Order History'
        )
        
        # Create test employee
        self.employee_user = User.objects.create_user(
            username='employee',
            password='emppass123',
            is_staff=True
        )
        self.employee = Employee.objects.create(
            user=self.employee_user,
            position='Tester',
            training_status=True
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Ski')
        self.assertEqual(self.product.price, Decimal('599.99'))
        self.assertEqual(str(self.product), 'Test Ski')

    def test_customer_creation(self):
        self.assertEqual(self.customer.user.username, 'testuser')
        self.assertEqual(self.customer.order_history, 'Test Order History')

    def test_employee_creation(self):
        self.assertEqual(self.employee.position, 'Tester')
        self.assertTrue(self.employee.training_status)
        self.assertTrue(self.employee.user.is_staff)

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.product = Product.objects.create(
            name='Test Ski',
            price=Decimal('599.99'),
            stock_status=10,
            size='170cm'
        )

    def test_homepage_view(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ski_manufacturing_app/homepage.html')

    def test_product_list_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('product-page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products.html')

    def test_product_list_view_unauthenticated(self):
        response = self.client.get(reverse('product-page'))
        self.assertEqual(response.status_code, 302)  # Redirects to login

class APITests(APITestCase):
    def setUp(self):
        # Create test user with staff privileges
        self.staff_user = User.objects.create_user(
            username='staffuser',
            password='staffpass123',
            is_staff=True
        )
        
        # Create regular test user
        self.regular_user = User.objects.create_user(
            username='regularuser',
            password='userpass123'
        )
        
        # Create test product
        self.product = Product.objects.create(
            name='Test Ski',
            price=Decimal('599.99'),
            stock_status=10,
            size='170cm'
        )

    def test_product_list_api(self):
        response = self.client.get(reverse('product-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Ski')

    def test_product_create_api_staff(self):
        self.client.force_authenticate(user=self.staff_user)
        data = {
            'name': 'New Ski',
            'price': '699.99',
            'stock_status': 5,
            'size': '180cm'
        }
        response = self.client.post(reverse('product-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_product_create_api_unauthorized(self):
        self.client.force_authenticate(user=self.regular_user)
        data = {
            'name': 'New Ski',
            'price': '699.99',
            'stock_status': 5,
            'size': '180cm'
        }
        response = self.client.post(reverse('product-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_product_detail_api(self):
        response = self.client.get(
            reverse('product-detail', kwargs={'pk': self.product.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Ski')

    def test_product_update_api_staff(self):
        self.client.force_authenticate(user=self.staff_user)
        data = {'name': 'Updated Ski'}
        response = self.client.patch(
            reverse('product-detail', kwargs={'pk': self.product.pk}),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Ski')

    def test_product_delete_api_staff(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.delete(
            reverse('product-detail', kwargs={'pk': self.product.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

class OrderAPITests(APITestCase):
    def setUp(self):
        # Create test user and customer
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.customer = Customer.objects.create(
            user=self.user
        )
        
        # Create test product
        self.product = Product.objects.create(
            name='Test Ski',
            price=Decimal('599.99'),
            stock_status=10,
            size='170cm'
        )

    def test_order_create_api(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'customer': self.customer.id,
            'status': 'pending'
        }
        response = self.client.post(reverse('order-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_order_list_api(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('order-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


