from django.shortcuts import render

# Create your views here.
def show_list_event(request):
    return render(request, "list_event.html")