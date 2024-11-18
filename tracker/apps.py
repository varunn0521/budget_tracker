from django.apps import AppConfig

class TrackerConfig(AppConfig):
    name = 'tracker'

    def ready(self):
        # Import and connect the signals when the app is ready
        import tracker.signals
