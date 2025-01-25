from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
import os
from datetime import datetime
from rest_framework.exceptions import NotFound

class ListFilesView(APIView):

    permission_classes = [IsAuthenticated]
    _media_root = os.getenv("DJANGO_MEDIA_ROOT")

    def get(self, request):

        path = os.path.join(self._media_root, str(request.user.profile.uuid)) + "/"

        to_return = {}
        to_return["files"] = []

        for root, dirs, files in os.walk(path):
            for file in files:

                to_return["files"].append({"name": file,
                                            "folder": root.replace(path, "/", 1),
                                            "created": datetime.fromtimestamp(os.path.getctime(os.path.join(root, file))).isoformat(),
                                            "modified": datetime.fromtimestamp(os.path.getmtime(os.path.join(root, file))).isoformat(),
                                            "size": os.path.getsize(os.path.join(root, file))})

        indexes = [ i for i in range(len(to_return["files"]), 0, -1) ]

        for file in to_return["files"]:
            file["id"] = indexes.pop()

        return Response(to_return)


class RetrieveFileView(APIView):

    permission_classes = [IsAuthenticated]
    _media_root = os.getenv("DJANGO_MEDIA_ROOT")

    def get(self, request):
        filepath = os.path.join(self._media_root, str(request.user.profile.uuid), request.query_params.get('filepath'))
        try: response = FileResponse(open(filepath, "rb"), content_type = 'text/plain')
        except: return NotFound(detail = f'File {filepath} not found i user\'s directory')
        response['Content-Disposition'] = f'attachement; filename={filepath.split("/")[-1]}'
        return response
        