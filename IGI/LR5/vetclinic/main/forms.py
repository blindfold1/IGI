from django import forms
from django.core.validators import RegexValidator
from django.utils import timezone
from .models import Review, Client, Appointment
from django.core.exceptions import ValidationError
import re

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'text': forms.Textarea(attrs={'rows': 3, 'minlength': 10})
        }

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 1 or rating > 5:
            raise forms.ValidationError('Рейтинг должен быть от 1 до 5')
        return rating

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) < 10:
            raise forms.ValidationError('Текст отзыва должен содержать минимум 10 символов')
        return text

class ClientForm(forms.ModelForm):
    phone = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$',
                message='Телефон должен быть в формате +375 (XX) XXX-XX-XX'
            )
        ],
        widget=forms.TextInput(attrs={
            'pattern': r'\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}',
            'placeholder': '+375 (XX) XXX-XX-XX',
            'title': 'Введите номер в формате +375 (XX) XXX-XX-XX'
        })
    )
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        validators=[
            lambda value: forms.ValidationError('Дата рождения не может быть в будущем') if value > timezone.now().date() else None,
            lambda value: forms.ValidationError('Дата рождения не может быть раньше 1900 года') if value.year < 1900 else None
        ]
    )
    address = forms.CharField(
        min_length=5,
        widget=forms.TextInput(attrs={
            'minlength': '5',
            'placeholder': 'Введите адрес (минимум 5 символов)'
        })
    )

    class Meta:
        model = Client
        fields = ['phone', 'birth_date', 'address']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.startswith('+375'):
            raise forms.ValidationError('Номер должен начинаться с +375')
        return phone

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        if birth_date > timezone.now().date():
            raise forms.ValidationError('Дата рождения не может быть в будущем')
        if birth_date.year < 1900:
            raise forms.ValidationError('Дата рождения не может быть раньше 1900 года')
        return birth_date

    def clean_address(self):
        address = self.cleaned_data['address']
        if len(address) < 5:
            raise forms.ValidationError('Адрес должен содержать минимум 5 символов')
        return address

class AppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            try:
                client = Client.objects.get(user=user)
                self.fields['pet'].queryset = client.pets.all()
            except Client.DoesNotExist:
                self.fields['pet'].queryset = self.fields['pet'].queryset.none()

    class Meta:
        model = Appointment
        fields = ['pet', 'doctor', 'services', 'date', 'diagnosis']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now():
            raise forms.ValidationError('Дата и время не могут быть в прошлом')
        return date 