from urllib import response
from django.http import HttpResponseRedirect


def redirect_index(request):
    return HttpResponseRedirect('../polls/')