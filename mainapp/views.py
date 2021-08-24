from django.db.models import query
from django.db.models.query_utils import RegisterLookupMixin
from django.shortcuts import render
from rest_framework.views import APIView
from mainapp.models import Music
from mainapp.serializers import MusicSerializer
from rest_framework import serializers, viewsets,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
# Create your views here.

class MusicViewSet(viewsets.ModelViewSet):
    queryset=Music.objects.all()
    serializer_class=MusicSerializer
    # permission_classes = (IsAuthenticated,) #授權，限制的授權的人操作的 API，要登入 (此法是針對整個class設定需要權限)

    def get_permissions(self):
        if self.action in ('create'):
            self.permission_classes=(IsAuthenticated,)
        return [permission() for permission in self.permission_classes]

    # [GET]/mainapp/api/{pk}/detail/
    @action(detail=True,methods=['get'],url_path='detail')
    def detail_action(self,request,pk=None):
        music=get_object_or_404(Music, pk=pk)
        result = {
            'singer': music.singer,
            'song': music.song
        }
        return Response(result, status=status.HTTP_200_OK)

    # [GET]/mainapp/api/all_singer
    @action(detail=False,methods=['get'],url_path='all_singer',permission_classes=(IsAuthenticated,))
    def all_singer(self, request):
        music = Music.objects.values_list('singer', flat=True).distinct()
        return Response(music, status=status.HTTP_200_OK)

class MusicViewSet2(APIView):
    serializer_class=MusicSerializer

    def get(self,request,format=None):
        music=Music.objects.all()
        serializer=MusicSerializer(music,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        serializer=self.serializer_class(data=request.data['data'])
        if serializer.is_valid():
            music_song=serializer.data['song']
            music_singer=serializer.data['singer']
            music=Music.objects.create(song=music_song,singer=music_singer)
            return Response({'Message': 'Success'},status=status.HTTP_200_OK)
        else:
            return Response({'Message': 'Invalid data...'},status=status.HTTP_400_BAD_REQUEST)

class MusicViewSet3(APIView):
    serializer_class=MusicSerializer

    def get(self,request,**kwargs):
        print(kwargs['id'])
        music=Music.objects.get(pk=kwargs['id'])
        # music=Music.objects.filter(pk=kwargs['id'])
        print(music)
        # music_get=self.serializer_class(music,many=True)
        music_get=MusicSerializer(music)
        print(music_get.data)
        return Response(music_get.data,status=status.HTTP_200_OK)

    def put(self,request,**kwargs):
        print(request.data)
        music_require=self.serializer_class(data=request.data['data'])
        data_id=kwargs['id']
        print(music_require.data) # 序列化出dict
        data_song=music_require.data['song']
        data_singer=music_require.data['singer']
        music=Music.objects.filter(id=data_id)[0]
        music.song=data_song
        music.singer=data_singer
        music.save()
        print(type(music))
        return Response(MusicSerializer(music).data,status=status.HTTP_200_OK)  #注意 .data 才會是dict https://www.cnblogs.com/ssgeek/p/13263810.html

    def delete(self,request,**kwargs):
        music_delete_id=kwargs['id']
        music_delete=Music.objects.filter(id=music_delete_id)
        if music_delete.exists()>0:
            music=music_delete[0]
            music.delete()
            return Response({'Message': 'Delete Success'},status=status.HTTP_200_OK)
        else:
            return Response({'Message': 'Invalid data...'},status=status.HTTP_400_BAD_REQUEST)




