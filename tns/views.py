from collections import defaultdict
from itertools import zip_longest

from django.db.models import Prefetch
from django.shortcuts import render
from django.utils import timezone

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


def player_standings(request):
    current_season = Season.objects.select_related("club").order_by("-number").first()

    standings = []
    if current_season:
        played_games = current_season.games.filter(
            date__lte=timezone.now().date()
        ).prefetch_related("team1_players", "team2_players")

        totals = defaultdict(lambda: {"played": 0, "wins": 0, "losses": 0, "draws": 0})

        for game in played_games:
            team1 = list(game.team1_players.all())
            team2 = list(game.team2_players.all())

            if game.team1_score > game.team2_score:
                winners, losers, drawers = team1, team2, []
            elif game.team2_score > game.team1_score:
                winners, losers, drawers = team2, team1, []
            else:
                winners, losers, drawers = [], [], team1 + team2

            for player in team1 + team2:
                totals[player]["played"] += 1
            for player in winners:
                totals[player]["wins"] += 1
            for player in losers:
                totals[player]["losses"] += 1
            for player in drawers:
                totals[player]["draws"] += 1

        standings = sorted(
            (
                {
                    "player": player,
                    "played": data["played"],
                    "wins": data["wins"],
                    "losses": data["losses"],
                    "draws": data["draws"],
                    "points": data["wins"],
                }
                for player, data in totals.items()
            ),
            key=lambda row: (-row["points"], row["player"].name),
        )

    return render(request, "tns/player_standings.html", {
        "current_season": current_season,
        "standings": standings,
    })

def about(request):
    return render(request, 'tns/about.html', {"title": "About"})

