from rest_framework.test import APITestCase
from django.urls import reverse


class NotesSmokeTests(APITestCase):
    def test_notes_crud_smoke(self):
        # List initially empty
        url_list = reverse('notes-list-create')
        resp = self.client.get(url_list)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, [])

        # Create without title -> 400
        resp = self.client.post(url_list, data={"description": "x"}, format='json')
        self.assertEqual(resp.status_code, 400)

        # Create with title -> 201
        resp = self.client.post(url_list, data={"title": "Task 1", "description": "desc"}, format='json')
        self.assertEqual(resp.status_code, 201)
        note_id = resp.data["id"]

        # Retrieve -> 200
        url_detail = reverse('notes-detail', kwargs={"id": note_id})
        resp = self.client.get(url_detail)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["title"], "Task 1")

        # Patch -> 200
        resp = self.client.patch(url_detail, data={"is_completed": True}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data["is_completed"])

        # Delete -> 204
        resp = self.client.delete(url_detail)
        self.assertEqual(resp.status_code, 204)
