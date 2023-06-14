from django.contrib import admin
from django.urls import path, include


admin.site.site_header = 'Мой учебный блог'
admin.site.index_title = 'Разделы админки Блога'
admin.site.site_title = 'Админка Блога'


urlpatterns = [
    path('admin/', admin.site.urls),
]
