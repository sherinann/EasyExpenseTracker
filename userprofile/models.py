from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils.datetime_safe import datetime

import jwt
import pyotp

from EasyExpenseTracker.utils import send_mail
from userprofile.exceptions import AuthenticationFailedError


class Profile(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=250)
    picture = models.ImageField()
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    pass_key = models.CharField(default=pyotp.random_base32, editable=False, max_length=25)

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

    def generate_otp(self):
        otp = pyotp.TOTP(self.pass_key)
        return otp.now()

    def verify_otp(self, otp):
        otp_obj = pyotp.TOTP(self.pass_key)
        return otp_obj.verify(otp, valid_window=settings.OTP_VALIDITY)

    def email_otp(self):
        body = """Hi %s,
        
        Your OTP for logging in to Easy Expense Tracker is %s.
        
        Have a nice day.""".format(self.name, self.generate_otp())
        sub = "You one time password for Easy Expense Tracker"
        send_mail(self.email, sub, body)

    @classmethod
    def authenticate(cls, token: str):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except jwt.InvalidTokenError:
            raise AuthenticationFailedError
        return Profile.objects.get(email=payload['email'])
