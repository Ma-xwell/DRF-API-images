from django.urls import path

from .views import AccountTierApiView, ImageView

urlpatterns = [
    path('images', ImageView.as_view()),
    path('tiers', AccountTierApiView.as_view())
]