from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import ReviewForm, ClientForm, AppointmentForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
import requests
import logging
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.conf import settings
from django.db.models import Avg, Count, Max, Min, Sum
import statistics
from datetime import date
from django.db import models
import calendar
from django.utils import timezone
from django.db.models.functions import ExtractWeekDay
import json
from datetime import datetime, timedelta
import random
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
import io
import base64
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

def index(request):
    reviews = Review.objects.all().order_by('-date')[:6]
    services = Service.objects.all()[:6]
    doctors = Doctor.objects.select_related('user', 'category', 'department').all()[:6]
    total_clients = Client.objects.count()
    total_pets = Pet.objects.count()
    total_appointments = Appointment.objects.count()
    latest_news = News.objects.order_by('-published_at')[:3]
    return render(request, 'main/index.html', {
        'reviews': reviews,
        'services': services,
        'doctors': doctors,
        'total_clients': total_clients,
        'total_pets': total_pets,
        'total_appointments': total_appointments,
        'latest_news': latest_news,
    })

def about(request):
    about = About.objects.first()
    return render(request, 'main/about.html', {'about': about})

class NewsListView(ListView):
    model = News
    template_name = 'main/news_list.html'
    context_object_name = 'news_list'
    ordering = ['-published_at']

class NewsDetailView(DetailView):
    model = News
    template_name = 'main/news_detail.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_list'] = News.objects.exclude(pk=self.object.pk).order_by('-published_at')[:5]
        return context

@method_decorator(login_required, name='dispatch')
class NewsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    template_name = 'main/news_form.html'
    fields = ['title', 'content', 'image']
    success_url = reverse_lazy('news_list')

    def test_func(self):
        return self.request.user.is_staff

@method_decorator(login_required, name='dispatch')
class NewsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = News
    template_name = 'main/news_confirm_delete.html'
    success_url = reverse_lazy('news_list')

    def test_func(self):
        return self.request.user.is_staff

class FAQListView(ListView):
    model = FAQ
    template_name = 'main/faq.html'
    context_object_name = 'faq_list'
    ordering = ['-added_at']

class ContactListView(ListView):
    model = Contact
    template_name = 'main/contacts.html'
    context_object_name = 'contact_list'
    ordering = ['name']

def privacy(request):
    return render(request, 'main/privacy.html')

def vacancies(request):
    vacancies = Vacancy.objects.filter(is_active=True).order_by('-published_at')
    return render(request, 'main/vacancies.html', {'vacancies': vacancies})

def promos(request):
    promos = PromoCode.objects.filter(is_active=True).order_by('-valid_until')
    return render(request, 'main/promos.html', {'promos': promos})

def reviews(request):
    reviews = Review.objects.all().order_by('-date')
    return render(request, 'main/reviews.html', {'reviews': reviews})

@login_required
def add_review(request):
    if request.method == 'POST':
        try:
            client = Client.objects.get(user=request.user)
        except Client.DoesNotExist:
            messages.error(request, 'Для добавления отзыва необходимо создать профиль клиента.')
            return redirect('client_create')
        rating = int(request.POST.get('rating'))
        text = request.POST.get('text')
        if not (1 <= rating <= 5):
            messages.error(request, 'Оценка должна быть от 1 до 5')
            return redirect('reviews')
        if not text:
            messages.error(request, 'Текст отзыва не может быть пустым')
            return redirect('reviews')
        Review.objects.create(
            client=client,
            rating=rating,
            text=text
        )
        messages.success(request, 'Отзыв успешно добавлен!')
    return redirect('reviews')

@login_required
def client_detail(request):
    if request.user.is_staff:
        return render(request, 'main/admin_profile.html')
    try:
        client = Client.objects.get(user=request.user)
        pets = Pet.objects.filter(client=client)
        appointments = Appointment.objects.filter(client=client).order_by('-date')
        return render(request, 'main/client_detail.html', {
            'client': client,
            'pets': pets,
            'appointments': appointments
        })
    except Client.DoesNotExist:
        messages.error(request, 'Профиль клиента не найден')
        return redirect('index')

