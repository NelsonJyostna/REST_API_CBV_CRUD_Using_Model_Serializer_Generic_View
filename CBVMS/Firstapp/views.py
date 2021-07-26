from django.shortcuts import render
from django.views.generic import View
from .models import Student
import io
from rest_framework.parsers import JSONParser
from .serializers import StudentSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class StudentCBV(View):
    def get(self, request, *args, **kwargs):
        json_data=request.body
        print("GET Json_Data", json_data)
        stream=io.BytesIO(json_data)
        print("GET Stream", stream)
        data=JSONParser().parse(stream)
        print("GET Data",data)
        id=data.get('id', None)
        print(id)
        if id is not None:
            stud= Student.objects.get(id=id)
            print("GET stud", stud)
            serializer= StudentSerializer(stud)
            print("GET Serializer", serializer)
            json_data=JSONRenderer().render(serializer.data)
            print("GET if id is not none vala json_data", json_data)
            return HttpResponse(json_data, content_type='application/json')
        else:
            studs=Student.objects.all()
            print("GET else studs", studs)
            serializer=StudentSerializer(studs, many=True)
            print("GET else serializer",serializer)
            json_data=JSONRenderer().render(serializer.data)
            print("GET else JsonRenderer", json_data)
            return HttpResponse(json_data, content_type='application/json')    
     
    def post(self, request, *args, **kwargs):
        json_data=request.body
        stream=io.BytesIO(json_data)
        data=JSONParser().parse(stream)
        serializer=StudentSerializer(data=data)
        print("POST serializer", serializer)
        if serializer.is_valid():
            serializer.save()
            msg={'msg':'Student Added Succesfully'}
            json_data=JSONRenderer().render(msg)
            print("POST JSON RENderer if part", json_data)
            return HttpResponse(json_data, content_type='application/json')
        else:
            json_data=JSONRenderer().render(serializer.errors)
            print("POST Json Renderer else part", json_data)
            return HttpResponse(json_data, content_type='application/json')

    def put(self, request, *args, **kwargs):
        json_data=request.body
        stream=io.BytesIO(json_data)
        data=JSONParser().parse(stream)
        id=data.get('id')
        stu=Student.objects.get(id=id)
        serializer=StudentSerializer(stu, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            msg={'msg': 'partially updated sucessfully'}
            json_data=JSONRenderer().render(msg)
            return HttpResponse(json_data, content_type='application/json')
        else:
            json_data=JSONRenderer().render(serializer.errors)
            return HttpResponse(json_data, content_type='application/json')

    def delete(self, request, *args, **kwargs):
        json_data=request.body
        stream=io.BytesIO(json_data)
        data=JSONParser().parse(stream)
        id=data.get('id', None)
        if id is not None:
            stu=Student.objects.get(id=id)
            stu.delete()
            msg={'msg':"Deleted student Successfully"}
            json_data=JSONRenderer().render(msg)
            return HttpResponse(json_data, content_type='application/json')
        else:
            msg={'msg': "Plz provide the id"}
            json_data=JSONRenderer().render(msg)
            return HttpResponse(json_data, content_type='application/json')