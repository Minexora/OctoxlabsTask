from rest_framework.test import APITestCase
from rest_framework import status
from api.serializers import *
from api.documents import *
from api.models import User, Entry


class EntryModelTests(APITestCase):
    def init_data(self):
        try:
            # User varsa al yoksa oluştur
            user = User.objects.filter(username="octoAdmin")
            if user.count() == 0:
                user = User.objects.create_superuser("octoAdmin", "octoAdmin@octoxlabs.com.tr", "159951", first_name="octoAdmin")
            else:
                user = user.first()
            self.init_user = user

            # Entry oluşturma
            self.init_entries = []
            init_entries_json = [
                {
                    "user": self.init_user,
                    "subject": "UnitTest1",
                    "message": "UnitTest1",
                },
                {
                    "user": self.init_user,
                    "subject": "UnitTest2",
                    "message": "UnitTest2",
                },
                {
                    "user": self.init_user,
                    "subject": "UnitTest3",
                    "message": "UnitTest3",
                },
                {
                    "user": self.init_user,
                    "subject": "UnitTest4",
                    "message": "UnitTest4",
                },
            ]

            for entry_json in init_entries_json:

                class request:
                    user = self.init_user
                    data = entry_json

                serializer = CreateEntrySerializer(data=request.data, context={"request": request})
                if serializer.is_valid():
                    self.init_entries.append(serializer.save())

        except Exception as e:
            print(str(e))

    def login(self):
        payload = {"username": "octoAdmin", "password": "159951"}
        return self.client.post("/api/login", data=payload, format="json")

    def get_tokens(self, res):
        if res.status_code == status.HTTP_200_OK:
            self.access_token = res.data.get("access_token", None)
            self.refresh_token = res.data.get("refresh_token", None)

    def set_token_to_header(self, token_type):
        self.client.credentials(HTTP_AUTHORIZATION=f"{token_type} {self.access_token}")

    def setUp(self) -> None:
        # Her test çalışmadan önce buradaki kodlar çalışır
        self.init_data()
        res = self.login()
        self.get_tokens(res)

    def test_login(self):
        res = self.login()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", res.data)

    def test_refresh_token(self):
        payload = {"refresh_token": self.refresh_token}
        res = self.client.post("/api/refresh-token", data=payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", res.data)
        self.get_tokens(res)

    def test_wrong_token_type(self):
        payload = {"query": "subject = deneme*"}
        self.set_token_to_header(token_type="Bearer")
        res = self.client.post("/api/search", data=payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_search(self):
        payload = {"query": "subject = unittest*"}
        self.set_token_to_header(token_type="octoxlabs")
        res = self.client.post("/api/search", data=payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        init_entries_count = len(self.init_entries)
        res_entries_count = len(res.data.get("onyl_datas", []))
        self.assertGreaterEqual(
            res_entries_count,
            init_entries_count,
        )
        db_entries_count = Entry.objects.filter(user=self.init_user).count()
        self.assertEqual(init_entries_count, db_entries_count)

    def test_create_entry(self):
        start_entries_count = Entry.objects.filter(user=self.init_user).count()
        payload = {"subject": "Deneme1", "message": "Yapılan test Deneme1"}
        self.set_token_to_header(token_type="octoxlabs")
        res = self.client.post("/api/create-entry", data=payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        end_entries_count = Entry.objects.filter(user=self.init_user).count()
        self.assertGreater(end_entries_count, start_entries_count)

    def test_delete_entry(self):
        start_entries_count = Entry.objects.filter(user=self.init_user).count()
        self.set_token_to_header(token_type="octoxlabs")
        last_add_init_entry = self.init_entries[-1]
        res = self.client.delete(f"/api/delete-entry/{last_add_init_entry.id}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        end_entries_count = Entry.objects.filter(user=self.init_user).count()
        self.assertGreater(start_entries_count, end_entries_count)
