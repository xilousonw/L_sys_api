from django.shortcuts import render

# Create your views here.



from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins
from . import models
from . import serializers

class BannerViewSet(ModelViewSet,mixins.ListModelMixin):
    queryset = models.Banner.objects.filter(is_delete=False, is_show=True).all()
    serializer_class = serializers.BannerSerializer
