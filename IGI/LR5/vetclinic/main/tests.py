from django.test import TestCase, Client as DjangoClient
from django.contrib.auth.models import User
from main.models import *
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.urls import reverse

class ClientModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client_obj = Client.objects.create(user=user, birth_date=date(1990,1,1), address='Test St', phone='+375 (29) 123-45-67')

    def test_create_client_valid(self):
        self.assertEqual(str(self.client_obj), f"{self.client_obj.user.get_full_name()} ({self.client_obj.phone})")

    def test_client_underage(self):
        user = User.objects.create(username='underage')
        client = Client(user=user, birth_date=date.today() - timedelta(days=365*17), address='Test', phone='+375 (29) 123-45-67')
        with self.assertRaises(ValidationError):
            client.full_clean()

    def test_client_phone_invalid(self):
        user = User.objects.create(username='badphone')
        client = Client(user=user, birth_date=date(2000,1,1), address='Test', phone='12345')
        with self.assertRaises(ValidationError):
            client.full_clean()

    def test_client_str(self):
        self.assertIn('testuser', str(self.client_obj))

class PetModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='petuser', password='testpass')
        client = Client.objects.create(user=user, birth_date=date(1990,1,1), address='Test St', phone='+375 (29) 123-45-67')
        self.pet = Pet.objects.create(client=client, name='Барсик', species='Кошка', breed='Сиамская', birth_date=date(2020,1,1))

    def test_create_pet(self):
        self.assertEqual(str(self.pet), 'Барсик (Кошка)')

    def test_pet_str(self):
        self.assertIn('Барсик', str(self.pet))

class DoctorModelTest(TestCase):
    def test_create_doctor(self):
        user = User.objects.create(username='docuser')
        cat = DoctorCategory.objects.create(name='Терапевт')
        dep = Department.objects.create(name='Общее')
        spec = Specialization.objects.create(name='Кошки')
        doctor = Doctor.objects.create(user=user, category=cat, department=dep, birth_date=date(1980,1,1))
        doctor.specializations.add(spec)
        self.assertEqual(str(doctor), user.get_full_name())

class ServiceModelTest(TestCase):
    def test_create_service(self):
        service = Service.objects.create(name='Вакцинация', price=50, description='Прививка', category='Процедуры')
        self.assertEqual(str(service), 'Вакцинация')

    def test_service_str(self):
        service = Service.objects.create(name='Test Service', price=100, description='desc', category='cat')
        self.assertEqual(str(service), 'Test Service')

class AppointmentModelTest(TestCase):
    def test_create_appointment(self):
        user = User.objects.create(username='appuser')
        client = Client.objects.create(user=user, birth_date=date(2000,1,1), address='Test', phone='+375 (29) 123-45-67')
        pet = Pet.objects.create(client=client, name='Барсик', species='Кот', breed='Дворянин', birth_date=date(2020,1,1))
        docuser = User.objects.create(username='docuser')
        cat = DoctorCategory.objects.create(name='Терапевт')
        dep = Department.objects.create(name='Общее')
        doctor = Doctor.objects.create(user=docuser, category=cat, department=dep, birth_date=date(1980,1,1))
        service = Service.objects.create(name='Вакцинация', price=50, description='Прививка', category='Процедуры')
        app = Appointment.objects.create(client=client, pet=pet, doctor=doctor, date=date.today())
        app.services.add(service)
        self.assertEqual(str(app), f"{client.user.get_full_name()} - {app.date.strftime('%d/%m/%Y')}")

class PromoCodeModelTest(TestCase):
    def test_create_promocode(self):
        promo = PromoCode.objects.create(code='PROMO10', discount=10, is_active=True, valid_until=date(2030,1,1))
        self.assertEqual(str(promo), 'PROMO10')

class ReviewModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='revuser', password='testpass')
        client = Client.objects.create(user=user, birth_date=date(1990,1,1), address='Test St', phone='+375 (29) 123-45-67')
        self.review = Review.objects.create(client=client, rating=5, text='Отлично!')

    def test_create_review(self):
        self.assertEqual(str(self.review), f"{self.review.client.user.get_full_name()} - 5")

    def test_review_str(self):
        self.assertIn('revuser', str(self.review))

class ServiceListViewTest(TestCase):
    def setUp(self):
        Service.objects.create(name='A', price=10, description='d', category='c')
        Service.objects.create(name='B', price=20, description='d', category='c')

    def test_service_list_view(self):
        c = DjangoClient()
        response = c.get(reverse('service_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A')
        self.assertContains(response, 'B')

class ClientFormValidationTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='formuser', password='testpass')
        self.client_obj = Client.objects.create(user=user, birth_date=date(1990,1,1), address='Test St', phone='+375 (29) 123-45-67')

    def test_phone_format(self):
        self.assertRegex(self.client_obj.phone, r'\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}') 