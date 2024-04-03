from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)
    username = models.CharField(
        max_length=100,
        blank=True,
        unique=True,
        db_index=True,
    )
    password = models.CharField(max_length=30, blank=True)
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following", blank=True
    )

    def follow(self, user):
        """
        Method to follow another user
        """
        self.following.add(user)

    def unfollow(self, user):
        """
        Method to unfollow another user
        """
        self.following.remove(user)

    def is_following(self, user):
        """
        Method to check if the user is following another user
        """
        return self.following.filter(pk=user.pk).exists()

    def is_followed_by(self, user):
        """
        Method to check if the user is followed by another user
        """
        return self.followers.filter(pk=user.pk).exists()
