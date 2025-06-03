from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
import random
from main.models import *

FIRST_NAMES = ['Иван', 'Петр', 'Сергей', 'Алексей', 'Дмитрий', 'Андрей', 'Максим', 'Евгений', 'Владимир', 'Антон', 'Григорий', 'Виктор', 'Олег', 'Мария', 'Елена', 'Анна', 'Ольга', 'Татьяна', 'Светлана', 'Наталья', 'Юлия', 'Екатерина', 'Алина', 'Вера', 'Галина']
LAST_NAMES = ['Иванов', 'Петров', 'Сидоров', 'Кузнецов', 'Смирнов', 'Попов', 'Васильев', 'Морозов', 'Волков', 'Соловьев', 'Михайлов', 'Новиков', 'Федоров', 'Ковалев', 'Романов', 'Борисов', 'Гаврилов', 'Денисов', 'Жуков', 'Захаров', 'Киселев', 'Макаров', 'Орлов', 'Павлов']
PET_NAMES = ['Барсик', 'Мурка', 'Шарик', 'Рекс', 'Белка', 'Стрелка', 'Том', 'Джерри', 'Лаки', 'Снежок', 'Граф', 'Рыжик', 'Пушок', 'Боня', 'Луна', 'Симба', 'Чарли', 'Мотя', 'Кузя', 'Тиша']
BREEDS = ['Сиамская', 'Британская', 'Дворняга', 'Лабрадор', 'Корги', 'Мейн-кун', 'Шпиц', 'Бульдог', 'Сфинкс', 'Персидская', 'Овчарка', 'Такса', 'Чихуахуа', 'Доберман', 'Бигль', 'Скоттиш-фолд']
SPECIES = ['Кошка', 'Собака', 'Попугай', 'Кролик', 'Хомяк', 'Черепаха', 'Крыса', 'Фретка', 'Шиншилла', 'Морская свинка', 'Игуана', 'Ёж', 'Змея']
POSITIONS = ['Администратор', 'Ветеринар', 'Ассистент', 'Грумер', 'Терапевт', 'Хирург', 'Офтальмолог', 'Кардиолог', 'Дерматолог', 'Рентгенолог', 'Лаборант', 'Менеджер', 'Тренер']
SERVICE_NAMES = ['Консультация', 'Вакцинация', 'Стерилизация', 'Чипирование', 'УЗИ', 'Рентген', 'Стоматология', 'Терапия', 'Хирургия', 'Груминг', 'Анализы', 'Кастрация', 'Удаление зуба']
CATEGORIES = ['Консультации', 'Процедуры', 'Операции', 'Диагностика', 'Уход', 'Лечение']
REVIEW_TEXTS = [
    'Очень доволен обслуживанием!',
    'Спасибо врачам за заботу!',
    'Быстро помогли нашему питомцу.',
    'Всё понравилось, рекомендую!',
    'Доброжелательный персонал.',
    'Чисто, уютно, современно.',
    'Профессиональный подход.',
    'Доступные цены и отличное качество.',
    'Обращаюсь не первый раз — всегда довольны.',
    'Спасибо за помощь!',
    'Врач объяснил всё понятно.',
    'Питомец быстро пошёл на поправку.'
]
FAQ_QUESTIONS = [
    'Как записаться на приём?',
    'Какие документы нужны для первого визита?',
    'Можно ли оплатить картой?',
    'Работаете ли вы ночью?',
    'Какие услуги доступны?',
    'Как подготовить питомца к операции?',
    'Есть ли парковка?',
    'Можно ли прийти без записи?',
    'Как получить консультацию онлайн?',
    'Какие вакцины вы используете?',
    'Сколько стоит приём?',
    'Как ухаживать за питомцем после операции?'
]
FAQ_ANSWERS = [
    'Записаться можно по телефону или через сайт.',
    'Паспорт владельца и ветеринарный паспорт животного.',
    'Да, принимаем карты и наличные.',
    'Да, мы работаем круглосуточно.',
    'Список услуг есть на сайте.',
    'Следуйте рекомендациям врача.',
    'Парковка есть перед зданием.',
    'Желательно записаться заранее.',
    'Консультация онлайн доступна по записи.',
    'Используем только сертифицированные вакцины.',
    'Стоимость зависит от услуги.',
    'Врач даст подробные рекомендации.'
]
NEWS_TITLES = [
    'Открытие нового филиала!',
    'Скидки на вакцинацию в июне',
    'Приём новых специалистов',
    'Бесплатная консультация терапевта',
    'День открытых дверей',
    'Обновление оборудования',
    'Партнёрство с приютами',
    'Акция для новых клиентов',
    'Расширение спектра услуг',
    'Вакцинация против бешенства',
    'Профилактика паразитов',
    'Семинар для владельцев кошек',
    'Праздничные часы работы'
]
NEWS_SUMMARIES = [
    'Узнайте подробности о нашем новом филиале.',
    'В июне действует специальная цена на вакцинацию.',
    'В нашей команде новые врачи!',
    'Получите бесплатную консультацию терапевта.',
    'Приглашаем на день открытых дверей.',
    'В клинике новое современное оборудование.',
    'Мы сотрудничаем с приютами города.',
    'Для новых клиентов — скидки!',
    'Теперь у нас больше услуг.',
    'Вакцинация против бешенства — акция!',
    'Профилактика паразитов — важна для здоровья.',
    'Семинар для владельцев кошек — бесплатно.',
    'В праздничные дни работаем по особому графику.'
]
VACANCY_TITLES = [
    'Ветеринарный врач',
    'Ассистент ветеринара',
    'Грумер',
    'Администратор',
    'Терапевт',
    'Хирург',
    'Офтальмолог',
    'Кардиолог',
    'Дерматолог',
    'Рентгенолог',
    'Лаборант',
    'Менеджер',
    'Тренер по дрессировке'
]
VACANCY_DESCRIPTIONS = [
    'Требуется опытный специалист.',
    'Работа в дружной команде.',
    'Гибкий график, достойная оплата.',
    'Возможность профессионального роста.',
    'Современное оборудование.',
    'Обучение за счёт компании.',
    'Дружелюбный коллектив.',
    'Работа с животными.',
    'Карьерный рост.',
    'Стабильная зарплата.',
    'Оформление по ТК.',
    'Бонусы и премии.',
    'Комфортные условия труда.'
]
PROMO_PREFIXES = ['WELCOME', 'SUMMER', 'VET', 'DISCOUNT', 'BONUS', 'HAPPY', 'SAVE', 'CLINIC', 'PET', 'CARE', 'FRIEND', 'FAMILY', 'NEW']

