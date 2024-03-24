from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from elasticsearch_dsl import Q
from django.contrib.auth import authenticate

from api.models import *
from api.serializers import *
from api.documents import EntryDocumet
from api.utils import generate_access_token, generate_refresh_token, jwt_decode
from api.authentication import CustomJwtAuthentication


class Index(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response(status=status.HTTP_200_OK, data={"msg": "Server çalışıyor..."})


class Login(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        user = authenticate(username=username, password=password)
        if user:
            res = {
                "access_token": generate_access_token(id=user.id),
                "refresh_token": generate_refresh_token(id=user.id),
            }
            return Response(data=res, status=status.HTTP_200_OK)
        return Response(
            data={"msg": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )


class RefreshToken(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refres_token = request.data.get("refresh_token", None)
        msg = {"msg": ""}
        if refres_token:
            try:
                data = jwt_decode(token=refres_token)
                res = {
                    "access_token": generate_access_token(id=data["user_id"]),
                    "refresh_token": generate_refresh_token(id=data["user_id"]),
                }
                return Response(data=res, status=status.HTTP_200_OK)
            except Exception:
                msg["msg"] = "Sent token has expired"
        else:
            msg["msg"] = "Refresh token information was not provided"
        return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)


class CreateEntry(APIView):
    authentication_classes = [CustomJwtAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateEntrySerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={"msg": "Your data has been successfully saved."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteEntry(APIView):
    authentication_classes = [CustomJwtAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            data = Entry.objects.filter(user=request.user, id=pk)
            if data.count() > 0:
                data.delete()
                return Response(
                    data={"msg": "The deletion was successful."},
                    status=status.HTTP_200_OK,
                )
            else:
                raise
        except Exception as e:
            return Response(
                data={"msg": "Entry not found!"}, status=status.HTTP_400_BAD_REQUEST
            )


class SearchEntry(APIView):
    authentication_classes = [CustomJwtAuthentication]
    permission_classes = [IsAuthenticated]

    def seach_data(self, user=None, query_params=None):
        q = EntryDocumet.search()
        if user and user.username:
            user_q = Q("match", user__username=user.username)
            if query_params:
                q = q.query(user_q & query_params)
            else:
                q = q.query(user_q)
        elif query_params:
            q = q.query(query_params)
        return q.execute()

    def create_query(self, query_dict):
        if query_dict:
            q_list = [
                (
                    Q("term", **{key: value})
                    if "*" not in value
                    else Q("wildcard", **{key: value})
                )
                for key, value in query_dict.items()
            ]
            combined_q = q_list[0]
            for q in q_list[1:]:
                combined_q |= q
            return combined_q
        return None

    def create_query_object(self, search_data):
        res = {}
        if search_data:
            search_data_list = str(search_data).split(",")
            for search_param in search_data_list:
                key, val = search_param.split("=")
                if key.strip() != "user__username":
                    res[key.strip()] = val.strip()
        return res

    def post(self, request):
        search_data = request.data.get("query", None)
        query_dict = self.create_query_object(search_data=search_data)
        res_datas = self.seach_data(
            query_params=self.create_query(query_dict), user=request.user
        )
        res = {"onyl_datas": [], "elasticsearch_datas": res_datas.to_dict()}
        for hit in res_datas:
            res["onyl_datas"].append(
                {
                    "subject": hit.subject,
                    "username": hit.user.username,
                    "message": hit.message,
                }
            )
        return Response(data=res, status=status.HTTP_200_OK)
