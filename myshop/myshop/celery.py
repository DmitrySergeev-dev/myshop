import os
from celery import Celery

# задать стандартный модуль настроек Django для программы 'celery'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')
app = Celery('myshop')  # создаем приложение Celery
app.config_from_object('django.conf:settings', namespace='CELERY') #  загружается
# любая конкретно-прикладная конфигурация из настроек проекта. Атрибут namespace
# задает префикс, который будет в вашем файле settings.py у настроек,
# связанных с Celery. Задав именное пространство CELERY, все настройки
# Celery должны включать в свое имя префикс CELERY_ (например, CELERY_BROKER_URL);
app.autodiscover_tasks()  #  чтобы очередь заданий Celery автоматически об-
# наруживала асинхронные задания в ваших приложениях. Celery будет
# искать файл tasks.py в каждом каталоге приложений, добавленных в
# INSTALLED_APPS, чтобы загружать определенные в нем асинхронные задания
