from django.shortcuts import render
from rest_framework import generics, status
from blog.serializers import PostSerializer
from .models import Post
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import Paginator

import math

def build_response(raw, *args, **kwargs):
    response = Response(raw, *args, **kwargs)
    response['Access-Control-Allow-Origin'] = '*'
    return response
# Create your views here.

class RoomView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class GetPosts(APIView):

    serializer_class = PostSerializer

    def get(self, request, format=None):
        
        data = Post.objects.all()

        if len(data) > 0:
            posts = PostSerializer(data, many=True).data
            return build_response(posts, status=status.HTTP_200_OK)
            
        return Response({'No data': 'Invalid requests'}, status=status.HTTP_404_NOT_FOUND)


class GetPaginatedPosts(APIView):

    serializer_class = PostSerializer
    lookup_url_kwarg = 'page_num'
    posts_num = 5

    def get(self, request, format=None):
        
        data = Post.objects.all().order_by('-publish')
        page_num = int(request.GET.get(self.lookup_url_kwarg))
        if len(data) > 0:
            index = math.ceil(len(data) / self.posts_num)
            paginated_data = [data[i*self.posts_num: (i*self.posts_num) +self.posts_num] for i in range(index)]            
            posts = PostSerializer(paginated_data[page_num], many=True).data
            return build_response(posts, status=status.HTTP_200_OK)
            
        return Response({'No data': 'Invalid requests'}, status=status.HTTP_404_NOT_FOUND)


class GetPost(APIView):
    serializer_class = PostSerializer
    lookup_url_kwarg = 'code'

    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            room = Post.objects.filter(code=code)
            if len(room) > 0:
                data = PostSerializer(room[0]).data
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Room Not Found': 'Invalid Room Code.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'Bad Request': 'Code paramater not found in request'}, status=status.HTTP_400_BAD_REQUEST)

