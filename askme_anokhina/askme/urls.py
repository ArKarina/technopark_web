from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('hot', views.hot, name = 'hot'),
    path('question/<int:question_id>', views.question, name = 'question'),
    path('ask', views.ask, name = 'ask'),
    path('login', views.login, name = 'login'),
    path('signup', views.signup, name = 'signup'),
    path('settings', views.settings, name = 'settings'),
    path('tag/<str:tag_name>', views.tag, name = 'tag'),
    path('logout', views.logout, name='logout'),
    path('likeQuestion', views.likeQuestion, name='likeQuestion'),
    path('likeAnswer', views.likeAnswer, name='likeAnswer'),
    path('correctAnswer', views.correctAnswer, name='correctAnswer'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
