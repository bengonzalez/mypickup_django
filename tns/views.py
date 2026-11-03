from itertools import zip_longest

from django.db.models import Prefetch
from django.shortcuts import render

from .models import Game, Season


def game_roster(request):
    seasons = Season.objects.select_related("club").prefetch_related(
        Prefetch("games", queryset=Game.objects.order_by("game_number"))
    ).order_by("club__name", "number")

    roster_rows = []

    game_id = request.GET.get("game")
    if game_id:
        selected_game = Game.objects.filter(pk=game_id).prefetch_related(
            "team1_players", "team2_players"
        ).first()
    else:
        selected_game = Game.objects.prefetch_related(
            "team1_players", "team2_players"
        ).order_by("-date").first()

    if selected_game:
        teams_by_color = {}
        for color, players in (
            (selected_game.team1_color, selected_game.team1_players.all()),
            (selected_game.team2_color, selected_game.team2_players.all()),
        ):
            teams_by_color[(color or "").strip().lower()] = players

        blue_players = teams_by_color.get("blue", [])
        red_players = teams_by_color.get("red", [])
        roster_rows = list(zip_longest(blue_players, red_players))

    return render(request, "tns/game_roster.html", {
        "seasons": seasons,
        "selected_game": selected_game,
        "roster_rows": roster_rows,
    })
