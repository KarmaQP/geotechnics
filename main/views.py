from django.shortcuts import render
from django.views import View


class StartingPageView(View):
  def get(self, request):
    return render(request, 'main/index.html')
