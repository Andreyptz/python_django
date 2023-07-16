import time

from django.http import HttpRequest
from django.shortcuts import render


def setup_useragent_on_request_middleware(get_response):

    print('initial call')
    def middleware(request: HttpRequest):
        print('before get response')
        request.user_agent = request.META['HTTP_USER_AGENT']
        response = get_response(request)
        print('after get response')
        return response

    return middleware

class CountRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_and_time = {}
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        min_pause = 20
        self.requests_count += 1
        print("requests count", self.requests_count)
        # ip = request.META.get('REMOTE_ADDR')
        # if ip in self.ip_and_time:
        #     print(time.time() - self.ip_and_time[ip])
        #     if time.time() - self.ip_and_time[ip] < min_pause:
        #         print("Повторный запрос возможен только через 20 секунд")
        #         self.ip_and_time[ip] = time.time()
        #         return render(request, 'requestdataapp/pause.html')
        #     else:
        #         self.ip_and_time[ip] = time.time()
        # else:
        #     self.ip_and_time[ip] = time.time()
        response = self.get_response(request)
        self.responses_count += 1
        print("responses count", self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print("got", self.exceptions_count, "exception so far")