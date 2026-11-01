from django.contrib import admin

# Register your models here.
from .models import Player
admin.site.register(Player)

from .models import Venue
admin.site.register(Venue)

from .models import Club
admin.site.register(Club)

from .models import Season
admin.site.register(Season)

from .models import Game
admin.site.register(Game)

from .models import Payment
admin.site.register(Payment)