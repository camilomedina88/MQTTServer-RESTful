from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import DataSource, Event, Variable, Widget, VarValue
from .serializers import DataSourceSerializer, VariableSerializer, VarValueSerializer


def index(request):
    datasource_list = DataSource.objects.order_by('-name')
    context = {'datasource_list': datasource_list}
    return render(request, 'iot_hub/index.html', context)

def web_datasource(request, uuid):
    datasource = DataSource.objects.get(source_id = uuid)
    context = {'datasource': datasource}
    return render(request, 'iot_hub/datasource.html', context)


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
        variables = Variable.objects.filter(data_source=datasource)
    except DataSource.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        #serializer = DataSourceSerializer(datasource)
        serializer = VariableSerializer(variables, many=True)
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

@csrf_exempt
def var_value_detail(request,uuid):
    try:
        variables = Variable.objects.get(var_id=uuid)
        varvalues = VarValue.objects.filter(variable = variables)
    except Variable.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = VarValueSerializer(varvalues, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = VarValueSerializer(data=data)
        if serializer.is_valid():
            serializer.save(variable = variables)
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

