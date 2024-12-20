from django.urls import path

# Placeholder view
def home(request):
    from django.http import HttpResponse
    return HttpResponse("Chats App Home")

urlpatterns = [
    path('', home, name='chats-home'),
]