@login_required
def client_edit(request):
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        messages.error(request, 'Сначала создайте профиль клиента!')
        return redirect('client_create')
    if request.method == 'POST':
        client.address = request.POST.get('address')
        client.phone = request.POST.get('phone')
        client.save()
        messages.success(request, 'Профиль успешно обновлён!')
        return redirect('client_detail')
    return render(request, 'main/client_edit.html', {'client': client})

@login_required
def client_delete(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('index')
    return render(request, 'main/client_delete.html')

@method_decorator(login_required, name='dispatch')
class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'main/review_form.html'
    success_url = reverse_lazy('reviews')

    def form_valid(self, form):
        form.instance.client = self.request.user.client
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'main/client_detail.html'
    context_object_name = 'client'

    def get_object(self):
        return get_object_or_404(Client, user=self.request.user)

@method_decorator(login_required, name='dispatch')
class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'main/client_form.html'
    success_url = reverse_lazy('client_detail')

    def get_object(self):
        return get_object_or_404(Client, user=self.request.user)

@method_decorator(login_required, name='dispatch')
class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'main/client_confirm_delete.html'
    success_url = reverse_lazy('index')

    def get_object(self):
        return get_object_or_404(Client, user=self.request.user)

@method_decorator(login_required, name='dispatch')
class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'main/appointment_form.html'
    success_url = reverse_lazy('client_detail')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        try:
            form.instance.client = self.request.user.client
        except Client.DoesNotExist:
            messages.error(self.request, 'Сначала заполните профиль клиента!')
            return redirect('client_create')
        # Считаем стоимость как сумму цен выбранных услуг
        total = sum(service.price for service in form.cleaned_data['services'])
        form.instance.total_price = total
        response = super().form_valid(form)
        messages.success(self.request, 'Запись на приём успешно создана!')
        return response

@method_decorator(login_required, name='dispatch')
class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'main/appointment_detail.html'
    context_object_name = 'appointment'

    def get_queryset(self):
        return Appointment.objects.filter(client__user=self.request.user)

@method_decorator(login_required, name='dispatch')
class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'main/appointment_form.html'
    success_url = reverse_lazy('client_detail')

    def get_queryset(self):
        return Appointment.objects.filter(client__user=self.request.user)

@method_decorator(login_required, name='dispatch')
class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    template_name = 'main/appointment_confirm_delete.html'
    success_url = reverse_lazy('client_detail')

    def get_queryset(self):
        return Appointment.objects.filter(client__user=self.request.user)

def weather_and_currency(request):
    # Погода (пример: Open-Meteo)
    weather = None
    try:
        resp = requests.get('https://api.open-meteo.com/v1/forecast?latitude=53.9&longitude=27.5667&current_weather=true')
        if resp.status_code == 200:
            data = resp.json()
            weather = {
                'temperature': data['current_weather']['temperature'],
                'windspeed': data['current_weather']['windspeed'],
                'weathercode': data['current_weather']['weathercode'],
            }
    except Exception as e:
        weather = {'error': str(e)}

    # Курс валют (Frankfurter API)
    currency = {}
    try:
        resp = requests.get('https://api.frankfurter.app/latest?from=USD&to=BYN,EUR,RUB')
        if resp.status_code == 200:
            data = resp.json()
            if 'rates' in data:
                currency = data['rates']
            else:
                currency = {'error': 'Нет данных о курсах валют'}
        else:
            currency = {'error': f'Ошибка API: {resp.status_code}'}
    except Exception as e:
        currency = {'error': str(e)}

    return render(request, 'main/weather_and_currency.html', {'weather': weather, 'currency': currency})

# --- Статистика и визуализация ---
@staff_member_required
def statistics(request):
    total_clients = Client.objects.count()
    total_pets = Pet.objects.count()
    total_appointments = Appointment.objects.count()
    avg_rating = Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0

    popular_services = Service.objects.annotate(
        count=Count('appointment')
    ).order_by('-count')[:5]

    # График популярных услуг
    service_names = [s.name for s in popular_services]
    service_counts = [s.count for s in popular_services]
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(service_names, service_counts, color='#4a90e2')
    ax.set_ylabel('Количество записей')
    ax.set_title('Популярные услуги')
    plt.xticks(rotation=20, ha='right')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    services_chart = base64.b64encode(buf.read()).decode('utf-8')

    # График записей по дням недели
    appointments_by_day = Appointment.objects.annotate(
        weekday=ExtractWeekDay('date')
    ).values('weekday').annotate(
        count=Count('id')
    ).order_by('weekday')
    days_ru = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    appointments_data = [0] * 7
    for day in appointments_by_day:
        appointments_data[day['weekday'] - 1] = day['count']
    fig2, ax2 = plt.subplots(figsize=(6, 3))
    ax2.bar(days_ru, appointments_data, color='#f39c12')
    ax2.set_ylabel('Количество записей')
    ax2.set_title('Записи по дням недели')
    plt.tight_layout()
    buf2 = io.BytesIO()
    plt.savefig(buf2, format='png')
    plt.close(fig2)
    buf2.seek(0)
    appointments_chart = base64.b64encode(buf2.read()).decode('utf-8')

    # График видов животных
    pets_by_species = Pet.objects.values('species').annotate(
        count=Count('id')
    ).order_by('-count')
    species_names = [p['species'] for p in pets_by_species]
    species_counts = [p['count'] for p in pets_by_species]
    fig3, ax3 = plt.subplots(figsize=(5, 5))
    ax3.pie(species_counts, labels=species_names, autopct='%1.0f%%', startangle=90)
    ax3.set_title('Виды животных')
    plt.tight_layout()
    buf3 = io.BytesIO()
    plt.savefig(buf3, format='png')
    plt.close(fig3)
    buf3.seek(0)
    pets_chart = base64.b64encode(buf3.read()).decode('utf-8')

    # График распределения рейтингов
    ratings_distribution = Review.objects.values('rating').annotate(
        count=Count('id')
    ).order_by('rating')
    ratings_data = [0] * 5
    for rating in ratings_distribution:
        ratings_data[rating['rating'] - 1] = rating['count']
    fig4, ax4 = plt.subplots(figsize=(6, 3))
    ax4.bar([str(i) for i in range(1, 6)], ratings_data, color='#2ecc71')
    ax4.set_ylabel('Количество отзывов')
    ax4.set_xlabel('Оценка')
    ax4.set_title('Распределение рейтингов')
    plt.tight_layout()
    buf4 = io.BytesIO()
    plt.savefig(buf4, format='png')
    plt.close(fig4)
    buf4.seek(0)
    ratings_chart = base64.b64encode(buf4.read()).decode('utf-8')

    context = {
        'total_clients': total_clients,
        'total_pets': total_pets,
        'total_appointments': total_appointments,
        'avg_rating': avg_rating,
        'popular_services': popular_services,
        'appointments_by_day': zip(days_ru, appointments_data),
        'pets_by_species': pets_by_species,
        'ratings_distribution': enumerate(ratings_data, start=1),
        'services_chart': services_chart,
        'appointments_chart': appointments_chart,
        'pets_chart': pets_chart,
        'ratings_chart': ratings_chart,
    }
    return render(request, 'main/statistics.html', context)

def quote_view(request):
    quote = None
    try:
        # Пробуем получить цитату с основного API
        resp = requests.get('https://api.quotable.io/random?lang=ru', verify=False)
        if resp.status_code == 200:
            data = resp.json()
            quote = {
                'content': data.get('content', ''),
                'author': data.get('author', '')
            }
    except Exception as e:
        # Если не получилось, используем запасной вариант
        quotes = [
            {'content': 'Здоровье - это не всё, но всё ничто без здоровья.', 'author': 'Сократ'},
            {'content': 'Лучший врач тот, кто знает бесполезность большинства лекарств.', 'author': 'Бенджамин Франклин'},
            {'content': 'Здоровье - это состояние полного физического, душевного и социального благополучия.', 'author': 'ВОЗ'},
            {'content': 'Предупредить легче, чем лечить.', 'author': 'Народная мудрость'},
            {'content': 'Здоровье - это богатство, которое нельзя купить.', 'author': 'Народная мудрость'}
        ]
        quote = random.choice(quotes)
    
    return render(request, 'main/quote.html', {'quote': quote})

def service_list(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', 'name')
    services = Service.objects.all()
    if query:
        services = services.filter(name__icontains=query)
    if sort == 'price':
        services = services.order_by('price')
    else:
        services = services.order_by('name')
    return render(request, 'main/service_list.html', {'services': services, 'query': query, 'sort': sort})

def client_list(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', 'name')
    clients = Client.objects.select_related('user').all()
    if query:
        clients = clients.filter(
            models.Q(user__first_name__icontains=query) |
            models.Q(user__last_name__icontains=query) |
            models.Q(phone__icontains=query)
        )
    if sort == 'birth_date':
        clients = clients.order_by('birth_date')
    else:
        clients = clients.order_by('user__last_name', 'user__first_name')
    return render(request, 'main/client_list.html', {'clients': clients, 'query': query, 'sort': sort})

def pet_list(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', 'name')
    pets = Pet.objects.select_related('client', 'client__user').all()
    if query:
        pets = pets.filter(
            models.Q(name__icontains=query) |
            models.Q(species__icontains=query) |
            models.Q(breed__icontains=query) |
            models.Q(client__user__last_name__icontains=query) |
            models.Q(client__user__first_name__icontains=query)
        )
    if sort == 'birth_date':
        pets = pets.order_by('birth_date')
    else:
        pets = pets.order_by('name')
    return render(request, 'main/pet_list.html', {'pets': pets, 'query': query, 'sort': sort})

def client_by_phone(request, phone):
    # phone приходит в формате 37529123123 (без +, скобок и дефисов)
    phone_pattern = f'+375 ({phone[3:5]}) {phone[5:8]}-{phone[8:10]}-{phone[10:12]}'
    client = Client.objects.filter(phone=phone_pattern).first()
    return render(request, 'main/client_by_phone.html', {'client': client, 'phone': phone_pattern})

def datetime_view(request):
    now_utc = timezone.now()
    now_local = timezone.localtime(now_utc)
    cal = calendar.TextCalendar()
    cal_str = cal.formatmonth(now_local.year, now_local.month)
    return render(request, 'main/datetime.html', {
        'now_utc': now_utc,
        'now_local': now_local,
        'calendar': cal_str,
    })

def info(request):
    # Получение данных о погоде
    weather = {'temperature': 0, 'humidity': 0, 'weathercode': 0, 'description': 'Нет данных'}
    try:
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": 53.9,
            "longitude": 27.6,
            "current": "temperature_2m,relative_humidity_2m,weather_code",
            "timezone": "auto"
        }
        weather_response = requests.get(weather_url, params=weather_params, timeout=3)
        weather_data = weather_response.json()
        weather = {
            'temperature': round(weather_data['current']['temperature_2m']),
            'humidity': weather_data['current']['relative_humidity_2m'],
            'weathercode': weather_data['current']['weather_code'],
            'description': get_weather_description(weather_data['current']['weather_code'])
        }
    except Exception as e:
        pass

    # Получение курсов валют
    currencies = [
        {'code': 'EUR', 'rate': '1.0000'},
        {'code': 'USD', 'rate': '1.1000'},
        {'code': 'GBP', 'rate': '0.8500'},
        {'code': 'BYN', 'rate': '3.5000'}
    ]
    try:
        currency_url = "https://api.frankfurter.app/latest"
        currency_params = {
            "from": "EUR",
            "to": "USD,GBP,BYN"
        }
        currency_response = requests.get(currency_url, params=currency_params, timeout=3)
        currency_data = currency_response.json()
        currencies = [
            {'code': 'EUR', 'rate': '1.0000'},
            {'code': 'USD', 'rate': f"{currency_data['rates']['USD']:.4f}"},
            {'code': 'GBP', 'rate': f"{currency_data['rates']['GBP']:.4f}"},
            {'code': 'BYN', 'rate': f"{currency_data['rates']['BYN']:.4f}"}
        ]
    except Exception as e:
        pass

    # Получение списка врачей
    doctors = Doctor.objects.select_related('user', 'category', 'department').all()
    # Получение списка питомцев
    pets = Pet.objects.all()[:6]
    context = {
        'weather': weather,
        'currencies': currencies,
        'doctors': doctors,
        'pets': pets
    }
    return render(request, 'main/info.html', context)

def get_weather_description(code):
    weather_codes = {
        0: "Ясно",
        1: "Преимущественно ясно",
        2: "Переменная облачность",
        3: "Пасмурно",
        45: "Туман",
        48: "Туман с инеем",
        51: "Легкая морось",
        53: "Умеренная морось",
        55: "Сильная морось",
        61: "Небольшой дождь",
        63: "Умеренный дождь",
        65: "Сильный дождь",
        71: "Небольшой снег",
        73: "Умеренный снег",
        75: "Сильный снег",
        77: "Снежные зерна",
        80: "Небольшой ливень",
        81: "Умеренный ливень",
        82: "Сильный ливень",
        85: "Небольшой снегопад",
        86: "Сильный снегопад",
        95: "Гроза",
        96: "Гроза с небольшим градом",
        99: "Гроза с сильным градом"
    }
    return weather_codes.get(code, "Неизвестно")

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    related_services = Service.objects.filter(category=service.category).exclude(pk=pk)[:3]
    return render(request, 'main/service_detail.html', {
        'service': service,
        'related_services': related_services
    })

@staff_member_required
def admin_panel(request):
    clients = Client.objects.select_related('user').all()
    doctors = Doctor.objects.select_related('user', 'category', 'department').all()
    pets = Pet.objects.select_related('client', 'client__user').all()
    services = Service.objects.all()
    appointments = Appointment.objects.select_related('client', 'pet', 'doctor').all()
    reviews = Review.objects.select_related('client', 'client__user').all()
    return render(request, 'main/admin_panel.html', {
        'clients': clients,
        'doctors': doctors,
        'pets': pets,
        'services': services,
        'appointments': appointments,
        'reviews': reviews,
    })

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def client_create(request):
    if hasattr(request.user, 'client'):
        messages.info(request, 'Профиль уже создан.')
        return redirect('client_detail')
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.user = request.user
            client.save()
            messages.success(request, 'Профиль успешно создан!')
            return redirect('client_detail')
    else:
        form = ClientForm()
    return render(request, 'main/client_create.html', {'form': form})

@login_required
def pet_create(request):
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        messages.error(request, 'Сначала создайте профиль клиента!')
        return redirect('client_create')
    if request.method == 'POST':
        name = request.POST.get('name')
        species = request.POST.get('species')
        breed = request.POST.get('breed')
        birth_date = request.POST.get('birth_date')
        if not name or not species or not birth_date:
            messages.error(request, 'Заполните все обязательные поля!')
        else:
            Pet.objects.create(client=client, name=name, species=species, breed=breed, birth_date=birth_date)
            messages.success(request, 'Питомец успешно добавлен!')
            return redirect('client_detail')
    return render(request, 'main/pet_create.html')

@staff_member_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    review.delete()
    messages.success(request, 'Отзыв удалён.')
    return redirect('reviews')

@staff_member_required
def all_appointments(request):
    appointments = Appointment.objects.select_related('client', 'pet', 'doctor').all().order_by('-date')
    return render(request, 'main/all_appointments.html', {'appointments': appointments})

@staff_member_required
def delete_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.delete()
    messages.success(request, 'Запись отклонена/удалена.')
    return redirect('all_appointments') 