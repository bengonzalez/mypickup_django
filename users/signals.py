from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
# This code listens for the post_save signal of the User model.
# When a User instance is created, it automatically creates a Profile instance linked to that user.
# It also ensures that the Profile instance is saved whenever the User instance is saved.
# This is useful for maintaining a one-to-one relationship between User and Profile models.
# The `Profile` model should have a ForeignKey or OneToOneField linking it to the `User` model.
# Make sure to import this signals module in your app's ready method
# to ensure the signals are registered when the application starts.
# For example, in your apps.py:
# from django.apps import AppConfig
# class YourAppConfig(AppConfig):
#     name = 'your_app_name'
#     def ready(self):
#         import your_app_name.signals
# This ensures that the signals are connected when the app is ready.



