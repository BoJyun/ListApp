from django.urls import path,include
from mainapp import views
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'music', views.MusicViewSet)

urlpatterns = [
    # path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')), ##配合授權
    path('api/music/', views.MusicViewSet2.as_view()),
    path('api/music/<int:id>/', views.MusicViewSet3.as_view()),
]