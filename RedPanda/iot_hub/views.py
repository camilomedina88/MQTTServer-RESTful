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
def bootstrap(request):
    datasource_list = DataSource.objects.order_by('-name')
    context = {'datasource_list': datasource_list}
    return render(request, 'iot_hub/bootstrap/pages/index.html',context)

def web_datasource(request, uuid):
    datasource = DataSource.objects.get(source_id = uuid)
    context = {'datasource': datasource}
    return render(request, 'iot_hub/datasource.html', context)
def web_variables(request, uuid):
    variable = Variable.objects.get(var_id = uuid)
    context = {'variable': variable}
    return render(request, 'iot_hub/variable.html', context)
def web_varWidget(request, uuid):
    variable = Variable.objects.get(var_id = uuid)
    context = {'variable': variable}
    return render(request, 'iot_hub/varWidget.html', context)

def web_trackingdemo(request):
    

    lat1 = Variable.objects.get(var_id= "3415aab6-6d2d-45e3-966a-58d49ab81b40")
    lng1 = Variable.objects.get(var_id= "5be2a39f-5de7-4d0b-ab19-8b0086f505c0")
    lat_list1 = VarValue.objects.filter(variable=lat1)
    lng_list1 = VarValue.objects.filter(variable=lng1)

    lat2 = Variable.objects.get(var_id= "39e22a89-0bdf-4e41-be6d-eff1495c4fe8")
    lng2 = Variable.objects.get(var_id= "3a02c8e8-1009-464c-922e-f7b1199b9cce")
    lat_list2 = VarValue.objects.filter(variable=lat2)
    lng_list2 = VarValue.objects.filter(variable=lng2)

    gps1 = []
    gps2 = []
    for value in lat_list1:
        try:
            longitude = lng_list1.get(timestamp=value.timestamp).value
            gps1.append({'timestamp':value.timestamp,'lat':value.value, 'lng':longitude})
        except:
            pass

    for value in lat_list2:
        try:
            longitude = lng_list2.get(timestamp=value.timestamp).value
            gps2.append({'timestamp':value.timestamp,'lat':value.value, 'lng':longitude})
        except:
            pass


    context = {'gps1': gps1, 'gps2': gps2}
    return render(request, 'iot_hub/tracking_demo.html', context)

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

