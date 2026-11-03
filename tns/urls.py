from django.urls import path

from . import views

urlpatterns = [
    path("games/roster/", views.game_roster, name="game-roster"),
]
