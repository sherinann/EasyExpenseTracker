from django.http import JsonResponse
from django.shortcuts import render

from EasyExpenseTracker.authentication import token_required


@token_required
def get_budget(request):
    if 'token' not in request.POST:
        return JsonResponse({"status":"Fail"})
    return JsonResponse({'status': "OK"})
