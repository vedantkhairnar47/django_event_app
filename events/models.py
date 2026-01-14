from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()

    # Each event is linked to one user
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='events'
    )

    # Automatically handled timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    