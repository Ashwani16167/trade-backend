from django.urls import path
from . import views
from .views import StockListView, add_to_watchlist
from .views import signup
from .views import LoginView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from .views import BalanceView
from .views import PasswordResetView

urlpatterns = [
    path('', views.home, name='home'),  # Homepage
    path('api/stocks/', views.stock_list, name='stock_list'),  # Stocks API endpoint
    path('api/watchlist/add/', add_to_watchlist, name='add-to-watchlist'),  # Watchlist add endpoint
    path('api/signup/', signup, name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('api/balance/', BalanceView.as_view(), name='get_balance'),
    path('api/password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('api/password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/password_reset/', PasswordResetView.as_view(), name='password_reset'),
]







