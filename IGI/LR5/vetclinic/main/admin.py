from django.contrib import admin
from .models import *

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'birth_date', 'address')
    search_fields = ('user__first_name', 'user__last_name', 'phone')

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'breed', 'client')
    search_fields = ('name', 'species', 'breed', 'client__user__last_name')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'department', 'birth_date')
    search_fields = ('user__first_name', 'user__last_name', 'category__name', 'department__name')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    search_fields = ('name', 'category')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'pet', 'doctor', 'date', 'total_price')
    search_fields = ('client__user__last_name', 'pet__name', 'doctor__user__last_name')
    list_filter = ('doctor', 'date')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client', 'rating', 'date')
    search_fields = ('client__user__last_name',)
    list_filter = ('rating',)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at')
    search_fields = ('title',)
    list_filter = ('published_at',)

@admin.register(DoctorCategory)
class DoctorCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'is_active', 'valid_until')
    list_filter = ('is_active',)

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'published_at')
    list_filter = ('is_active',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'phone', 'email')
    search_fields = ('name', 'position')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'added_at')
    search_fields = ('question',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at')

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('updated_at',)

@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ('updated_at',)

@admin.register(CompanyHistory)
class CompanyHistoryAdmin(admin.ModelAdmin):
    list_display = ('about', 'year', 'event')
    list_filter = ('about', 'year')
    search_fields = ('event',)

@admin.register(CompanyRequisite)
class CompanyRequisiteAdmin(admin.ModelAdmin):
    list_display = ('about', 'key', 'value')
    list_filter = ('about',)
    search_fields = ('key', 'value') 