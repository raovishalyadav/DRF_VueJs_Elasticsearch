from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from drfelastic import views

router = routers.DefaultRouter()
router.register(r'articles', views.ArticleViewSet)

urlpatterns = [
    path('api/articles/search/', views.ArticleViewSet.as_view({'get': 'search'})),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
