from django.http import Http404
from django.shortcuts import get_object_or_404

from EasyExpenseTracker.error_codes import MISSING_PARAM
from EasyExpenseTracker.utils import generate_json
from userprofile.models import Profile


def get_otp(request):
    """
        API HTTP POST /profile/otp/

        Params:
        * Email

        Return
        * Success
    """
    email = request.GET.get('email', None)
    if email is None:
        return generate_json(success=False, error=MISSING_PARAM)
    profile = get_object_or_404(Profile, email=email)
    profile.email_otp()
    return generate_json(success=True)
