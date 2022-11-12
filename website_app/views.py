from django.shortcuts import render
from django.views.generic import View
from scrapyd_api import ScrapydAPI
from django.http import HttpResponse


scrapyd = ScrapydAPI('http://localhost:6800')

# Create your views here.
class MainPageView(View):
    def get(self, request):
        task = scrapyd.schedule('default', 'eve_crawler')
        return HttpResponse(task)