from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.datetime_safe import datetime

import jwt

from userprofile.exceptions import AuthenticationFailedError


class Profile(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=250)
    picture = models.ImageField()
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    @property
    def serialize(self):
        return {
            "email": self.email,
            "name": self.name,
            "picture": self.picture
        }

    def generate_token(self):
        payload = {
            'email': self.email,
            'iat': datetime.utcnow(),
        }
        return jwt.encode(payload, settings.SECRET_KEY)

    @classmethod
    def authenticate(cls, token: str):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except jwt.InvalidTokenError:
            raise AuthenticationFailedError
        return Profile.objects.get(email=payload['email'])
