from django.shortcuts import render

# Create your views here.
def show_enrolled_event(request):
    return render(request, "enrolled_event.html")