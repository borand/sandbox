# native libraries
import time
import datetime

# django libraries
from django.http import Http404
from django.contrib.auth.models import User
from django.http import HttpResponse
from . import models
from data_utils import data_value_submission
import logging
logger = logging.getLogger(__name__)

# rest_framework libraries

#######################################################################################
# API - usign django-rest-framework
#

#######################################################################################
# API
#

def api_submit_datavalue(request, datestamp, sn, val):
    msg = "[SUBMITTED] datestamp: %s, sn: %s, val: %s" % (datestamp, sn, val)
    logger.info(msg)
    try:
        results = data_value_submission(datestamp, sn, val, request.META.get('REMOTE_ADDR'))
    except Exception as E:                
        results = 'Exception:' + E.message
    return HttpResponse(results)

#######################################################################################
# API - usign django-rest-framework - PART 1
#
# # Only needed for the first part of the tutorial
# class JSONResponse(HttpResponse):
#     """
#     An HttpResponse that renders it's content into JSON.
#     """
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)

#######################################################################################
# API - usign django-rest-framework - PART 2
#
# @api_view(['GET', 'POST'])
# #@csrf_exempt
# def units_list(request, format=None):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         snippets = models.Units.objects.all()
#         serializer = UnitsSerializer(snippets, many=True)
#         return Response(serializer.data)
#         #return JSONResponse(serializer.data)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = UnitsSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             #return JSONResponse(serializer.data, status=201)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             #return JSONResponse(serializer.errors, status=400)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# # @csrf_exempt
# def units_detail(request, pk, format=None):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         snippet = models.Units.objects.get(pk=pk)
#     except models.Units.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#         # return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = UnitsSerializer(snippet)
#         return Response(serializer.data)
#         # return JSONResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = UnitsSerializer(snippet, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#             # return JSONResponse(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             # return JSONResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         snippet.delete()
#         # return HttpResponse(status=204)
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class UnitstList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     """
#     List all snippets, or create a new snippet.
#     """

#     queryset = models.Units.objects.all()
#     serializer_class = UnitsSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

#     # Before adding mixins
#     # def get(self, request, format=None):
#     #     snippets = models.Units.objects.all()
#     #     serializer = UnitsSerializer(snippets, many=True)
#     #     return Response(serializer.data)

#     # def post(self, request, format=None):
#     #     serializer = UnitsSerializer(data=data)
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UnitsDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
    
#     queryset = models.Units.objects.all()
#     serializer_class = UnitsSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

#     ## Pre mixins
#     # def get_object(self, pk):
#     #     try:
#     #         return models.Units.objects.get(pk=pk)
#     #     except models.Units.DoesNotExist:
#     #         raise Http404

#     # def get(self, request, pk, format=None):
#     #     snippet = self.get_object(pk)
#     #     serializer = UnitsSerializer(snippet)
#     #     return Response(serializer.data)

#     # def put(self, request, pk, format=None):
#     #     snippet = self.get_object(pk)
#     #     serializer = UnitsSerializer(snippet, data=request.DATA)
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return Response(serializer.data)
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # def delete(self, request, pk, format=None):
#     #     snippet = self.get_object(pk)
#     #     snippet.delete()
#     #     return Response(status=status.HTTP_204_NO_CONTENT)