class Command(BaseCommand):
    help = 'Заполняет все основные таблицы тестовыми данными (12-13 записей в каждую)'

    def handle(self, *args, **kwargs):
        # Users, Clients
        for i in range(1, 14):
            username = f'user{i}'
            if not User.objects.filter(username=username).exists():
                first = random.choice(FIRST_NAMES)
                last = random.choice(LAST_NAMES)
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@test.com',
                    password='test1234',
                    first_name=first,
                    last_name=last
                )
                Client.objects.create(
                    user=user,
                    birth_date=date(1985, 1, 1) + timedelta(days=random.randint(0, 12000)),
                    address=f'ул. {random.choice(["Центральная", "Лесная", "Парковая", "Молодёжная", "Садовая", "Школьная", "Победы", "Мира", "Гагарина", "Озерная"])} д.{random.randint(1, 100)}',
                    phone=f'+375 (29) {random.randint(100,999)}-{random.randint(10,99)}-{random.randint(10,99)}'
                )
        self.stdout.write(self.style.SUCCESS('Клиенты созданы'))

        # DoctorCategory, Department, Specialization
        for i in range(1, 4):
            DoctorCategory.objects.get_or_create(name=f'Категория {i}')
            Department.objects.get_or_create(name=f'Отделение {i}')
            Specialization.objects.get_or_create(name=f'Специализация {i}')
        self.stdout.write(self.style.SUCCESS('Категории, отделения, специализации созданы'))

        # Doctors
        for i in range(1, 14):
            username = f'doctor{i}'
            if not User.objects.filter(username=username).exists():
                first = random.choice(FIRST_NAMES)
                last = random.choice(LAST_NAMES)
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@test.com',
                    password='test1234',
                    first_name=first,
                    last_name=last
                )
                doctor = Doctor.objects.create(
                    user=user,
                    category=DoctorCategory.objects.order_by('?').first(),
                    department=Department.objects.order_by('?').first(),
                    birth_date=date(1970, 1, 1) + timedelta(days=random.randint(0, 18000))
                )
                doctor.specializations.add(Specialization.objects.order_by('?').first())
        self.stdout.write(self.style.SUCCESS('Врачи созданы'))

        # Pets
        for i in range(1, 14):
            Pet.objects.create(
                client=Client.objects.order_by('?').first(),
                name=random.choice(PET_NAMES),
                species=random.choice(SPECIES),
                breed=random.choice(BREEDS),
                birth_date=date(2012, 1, 1) + timedelta(days=random.randint(0, 4000))
            )
        self.stdout.write(self.style.SUCCESS('Питомцы созданы'))

        # Диагнозы для каждого животного
        pets = Pet.objects.all()
        for pet in pets:
            Diagnosis.objects.create(
                pet=pet,
                doctor=Doctor.objects.order_by('?').first(),
                description=f'{random.choice(["Здоров", "Лёгкая простуда", "Паразиты", "Травма лапы", "Проблемы с зубами", "Воспаление уха", "Аллергия", "Проблемы с ЖКТ", "Вакцинация", "Плановый осмотр", "Ожирение", "Потеря аппетита", "Кожные высыпания"])} у {pet.name}',
                date=timezone.now().date() - timedelta(days=random.randint(0, 100))
            )
        self.stdout.write(self.style.SUCCESS('Диагнозы для всех питомцев созданы'))

        # Services
        for i in range(1, 14):
            Service.objects.get_or_create(
                name=SERVICE_NAMES[i-1],
                price=random.randint(10, 200),
                description=f'{SERVICE_NAMES[i-1]} — {random.choice(["быстро и качественно", "с заботой о питомце", "по акции", "с гарантией", "от лучших специалистов", "по современным стандартам"])}',
                category=random.choice(CATEGORIES)
            )
        self.stdout.write(self.style.SUCCESS('Услуги созданы'))

        # News
        for i in range(1, 14):
            News.objects.create(
                title=random.choice(NEWS_TITLES),
                summary=random.choice(NEWS_SUMMARIES),
                content=f'{random.choice(NEWS_SUMMARIES)} Подробнее на сайте.',
                published_at=timezone.now() - timedelta(days=i)
            )
        self.stdout.write(self.style.SUCCESS('Новости созданы'))

        # FAQ
        for i in range(1, 14):
            FAQ.objects.create(
                question=random.choice(FAQ_QUESTIONS),
                answer=random.choice(FAQ_ANSWERS),
                added_at=timezone.now().date() - timedelta(days=i)
            )
        self.stdout.write(self.style.SUCCESS('FAQ созданы'))

        # Contacts
        for i in range(1, 14):
            Contact.objects.create(
                name=f'{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}',
                position=random.choice(POSITIONS),
                phone=f'+375 (29) {random.randint(100,999)}-{random.randint(10,99)}-{random.randint(10,99)}',
                email=f'contact{i}@test.com',
                description=f'Специалист по {random.choice(["кошкам", "собакам", "грызунам", "птицам", "экзотическим животным", "лечению", "диагностике", "уходу"])}',
                birth_date=date(1975, 1, 1) + timedelta(days=random.randint(0, 18000))
            )
        self.stdout.write(self.style.SUCCESS('Контакты созданы'))

        # Reviews
        for i in range(1, 14):
            Review.objects.create(
                client=Client.objects.order_by('?').first(),
                rating=random.randint(3, 5),
                text=random.choice(REVIEW_TEXTS),
                date=timezone.now().date() - timedelta(days=random.randint(0, 100))
            )
        self.stdout.write(self.style.SUCCESS('Отзывы созданы'))

        # Vacancies
        for i in range(1, 14):
            Vacancy.objects.create(
                title=random.choice(VACANCY_TITLES),
                description=random.choice(VACANCY_DESCRIPTIONS),
                is_active=bool(random.getrandbits(1)),
                published_at=timezone.now() - timedelta(days=random.randint(0, 100))
            )
        self.stdout.write(self.style.SUCCESS('Вакансии созданы'))

        # PromoCodes
        for i in range(1, 14):
            code = f'{random.choice(PROMO_PREFIXES)}{random.randint(10,99)}'
            PromoCode.objects.get_or_create(
                code=code,
                defaults={
                    'discount': random.randint(5, 30),
                    'is_active': bool(random.getrandbits(1)),
                    'valid_until': timezone.now().date() + timedelta(days=random.randint(10, 100))
                }
            )
        self.stdout.write(self.style.SUCCESS('Промокоды созданы'))

        # Appointments
        for i in range(1, 14):
            appointment = Appointment.objects.create(
                client=Client.objects.order_by('?').first(),
                pet=Pet.objects.order_by('?').first(),
                doctor=Doctor.objects.order_by('?').first(),
                date=timezone.now() + timedelta(days=random.randint(1, 30)),
                diagnosis=f'{random.choice(["Плановый осмотр", "Вакцинация", "Лечение", "Операция", "Консультация", "Сдача анализов", "Профилактика"])}',
                total_price=random.randint(20, 300)
            )
            appointment.services.add(Service.objects.order_by('?').first())
        self.stdout.write(self.style.SUCCESS('Посещения созданы'))

        self.stdout.write(self.style.SUCCESS('Все тестовые данные успешно созданы!')) 