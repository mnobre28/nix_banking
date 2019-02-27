from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
import json
from nix_app.models import User, Transfer
import datetime

client = Client()


class CreateUserTest(TestCase):
    def setUp(self):
        self.new_user = {"name": "A test user",
                         "cnpj": "1234567890"}

    def test_create_new_user(self):
        response = client.post(reverse('create_user'),
                               data=json.dumps(self.new_user),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        saved_user = User.objects.first()
        self.assertEqual(saved_user.id, 1)


class GetUpdateDeleteUserTest(TestCase):
    def setUp(self):
        self.user = User(name="New username", cnpj="1234567890")

    def get_user(self):
        response = client.get(reverse('get_delete_update_user', kwargs={'user_id': self.user.id}),
                              content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_user(self):
        new_user_data = {"name": "Updated username",
                         "cnpj": "0987654321"}
        response = client.put(reverse('get_delete_update_user',
                              kwargs={'user_id': 1}),
                              data=json.dumps(new_user_data),
                              content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_user = User.objects.get(id=1)
        self.assertEquals(updated_user.name, new_user_data["name"])
        self.assertEquals(updated_user.cnpj, new_user_data["cnpj"])

    def test_delete_user(self):
        response = client.delete(reverse('get_delete_update_user',
                                 kwargs={'user_id': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        all_users = User.objects.all()
        self.assertEqual(len(all_users), 0)


class GetAllUsersTest(TestCase):
    def setUp(self):
        User(name="User A", cnpj="123").save()
        User(name="User B", cnpj="345").save()
        User(name="User C", cnpj="678").save()

    def test_can_get_all_users(self):
        response = client.get(reverse('get_all_users'))
        expected_response = [{"id": 1, "name": "User A", "cnpj": "123"},
                             {"id": 2, "name": "User B", "cnpj": "345"},
                             {"id": 3, "name": "User C", "cnpj": "678"}]
        self.assertEqual(json.loads(response.data), expected_response)


class CanCreateTransferTest(TestCase):
    def setUp(self):
        self.test_user = User()
        self.test_user.save()
        self.doc_transfer = Transfer(transfer_value=1000, user_id=self.test_user, receivers_bank="Test Bank")
        self.cc_transfer = Transfer(receivers_bank="Test Bank", payers_bank="Test Bank", user_id=self.test_user)
        self.ted_transfer = Transfer(transfer_value=4000, user_id=self.test_user, receivers_bank="Test Bank",
                                     creation_date=datetime.datetime(2019, 1, 1, 12))
        self.transfer_with_invalid_value = Transfer(transfer_value=Transfer.MAX_TRANSFER_VALUE + 1,
                                                    user_id=self.test_user, receivers_bank="Test Bank")
        self.transfer_with_invalid_user = Transfer()

    def test_can_set_doc_transfer_type(self):
        response = client.post(reverse('create_transfer'),
                               data=json.dumps(self.doc_transfer.as_dict()),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        saved_doc_transfer = Transfer.non_deleted_objects().first()
        self.assertEqual(saved_doc_transfer.transfer_type, Transfer.TRANSFER_TYPE_OPTIONS.DOC)

    def test_can_set_cc_transfer_type(self):
        response = client.post(reverse('create_transfer'),
                               data=json.dumps(self.cc_transfer.as_dict()),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        saved_cc_transfer = Transfer.non_deleted_objects().first()
        self.assertEqual(saved_cc_transfer.transfer_type, Transfer.TRANSFER_TYPE_OPTIONS.CC)

    def test_can_set_ted_transfer_type(self):
        response = client.post(reverse('create_transfer'),
                               data=json.dumps(self.ted_transfer.as_dict()),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        saved_ted_transfer = Transfer.non_deleted_objects().first()
        self.assertEqual(saved_ted_transfer.transfer_type, Transfer.TRANSFER_TYPE_OPTIONS.TED)

    def test_cant_create_transfer_that_exceeds_value_limit(self):
        response = client.post(reverse('create_transfer'),
                               data=json.dumps(self.transfer_with_invalid_value.as_dict()),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cant_create_transfer_without_user(self):
        response = client.post(reverse('create_transfer'),
                               data=json.dumps(self.transfer_with_invalid_user.as_dict()),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetUpdateDeleteTransferTest(TestCase):
    def setUp(self):
        user = User(name="New username", cnpj="1234567890")
        user.save()
        self.transfer = Transfer(user_id=user)
        self.transfer.save()

    def get_user(self):
        response = client.get(reverse('get_delete_update_transfer', kwargs={'transfer_id': self.transfer.id}),
                              content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_transfer(self):
        new_transfer_data = {"payers_name": "new payers name",
                             "receivers_name": "new receivers name"}
        response = client.put(reverse('get_delete_update_transfer',
                              kwargs={'transfer_id': 1}),
                              data=json.dumps(new_transfer_data),
                              content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_transfer = Transfer.objects.get(id=1)
        self.assertEquals(updated_transfer.payers_name, new_transfer_data["payers_name"])
        self.assertEquals(updated_transfer.receivers_name, new_transfer_data["receivers_name"])

    def test_delete_transfer(self):
        response = client.delete(reverse('get_delete_update_transfer',
                                 kwargs={'transfer_id': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        all_transfers = Transfer.non_deleted_objects().all()
        self.assertEqual(len(all_transfers), 0)


class GetAllTransfersTest(TestCase):
    def setUp(self):
        self.user = User(name="User A", cnpj="123").save()
        Transfer(user_id=self.user).save()
        Transfer(user_id=self.user).save()

    def test_can_get_all_users(self):
        response = client.get(reverse('get_all_transfers'))
        expected_response = [{'id': 1, 'user_id': None, 'payers_name': '', 'payers_bank': '', 'payers_agency': '',
                              'payers_account': '', 'receivers_name': '', 'receivers_bank': '', 'receivers_agency': '',
                              'receivers_account': '', 'transfer_value': 1, 'transfer_type': 'CC',
                              'creation_date': '2019-02-27'},
                             {'id': 2, 'user_id': None, 'payers_name': '', 'payers_bank': '', 'payers_agency': '',
                              'payers_account': '', 'receivers_name': '', 'receivers_bank': '', 'receivers_agency': '',
                              'receivers_account': '', 'transfer_value': 1, 'transfer_type': 'CC',
                              'creation_date': '2019-02-27'}]
        self.assertEqual(json.loads(response.data), expected_response)


class FilterTransfersTest(TestCase):
    def setUp(self):
        self.user = User()
        self.user.save()
        self.date_filter = datetime.date(2019, 1, 1)
        self.payers_name_filter = "Payer to find"
        self.receiver_name_filter = "Receiver to find"
        self.transfer_to_filter_by_date = Transfer(user_id=self.user, creation_date=self.date_filter)
        self.transfer_to_filter_by_date.save()
        self.transfer_filter_by_payer = Transfer(user_id=self.user, payers_name=self.payers_name_filter)
        self.transfer_filter_by_payer.save()
        self.transfer_filter_by_receiver = Transfer(user_id=self.user, receivers_name=self.receiver_name_filter)
        self.transfer_filter_by_receiver.save()

    def test_can_filter_by_date(self):
        response = client.get(reverse('filter_transfers', kwargs={'filter_type': "date",
                                                                  'filter': self.date_filter}),
                              content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.data)), 1)

    def test_can_filter_by_payers_name(self):
        response = client.get(reverse('filter_transfers', kwargs={'filter_type': "payer",
                                                                  'filter': self.payers_name_filter}),
                              content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.data)), 1)

    def test_can_filter_by_receivers_name(self):
        response = client.get(reverse('filter_transfers', kwargs={'filter_type': "receiver",
                                                                  'filter': self.receiver_name_filter}),
                              content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.data)), 1)


class GetSumOfAllTransfersTest(TestCase):
    def setUp(self):
        test_user = User()
        test_user.save()
        self.transfer_one_hundred = Transfer(user_id=test_user, transfer_value=100)
        self.transfer_one_hundred.save()
        self.transfer_two_hundred = Transfer(user_id=test_user, transfer_value=200)
        self.transfer_two_hundred.save()
        self.transfer_seven_hundred = Transfer(user_id=test_user, transfer_value=700)
        self.transfer_seven_hundred.save()

    def test_can_sum_all_transfer_values(self):
        expected_total = 1000
        response = client.get(reverse('get_transfer_total'), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.data), {'transfer_total': expected_total})