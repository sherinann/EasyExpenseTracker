from django.http import JsonResponse


def generate_json(success=True, error=None, data={}):
    ret = dict(data)
    ret["success"] = success
    if error is not None:
        ret['error_code'] = error
    return JsonResponse(ret)


def send_mail(to, subject, body):
    print(to)
    print("Sub: " + subject)
    print(body)
