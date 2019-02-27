from django.db import models
from model_utils import Choices
import datetime
from django.core.exceptions import ObjectDoesNotExist


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(default="", max_length=128, verbose_name="Nome")
    cnpj = models.CharField(default="", max_length=14, verbose_name="CNPJ")
    objects = models.Manager()

    def __str__(self):
        return u"Usuário {}".format(self.name)

    def as_dict(self):
        return {'name': self.name, 'cnpj': self.cnpj}


class Transfer(models.Model):
    TRANSFER_TYPE_OPTIONS = Choices('CC', 'TED', 'DOC')
    MAX_TRANSFER_VALUE = 100000
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, related_name='transfers', verbose_name="Transferências",
                                on_delete=models.CASCADE, null=True)
    payers_name = models.CharField(default="", max_length=128, verbose_name="Nome do pagador")
    payers_bank = models.CharField(default="", max_length=128, verbose_name="Banco do pagador")
    payers_agency = models.CharField(default="", max_length=128, verbose_name="Agência do pagador")
    payers_account = models.CharField(default="", max_length=128, verbose_name="Conta do pagador")
    receivers_name = models.CharField(default="", max_length=128, verbose_name="Nome do recebedor")
    receivers_bank = models.CharField(default="", max_length=128, verbose_name="Banco do recebedor")
    receivers_agency = models.CharField(default="", max_length=128, verbose_name="Agência do recebedor")
    receivers_account = models.CharField(default="", max_length=128, verbose_name="Conta do recebedor")
    transfer_value = models.PositiveIntegerField(default=1, verbose_name="Valor da Transferência")
    transfer_type = models.CharField(choices=TRANSFER_TYPE_OPTIONS, default=TRANSFER_TYPE_OPTIONS.DOC,
                                     verbose_name="Tipo da transferência", max_length=3)
    creation_date = models.DateField(verbose_name="Data de criação")
    is_deleted = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return u"Transferência {}".format(self.id)

    def save(self, *args, **kwargs):
        if self.transfer_value > self.MAX_TRANSFER_VALUE:
            raise ValueError("Transfer value cannot exceed R$ {}".format(self.MAX_TRANSFER_VALUE))
        if self.creation_date is None:
            self.creation_date = datetime.datetime.now()
        self._set_transfer_type()
        super(Transfer, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_deleted = True

    def hard_delete(self):
        super(Transfer, self).delete()

    @staticmethod
    def non_deleted_objects():
        return Transfer.objects.filter(is_deleted=False)

    def as_dict(self):
        transfer_dict = {"id": self.id,
                         "user_id": self.user_id.id if self.user_id else None,
                         "payers_name": self.payers_name,
                         "payers_bank": self.payers_bank,
                         "payers_agency": self.payers_agency,
                         "payers_account": self.payers_account,
                         "receivers_name": self.receivers_name,
                         "receivers_bank": self.receivers_bank,
                         "receivers_agency": self.receivers_agency,
                         "receivers_account": self.receivers_account,
                         "transfer_value": self.transfer_value,
                         "transfer_type": self.transfer_type,
                         "creation_date": self.creation_date.isoformat() if self.creation_date else None}
        return transfer_dict

    def get_data_from_dict(self, transfer_data):
        try:
            self.user_id = User.objects.get(id=transfer_data["user_id"])
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("User with id {} does not exist.".format(transfer_data["user_id"]))
        self.payers_name = transfer_data["payers_name"]
        self.payers_bank = transfer_data["payers_bank"]
        self.payers_agency = transfer_data["payers_agency"]
        self.receivers_name = transfer_data["receivers_name"]
        self.receivers_bank = transfer_data["receivers_bank"]
        self.receivers_agency = transfer_data["receivers_agency"]
        self.receivers_account = transfer_data["receivers_account"]
        self.transfer_value = transfer_data["transfer_value"]
        self.transfer_type = transfer_data["transfer_type"]
        if transfer_data["creation_date"]:
            if isinstance(transfer_data["creation_date"], str):
                transfer_data["creation_date"] = datetime.datetime. \
                    strptime(transfer_data["creation_date"], "%Y-%m-%dT%H:%M:%S")
            self.creation_date = transfer_data["creation_date"]

    def _set_transfer_type(self):
        if self.receivers_bank == self.payers_bank:
            self.transfer_type = self.TRANSFER_TYPE_OPTIONS.CC
        elif self.transfer_value < 5000 and 10 < self.creation_date.hour < 16:
            self.transfer_type = self.TRANSFER_TYPE_OPTIONS.TED
        else:
            self.transfer_type = self.TRANSFER_TYPE_OPTIONS.DOC
