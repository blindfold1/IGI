from django.core.management.base import BaseCommand
from main.models import About, CompanyHistory, CompanyRequisite
from django.core.files.base import ContentFile
from django.utils import timezone
import urllib.request

class Command(BaseCommand):
    help = 'Автоматически заполняет раздел О компании: логотип, текст, история, реквизиты.'

    def handle(self, *args, **kwargs):
        # 1. Создаём или обновляем About
        about, created = About.objects.get_or_create(id=1)
        about.content = (
            "Ветеринарная клиника 'Забота' — современный центр помощи животным. "
            "Мы работаем с 2010 года, оказываем полный спектр ветеринарных услуг, "
            "используем современное оборудование и заботимся о каждом пациенте."
        )
        # Логотип (минималистичный, как у компании)
        logo_url = 'https://cdn-icons-png.flaticon.com/512/616/616408.png'
        try:
            result = urllib.request.urlopen(logo_url)
            about.logo.save('logo_company.png', ContentFile(result.read()), save=False)
        except Exception:
            pass
        about.save()

        # 2. История по годам
        CompanyHistory.objects.filter(about=about).delete()
        history = [
            (2010, 'Открытие клиники'),
            (2012, 'Появление круглосуточного приёма'),
            (2015, 'Открытие лаборатории диагностики'),
            (2018, 'Внедрение онлайн-записи и электронной карты пациента'),
            (2022, 'Переезд в новое современное здание'),
        ]
        for year, event in history:
            CompanyHistory.objects.create(about=about, year=year, event=event)

        # 3. Реквизиты
        CompanyRequisite.objects.filter(about=about).delete()
        requisites = [
            ('ИНН', '1234567890'),
            ('ОГРН', '1097746381234'),
            ('Юридический адрес', 'г. Минск, ул. Восточная, 66'),
            ('Телефон', '+375 (29) 123-45-67'),
            ('E-mail', 'info@vetclinic.by'),
            ('Банк', 'ОАО "Беларусбанк"'),
            ('Р/с', 'BY13 BPSB 3012 3456 7890 1234 5678'),
        ]
        for key, value in requisites:
            CompanyRequisite.objects.create(about=about, key=key, value=value)

        self.stdout.write(self.style.SUCCESS('Раздел "О компании" успешно заполнен!')) 