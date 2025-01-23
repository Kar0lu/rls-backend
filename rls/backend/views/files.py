from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
import os

class ListFilesView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        path = os.path.join(os.getenv("DJANGO_MEDIA_ROOT"), str(request.user.pk))

        to_return = {}
        for root, dirs, files in os.walk(path):

            if root not in to_return.keys():
                to_return[root] = []

            for file in files:
                to_return[root].append({"filename": file, "size": os.path.getsize(os.path.join(root, file))})

        return Response(to_return)


class RetrieveFileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        pass