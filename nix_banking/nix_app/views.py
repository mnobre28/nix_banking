from nix_app.models import User, Transfer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
import json


@api_view(["POST"])
def create_user(request):
    if request.method == 'POST':
        User(name=request.data.get('name'), cnpj=request.data.get('cnpj')).save()
        return Response(status=status.HTTP_201_CREATED)


@api_view(["PUT", "GET", "DELETE"])
def get_delete_update_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(json.dumps(user.as_dict()), status=status.HTTP_201_CREATED)

    elif request.method == 'PUT':
        user.name = request.data.get('name')
        user.cnpj = request.data.get('cnpj')
        user.save()
        return Response(status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def get_all_users(request):
    if request.method == 'GET':
        all_users = list(User.objects.values())
        return Response(json.dumps(all_users), status=status.HTTP_200_OK)


@api_view(["POST"])
def create_transfer(request):
    if request.method == 'POST':
        try:
            transfer = Transfer()
            transfer.get_data_from_dict(request.data)
            transfer.save()
            return Response(status=status.HTTP_201_CREATED)
        except (ObjectDoesNotExist, ValueError):
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT", "GET", "DELETE"])
def get_delete_update_transfer(request, transfer_id):
    try:
        transfer = Transfer.non_deleted_objects().get(id=transfer_id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(json.dumps(transfer.as_dict()), status=status.HTTP_201_CREATED)

    elif request.method == 'PUT':
        transfer.get_data_from_dict(request.data)
        transfer.save()
        return Response(status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        transfer.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def get_all_transfers(request):
    if request.method == 'GET':
        all_transfers_as_dict = []
        for transfer in Transfer.non_deleted_objects().all():
            all_transfers_as_dict.append(transfer.as_dict())
        return Response(json.dumps(all_transfers_as_dict), status=status.HTTP_200_OK)

@api_view(["GET"])
def filter_transfers(request, filter_type, filter):
    if request.method == 'GET':
        filtered_transfers_as_dict = []
        if filter_type == "date":
            filtered_transfers = Transfer.non_deleted_objects().filter(creation_date__contains=filter)
        elif filter_type == "payer":
            filtered_transfers = Transfer.non_deleted_objects().filter(payers_name=filter)
        elif filter_type == "receiver":
            filtered_transfers = Transfer.non_deleted_objects().filter(receivers_name=filter)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        for transfer in filtered_transfers:
            filtered_transfers_as_dict.append(transfer.as_dict())

        return Response(json.dumps(filtered_transfers_as_dict), status=status.HTTP_200_OK)

@api_view(["GET"])
def get_transfer_total(request):
    if request.method == 'GET':
        all_transfers = Transfer.non_deleted_objects().all()
        transfer_total = 0
        for transfer in all_transfers:
            transfer_total += transfer.transfer_value
        return Response(json.dumps({'transfer_total': transfer_total}), status=status.HTTP_200_OK)