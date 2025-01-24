from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
import os
from datetime import datetime

class ListFilesView(APIView):

    permission_classes = [IsAuthenticated]
    media_root = os.getenv("DJANGO_MEDIA_ROOT")

    def get(self, request):

        path = os.path.join(self.media_root, str(request.user.profile.uuid)) + "/"

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

    def get(self, request):
        # path = os.path.join(self.media_root, request.user.profile.uuid, request.query_params.get('path'))
        # return Response({"path": path})
        pass