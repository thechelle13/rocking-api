from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rockapi.views import register_user, login_user
from rockapi.views import TypeView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'types', TypeView, 'type')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
]
