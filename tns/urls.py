from django.urls import path

from . import views

urlpatterns = [
    path('', views.game_roster, name="tns-home"),
    path("games/roster/", views.game_roster, name="game-roster"),
    path("standings/", views.player_standings, name="player-standings"),
    path('about/', views.about, name='tns-about'),
]
