from django.apps import AppConfig


class UsersConfig(AppConfig):
    # default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        # Import the signals module to ensure the signals are registered
        import users.signals
        # This will connect the signals defined in users/signals.py
        # to the appropriate model events, such as post_save for User.
        # This is necessary to ensure that the signal handlers are executed
        # when the corresponding model events occur.
        # The import statement should be placed here to avoid circular imports.
        # By importing it in the ready method, we ensure that the signals are connected
        # when the application starts, allowing the signal handlers to function correctly.
        # Make sure that the signals module is correctly defined in users/signals.py
        # and that it contains the necessary signal handlers for the User model.
        # This is a common pattern in Django applications to manage signals effectively.
        
