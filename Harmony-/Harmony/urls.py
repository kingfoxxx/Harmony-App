from.import views
from django.urls import path


#all url links for my application authentications
urlpatterns = [
    path('home', views.home, name='home-page'),
    path('signup', views.signup, name='signup'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('myartists', views.myartists, name='myartists'),
    path('search', views.search, name='search page'),
    path('', views.landing_page, name='landing_page'),
]
