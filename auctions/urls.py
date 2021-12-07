from django.urls import path

from . import views


app_name = 'auction'
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name ="create_listing"),
    path("listing/<int:id>", views.listing, name ="listing"),
    path("<str:user>/watchlist", views.watchlist, name ="watchlist"),
    path("categories", views.categories, name ="categories"),
    path("categories/<str:title>", views.category, name = 'category'),
    path("<int:id>/bid", views.bid, name = 'bid'),
    path("/<int:id>/new_comment", views.new_comment, name ='new_comment')
]
