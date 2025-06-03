from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from datetime import date

# --- Вспомогательные функции ---
def validate_phone(value):
    pattern = r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$'
    if not re.match(pattern, value):
        raise ValidationError('Формат: +375 (29) XXX-XX-XX')

def validate_adult(birth_date):
    age = (date.today() - birth_date).days // 365
    if age < 18:
        raise ValidationError('Возраст должен быть 18+')

# --- Клиент ---
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    birth_date = models.DateField(validators=[validate_adult], verbose_name='Дата рождения')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    phone = models.CharField(max_length=20, validators=[validate_phone], help_text='Формат: +375 (29) XXX-XX-XX', verbose_name='Телефон')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменено', null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.phone})"
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

# --- Домашнее животное (пациент) ---
class Pet(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='pets', verbose_name='Владелец')
    name = models.CharField(max_length=100, verbose_name='Кличка')
    species = models.CharField(max_length=50, verbose_name='Вид')
    breed = models.CharField(max_length=50, blank=True, verbose_name='Порода')
    birth_date = models.DateField(verbose_name='Дата рождения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменено', null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.species})"
    class Meta:
        verbose_name = 'Домашнее животное'
        verbose_name_plural = 'Домашние животные'

# --- Категория врача ---
class DoctorCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Категория врача'
        verbose_name_plural = 'Категории врачей'

# --- Отделение ---
class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name='Отделение')
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Отделение'
        verbose_name_plural = 'Отделения'

# --- Специализация врача ---
class Specialization(models.Model):
    name = models.CharField(max_length=100, verbose_name='Специализация')
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Специализация врача'
        verbose_name_plural = 'Специализации врачей'

# --- Врач ---
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    category = models.ForeignKey(DoctorCategory, on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, verbose_name='Отделение')
    specializations = models.ManyToManyField(Specialization, blank=True, verbose_name='Специализации')
    birth_date = models.DateField(validators=[validate_adult], verbose_name='Дата рождения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменено', null=True, blank=True)
    
    def __str__(self):
        return self.user.get_full_name()
    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'

# --- Диагноз ---
class Diagnosis(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='diagnoses', verbose_name='Пациент')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, verbose_name='Врач')
    description = models.TextField(verbose_name='Описание')
    date = models.DateField(auto_now_add=True, verbose_name='Дата постановки')
    
    def __str__(self):
        return f"{self.pet.name} - {self.description[:30]}"
    class Meta:
        verbose_name = 'Диагноз'
        verbose_name_plural = 'Диагнозы'

# --- Услуга ---
class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')
    description = models.TextField(verbose_name='Описание')
    category = models.CharField(max_length=100, verbose_name='Категория услуги')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменено', null=True, blank=True)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

# --- Заказ/Посещение ---
class Appointment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name='Пациент')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, verbose_name='Врач')
    services = models.ManyToManyField(Service, verbose_name='Услуги')
    date = models.DateTimeField(verbose_name='Дата и время')
    diagnosis = models.TextField(blank=True, null=True, verbose_name='Диагноз')
    promo_code = models.ForeignKey('PromoCode', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Промокод')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменено', null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Итоговая стоимость')
    
    def __str__(self):
        return f"{self.client.user.get_full_name()} - {self.date.strftime('%d/%m/%Y')}"
    class Meta:
        verbose_name = 'Посещение'
        verbose_name_plural = 'Посещения'

# --- Промокод/Купон ---
class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name='Код')
    discount = models.PositiveIntegerField(help_text='Скидка в процентах', verbose_name='Скидка (%)')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    valid_until = models.DateField(verbose_name='Действителен до')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменено', null=True, blank=True)
    
    def __str__(self):
        return self.code
    class Meta:
        verbose_name = 'Промокод/Купон'
        verbose_name_plural = 'Промокоды и купоны'

# --- Новость ---
class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    summary = models.CharField(max_length=300, verbose_name='Краткое содержание')
    content = models.TextField(verbose_name='Текст')
    image = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name='Картинка')
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменено', null=True, blank=True)
    
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

# --- Вакансия ---
class Vacancy(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменено', null=True, blank=True)
    
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

# --- Отзыв ---
class Review(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    rating = models.PositiveSmallIntegerField(verbose_name='Оценка')
    text = models.TextField(verbose_name='Текст')
    date = models.DateField(auto_now_add=True, verbose_name='Дата')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменено', null=True, blank=True)
    
    def __str__(self):
        return f"{self.client.user.get_full_name()} - {self.rating}"
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

# --- Контакт (сотрудник) ---
class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name='ФИО')
    position = models.CharField(max_length=100, verbose_name='Должность')
    phone = models.CharField(max_length=20, validators=[validate_phone], verbose_name='Телефон')
    email = models.EmailField(verbose_name='Почта')
    photo = models.ImageField(upload_to='contacts/', blank=True, null=True, verbose_name='Фото')
    description = models.TextField(blank=True, verbose_name='Описание')
    birth_date = models.DateField(validators=[validate_adult], verbose_name='Дата рождения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменено', null=True, blank=True)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Контакт (сотрудник)'
        verbose_name_plural = 'Контакты (сотрудники)'

# --- FAQ (Словарь терминов и понятий) ---
class FAQ(models.Model):
    question = models.CharField(max_length=300, verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')
    added_at = models.DateField(auto_now_add=True, verbose_name='Дата добавления')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменено', null=True, blank=True)
    
    def __str__(self):
        return self.question
    class Meta:
        verbose_name = 'Вопрос-ответ (FAQ)'
        verbose_name_plural = 'Вопросы-ответы (FAQ)'

# --- Статья (для главной и новостей) ---
class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

# --- О компании (About) ---
class About(models.Model):
    content = models.TextField(verbose_name='Текст')
    logo = models.ImageField(upload_to='about/', blank=True, null=True, verbose_name='Логотип')
    video_url = models.URLField(blank=True, null=True, verbose_name='Видео о компании (YouTube)')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    
    def __str__(self):
        return "О компании"
    class Meta:
        verbose_name = 'О компании'
        verbose_name_plural = 'О компании'

# --- Политика конфиденциальности ---
class PrivacyPolicy(models.Model):
    content = models.TextField(blank=True, verbose_name='Текст')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    
    def __str__(self):
        return "Политика конфиденциальности"
    class Meta:
        verbose_name = 'Политика конфиденциальности'
        verbose_name_plural = 'Политика конфиденциальности'

# --- История компании ---
class CompanyHistory(models.Model):
    about = models.ForeignKey(About, on_delete=models.CASCADE, related_name='history', verbose_name='О компании')
    year = models.PositiveIntegerField(verbose_name='Год')
    event = models.CharField(max_length=300, verbose_name='Событие')
    
    def __str__(self):
        return f"{self.year}: {self.event[:30]}"
    class Meta:
        verbose_name = 'История компании'
        verbose_name_plural = 'История компании'
        ordering = ['year']

# --- Реквизит компании ---
class CompanyRequisite(models.Model):
    about = models.ForeignKey(About, on_delete=models.CASCADE, related_name='requisites', verbose_name='О компании')
    key = models.CharField(max_length=100, verbose_name='Параметр')
    value = models.CharField(max_length=300, verbose_name='Значение')
    
    def __str__(self):
        return f"{self.key}: {self.value}"
    class Meta:
        verbose_name = 'Реквизит компании'
        verbose_name_plural = 'Реквизиты компании' 