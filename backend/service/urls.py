from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from app.views import AchievementViewSet, CatViewSet, GetChat, GetUser

router = routers.DefaultRouter()
router.register(r'cats', CatViewSet)
router.register(r'achievements', AchievementViewSet)


urlpatterns = [
    path('log/', include('logger.urls')),
    path('api/userlist/', GetUser.as_view()),
    path('api/chathistory/<int:pk>/', GetChat.as_view()),
    
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('djoser.urls')),  # Работа с пользователями
    path('api/', include('djoser.urls.authtoken')),  # Работа с токенами
    path("chat/", include('app.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
