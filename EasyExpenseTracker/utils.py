from django.http import JsonResponse


def generate_json(sucess: bool, data={}):
    ret = dict(data)
    ret["sucess"] = sucess
    return JsonResponse(ret)
