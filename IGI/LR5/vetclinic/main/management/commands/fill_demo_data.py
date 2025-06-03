from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import *
from django.utils import timezone
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Автоматически заполняет базу тестовыми данными для статистики и витрины'

    def handle(self, *args, **kwargs):
        # Услуги
        services = [
            Service.objects.create(name='Вакцинация', price=30, description='Профилактическая вакцинация', category='Профилактика'),
            Service.objects.create(name='Чипирование', price=50, description='Вживление микрочипа', category='Профилактика'),
            Service.objects.create(name='Стерилизация', price=120, description='Операция по стерилизации', category='Хирургия'),
            Service.objects.create(name='Удаление зубного камня', price=80, description='Профессиональная чистка зубов', category='Терапия'),
            Service.objects.create(name='УЗИ', price=60, description='Ультразвуковое исследование', category='Диагностика'),
        ]

        # Категории и отделения
        cat1 = DoctorCategory.objects.get_or_create(name='Высшая категория')[0]
        cat2 = DoctorCategory.objects.get_or_create(name='Категория 1')[0]
        dep1 = Department.objects.get_or_create(name='Терапевтическое отделение')[0]
        dep2 = Department.objects.get_or_create(name='Хирургическое отделение')[0]
        dep3 = Department.objects.get_or_create(name='Офтальмологическое отделение')[0]

        # Врачи
        for i, name in enumerate(['Петр Соловьев', 'Дмитрий Сидоров', 'Андрей Михайлов', 'Евгений Смирнов', 'Андрей Иванов', 'Петр Новиков']):
            username = f'doctor{i+1}'
            user, _ = User.objects.get_or_create(username=username, defaults={
                'first_name': name.split()[0],
                'last_name': name.split()[1],
                'email': f'{username}@test.com'
            })
            Doctor.objects.get_or_create(user=user, defaults={
                'category': cat1 if i % 2 == 0 else cat2,
                'department': [dep1, dep2, dep3][i % 3],
                'birth_date': timezone.now().date() - timedelta(days=365*35)
            })

        # Клиенты и питомцы
        for i, pet_data in enumerate([
            ('Барсик', 'Кошка', 'Сиамская'),
            ('Пушок', 'Крыса', 'Коги'),
            ('Пушок', 'Шиншилла', 'Такса'),
            ('Мурка', 'Хомяк', 'Мейн-кун'),
            ('Стрелка', 'Собака', 'Овчарка'),
            ('Граф', 'Фретка', 'Коги'),
        ]):
            username = f'client{i+1}'
            user, _ = User.objects.get_or_create(username=username, defaults={
                'first_name': pet_data[0],
                'last_name': 'Клиентов',
                'email': f'{username}@test.com'
            })
            client, _ = Client.objects.get_or_create(user=user, defaults={
                'birth_date': timezone.now().date() - timedelta(days=365*30),
                'address': f'ул. Тестовая, д.{i+1}',
                'phone': f'+375 (29) 100-00-0{i+1}'
            })
            pet, _ = Pet.objects.get_or_create(client=client, name=pet_data[0], species=pet_data[1], breed=pet_data[2], defaults={
                'birth_date': timezone.now().date() - timedelta(days=365*3)
            })

        # Записи и отзывы
        all_clients = list(Client.objects.all())
        all_pets = list(Pet.objects.all())
        all_doctors = list(Doctor.objects.all())
        for i in range(10):
            client = random.choice(all_clients)
            pet = random.choice(all_pets)
            doctor = random.choice(all_doctors)
            app = Appointment.objects.create(
                client=client,
                pet=pet,
                doctor=doctor,
                date=timezone.now() - timedelta(days=random.randint(0, 30)),
                diagnosis='Плановый осмотр',
                total_price=random.randint(30, 150)
            )
            app.services.set(random.sample(services, k=random.randint(1, 3)))
            Review.objects.get_or_create(client=client, rating=random.randint(3, 5), text='Все понравилось! Спасибо врачу.')

        self.stdout.write(self.style.SUCCESS('Демо-данные успешно добавлены!')) 