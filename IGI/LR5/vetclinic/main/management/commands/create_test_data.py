from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from main.models import *

class Command(BaseCommand):
    help = 'Creates test data for the veterinary clinic'

    def handle(self, *args, **kwargs):
        # Create superuser
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            admin_user.first_name = 'Кирилл'
            admin_user.last_name = 'Шарафанович'
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Superuser created'))

            # Create client record for admin
            Client.objects.create(
                user=admin_user,
                birth_date=date(1990, 1, 1),
                address='ул. Восточная, 66',
                phone='+375 (29) 123-45-67'
            )
            self.stdout.write(self.style.SUCCESS('Admin client record created'))

        # Create regular user
        if not User.objects.filter(username='client').exists():
            user = User.objects.create_user('client', 'client@example.com', 'client123')
            user.first_name = 'Иван'
            user.last_name = 'Иванов'
            user.save()
            self.stdout.write(self.style.SUCCESS('Regular user created'))

        # Create client
        if not Client.objects.filter(user__username='client').exists():
            client = Client.objects.create(
                user=User.objects.get(username='client'),
                birth_date=date(1990, 1, 1),
                address='ул. Примерная, 123',
                phone='+375 (29) 123-45-67'
            )
            self.stdout.write(self.style.SUCCESS('Client created'))

        # Create doctor category
        if not DoctorCategory.objects.exists():
            category = DoctorCategory.objects.create(name='Высшая категория')
            self.stdout.write(self.style.SUCCESS('Doctor category created'))

        # Create department
        if not Department.objects.exists():
            department = Department.objects.create(name='Терапевтическое отделение')
            self.stdout.write(self.style.SUCCESS('Department created'))

        # Create specialization
        if not Specialization.objects.exists():
            specialization = Specialization.objects.create(name='Терапевт')
            self.stdout.write(self.style.SUCCESS('Specialization created'))

        # Create doctor user
        if not User.objects.filter(username='doctor').exists():
            doctor_user = User.objects.create_user('doctor', 'doctor@example.com', 'doctor123')
            doctor_user.first_name = 'Петр'
            doctor_user.last_name = 'Петров'
            doctor_user.save()
            self.stdout.write(self.style.SUCCESS('Doctor user created'))

        # Create doctor
        if not Doctor.objects.exists():
            doctor = Doctor.objects.create(
                user=User.objects.get(username='doctor'),
                category=DoctorCategory.objects.first(),
                department=Department.objects.first(),
                birth_date=date(1985, 1, 1)
            )
            doctor.specializations.add(Specialization.objects.first())
            self.stdout.write(self.style.SUCCESS('Doctor created'))

        # Create pet
        if not Pet.objects.exists():
            pet = Pet.objects.create(
                client=Client.objects.first(),
                name='Барсик',
                species='Кошка',
                breed='Сиамская',
                birth_date=date(2020, 1, 1)
            )
            self.stdout.write(self.style.SUCCESS('Pet created'))

        # Create service
        if not Service.objects.exists():
            service = Service.objects.create(
                name='Консультация терапевта',
                price=50.00,
                description='Первичный осмотр и консультация терапевта',
                category='Консультации'
            )
            self.stdout.write(self.style.SUCCESS('Service created'))

        # Create diagnosis
        if not Diagnosis.objects.exists():
            diagnosis = Diagnosis.objects.create(
                pet=Pet.objects.first(),
                doctor=Doctor.objects.first(),
                description='Здоров',
                date=timezone.now().date()
            )
            self.stdout.write(self.style.SUCCESS('Diagnosis created'))

        # Create appointment
        if not Appointment.objects.exists():
            appointment = Appointment.objects.create(
                client=Client.objects.first(),
                pet=Pet.objects.first(),
                doctor=Doctor.objects.first(),
                date=timezone.now() + timedelta(days=1),
                diagnosis='Плановый осмотр',
                total_price=50.00
            )
            appointment.services.add(Service.objects.first())
            self.stdout.write(self.style.SUCCESS('Appointment created'))

        # Create promo code
        if not PromoCode.objects.exists():
            promo = PromoCode.objects.create(
                code='WELCOME10',
                discount=10,
                is_active=True,
                valid_until=timezone.now().date() + timedelta(days=30)
            )
            self.stdout.write(self.style.SUCCESS('Promo code created'))

        # Create news
        if not News.objects.exists():
            news = News.objects.create(
                title='Открытие новой клиники',
                summary='Мы рады сообщить об открытии новой ветеринарной клиники',
                content='Подробная информация об открытии новой клиники...',
                published_at=timezone.now()
            )
            self.stdout.write(self.style.SUCCESS('News created'))

        # Create FAQ
        if not FAQ.objects.exists():
            faq = FAQ.objects.create(
                question='Какие документы нужны для первого визита?',
                answer='При первом визите необходимо иметь паспорт и ветеринарный паспорт питомца.',
                added_at=timezone.now().date()
            )
            self.stdout.write(self.style.SUCCESS('FAQ created'))

        # Create contact
        if not Contact.objects.exists():
            contact = Contact.objects.create(
                name='Анна Сидорова',
                position='Администратор',
                phone='+375 (29) 765-43-21',
                email='admin@vetclinic.by',
                description='Главный администратор клиники',
                birth_date=date(1992, 1, 1)
            )
            self.stdout.write(self.style.SUCCESS('Contact created'))

        # Create review
        if not Review.objects.exists():
            review = Review.objects.create(
                client=Client.objects.first(),
                rating=5,
                text='Отличная клиника, очень доволен обслуживанием!',
                date=timezone.now().date()
            )
            self.stdout.write(self.style.SUCCESS('Review created'))

        # Create vacancy
        if not Vacancy.objects.exists():
            vacancy = Vacancy.objects.create(
                title='Ветеринарный врач',
                description='Требуется опытный ветеринарный врач',
                is_active=True,
                published_at=timezone.now()
            )
            self.stdout.write(self.style.SUCCESS('Vacancy created'))

        self.stdout.write(self.style.SUCCESS('All test data created successfully')) 