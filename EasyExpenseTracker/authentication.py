from EasyExpenseTracker.error_codes import TOKEN_NOT_FOUND, INVALID_TOKEN
from EasyExpenseTracker.utils import generate_json
from userprofile.models import Profile, AuthenticationFailedError


def token_required(view):
    def new_view(request):
        try:
            token = request.POST['token']
        except KeyError:
            return generate_json(sucess=False, data={'code': TOKEN_NOT_FOUND})
        try:
            profile = Profile.authenticate(token)
        except AuthenticationFailedError:
            return generate_json(sucess=False, data={'code': INVALID_TOKEN})
        request.profile = profile
        return view(request)

    return new_view
