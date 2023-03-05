from django.urls import path

from .views import ImageApiView, AccountTierApiView

urlpatterns = [
    path('api/image', ImageApiView.as_view()),
    path('api/tier', AccountTierApiView.as_view()),
]