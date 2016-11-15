from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import DataSource, Event, Variable, Widget
from .serializers import DataSourceSerializer, VariableSerializer

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def datasource_list(request):
    """
    List all DataSources, or create a new DataSources.
    """
    if request.method == 'GET':
        datasource = DataSource.objects.all()
        serializer = DataSourceSerializer(datasource, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DataSourceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def datasource_detail(request, uuid):
    """
    Retrieve, update or delete a code DataSource.
    """
    try:
        datasource = DataSource.objects.get(source_id=uuid)
    except DataSource.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DataSourceSerializer(datasource)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DataSourceSerializer(datasource, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        datasource.delete()
        return HttpResponse(status=204)