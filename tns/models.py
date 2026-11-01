from django.db import models

# Create your models here.


class Venue(models.Model):
    name = models.CharField(max_length=30)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Club(models.Model):
    name = models.CharField(max_length=25)
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True, related_name="clubs")

    def __str__(self):
        return self.name


class Season(models.Model):
    number = models.PositiveIntegerField()
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="seasons")

    def __str__(self):
        return f"Season {self.number} ({self.club.name})"

class Player(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    clubs = models.ManyToManyField(Club, blank=True, related_name="players")

    def __str__(self):
        return self.name

class Game(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="games")
    game_number = models.PositiveIntegerField()
    date = models.DateField()
    fee = models.DecimalField(max_digits=6, decimal_places=2)

    team1_captain = models.ForeignKey(
        Player, on_delete=models.SET_NULL, null=True, blank=True, related_name="team1_captain_games"
    )
    team2_captain = models.ForeignKey(
        Player, on_delete=models.SET_NULL, null=True, blank=True, related_name="team2_captain_games"
    )

    team1_players = models.ManyToManyField(Player, blank=True, related_name="team1_games")
    team2_players = models.ManyToManyField(Player, blank=True, related_name="team2_games")

    team1_color = models.CharField(max_length=20)
    team2_color = models.CharField(max_length=20)

    team1_score = models.PositiveIntegerField(default=0)
    team2_score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Game {self.game_number} - {self.season}"


class Payment(models.Model):
    season = models.ForeignKey(Season, on_delete=models.SET_NULL, null=True, related_name="payments")
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True, related_name="payments")
    date = models.DateField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, related_name="payments")
    type = models.CharField(max_length=30)

    def __str__(self):
        return f"Payment {self.amount} - {self.player}"
