from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:Auction_id>",views.list,name="list"),   
    path("<int:Auction_id>/watchlist",views.toggle_watchlist,name="toggle_watchlist"),
  path("watchlist/list",views.user_watchlist,name="watchlist"),
  path("<str:category>/list",views.category,name="category"),
  path("create_auction",views.create_auction,name="create_auction")
]
