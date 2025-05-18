from django.urls import path
from .views import StartStreamView,RegisterView,SignInView

urlpatterns = [
    path('stream/', StartStreamView.as_view()),
    path('api/register/', RegisterView.as_view() ,name='register'),
    path("api/signin/",SignInView.as_view(), name='signin'),
]