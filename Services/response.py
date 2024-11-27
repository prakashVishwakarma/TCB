
from django.http import HttpResponse, JsonResponse

from Logger.myLogger import Logger

logger = Logger("response")

def api_response(status, message, data):
    try:
        HttpResponse.status_code = status
        return JsonResponse({"status": status, "message": str(message), "data": data})
    except Exception as e:
        logger.error(str(e))
        HttpResponse.status_code = 500
        print("Exception ")
        print(type(e))
        return JsonResponse({"status": 500, "message": str(e), "data": {}})
