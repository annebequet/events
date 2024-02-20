from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import User
from .serializers import ChangePasswordSerializer, ProfileSerializer, RegisterSerializer


class ProfileUserViewset(viewsets.ViewSet):
    def list(self, request):
        queryset = User.objects.all()
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ProfileSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=["put"])
    def change_password(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = ChangePasswordSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "password changed"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordApiView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ChangePasswordSerializer


class RegisterApiView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
