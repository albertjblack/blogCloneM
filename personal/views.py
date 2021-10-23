from django.shortcuts import render
from account import models

# Create your views here.
def home_screen_view(request):
    list_of_values = []
    list_of_values.append(1)
    list_of_values.append(2)
    context = {
        'some_string':'This is some string',
        'list_of_values': list_of_values,
        'accounts': models.Account.objects.all()
    }
    return render(request,'personal/home.html', context=context)