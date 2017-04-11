# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.db import models
from django.utils import timezone
from django.utils import formats
from django.utils.six import python_2_unicode_compatible
from django.contrib.contenttypes.models import ContentType
from yamoney.signals import transaction_success


@python_2_unicode_compatible
class Transaction(models.Model):
    NOTIFICATION_TYPE_P2P = 'p2p-incoming'
    NOTIFICATION_TYPE_CARD = 'card-incoming'
    NOTIFICATION_TYPE_CHOICES = (
        (NOTIFICATION_TYPE_P2P, 'Перевод из кошелька'),
        (NOTIFICATION_TYPE_CARD, 'Перевод с карты'),
    )
    CURRENCY_RUB = '643'
    CURRENCY_CHOICES = (
        (CURRENCY_RUB, 'руб.'),
    )

    notification_type = models.CharField('Тип операции', max_length=100, choices=NOTIFICATION_TYPE_CHOICES)
    operation_id = models.CharField('Идентификатор операции', max_length=255)
    amount = models.DecimalField('Сумма, которая зачислена на счет получателя', max_digits=18, decimal_places=2)
    withdraw_amount = models.DecimalField('Сумма, которая списана со счета отправителя', max_digits=18,
                                          decimal_places=2, blank=True, null=True)
    currency = models.CharField('Валюта', max_length=100, choices=CURRENCY_CHOICES, default=CURRENCY_RUB)
    datetime = models.DateTimeField('Дата и время совершения перевода')
    sender = models.CharField('Номер счета отправителя', max_length=255, blank=True,
                              help_text='Только для переводов из кошелька')
    codepro = models.BooleanField('Служебное', default=False)
    label = models.CharField('Метка платежа', max_length=255, blank=True)
    test_notification = models.BooleanField('Тестовая операция', default=False)
    unaccepted = models.BooleanField('Перевод не зачислен', default=False,
                                     help_text='Получателю нужно освободить место в кошельке '
                                               'или использовать код протекции')
    lastname = models.CharField('Фамилия отправителя', max_length=255, blank=True)
    firstname = models.CharField('Имя отправителя', max_length=255, blank=True)
    fathersname = models.CharField('Отчество отправителя', max_length=255, blank=True)
    email = models.EmailField('Email отправителя', blank=True)
    phone = models.CharField('Телефон отправителя', max_length=50, blank=True)

    class Meta:
        verbose_name = 'Перевод'
        verbose_name_plural = 'Переводы'

    def __str__(self):
        return '%s на сумму %.2f %s от %s' % (
            self.get_notification_type_display(),
            self.withdraw_amount or 0,
            self.get_currency_display(),
            formats.date_format(timezone.localtime(self.datetime), 'DATETIME_FORMAT')
        )

    def get_related_obj(self):
        if self.label:
            label_parts = self.label.split('-')
            if len(label_parts) != 2:
                return None
            obj_type_str, obj_pk = label_parts
            if obj_type_str and obj_pk:
                label_parts = obj_type_str.split('.')
                if len(label_parts) != 2:
                    return None
                app_label, model_name = label_parts
                try:
                    obj_type = ContentType.objects.get_by_natural_key(app_label, model_name)
                except ContentType.DoesNotExist:
                    return None
                try:
                    obj_pk = int(obj_pk)
                except ValueError:
                    return None
                try:
                    obj = obj_type.get_object_for_this_type(pk=obj_pk)
                except obj_type.DoesNotExist:
                    return None
                else:
                    return obj
        return None

    def save(self, *args, **kwargs):
        created = self.pk is None
        super(Transaction, self).save(*args, **kwargs)
        if created:
            transaction_success.send(sender=self, related_obj=self.get_related_obj())

    @staticmethod
    def generate_label(obj):
        obj_type = ContentType.objects.get_for_model(obj)
        return '%s-%s' % ('.'.join(obj_type.natural_key()), obj.pk)
