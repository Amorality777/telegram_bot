# Create your models here.

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from amo.models import Technique, City, OrderBot, District


class TGConfigManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(id=0)


class TGUserManager(models.Manager):
    def get_queryset(self, amo_id=None):
        if amo_id:
            return super().get_queryset().filter(amo_id=amo_id)
        return super().get_queryset()


class TGConfig(models.Model):
    id = models.IntegerField(primary_key=True)
    token = models.CharField(max_length=250)
    config = TGConfigManager()

    class Meta:
        verbose_name = 'Настройка ТГ'
        verbose_name_plural = 'Настройка ТГ'

    def __str__(self):
        return '****'


class TGLogist(models.Model):
    name = models.CharField(max_length=250, verbose_name='имя логиста', blank=True, null=True, default='****')
    tg_id = models.IntegerField(verbose_name='телеграмм id логиста', blank=True, null=True)

    class Meta:
        verbose_name = 'ТГ Логиста'
        verbose_name_plural = 'ТГ Логиста'

    def __str__(self):
        return self.name


class TGUserAmo(models.Model):
    STATUS_BLOCK = (
        ('diagnostics', 'Диагностика'),
        ('amount_repair', 'Сумма ремонта'),
        ('amount_consumables', 'Сумма расходников'),
        ('consumables', 'Расходники'),
    )
    amo_id = models.IntegerField(verbose_name='амо id мастера', blank=True, null=True)
    amo_leads_id = models.IntegerField(verbose_name='амо id сделки', blank=True, null=True)
    tg_id = models.IntegerField(verbose_name='телеграмм id мастера', blank=True, null=True)
    name = models.CharField(max_length=250, verbose_name='имя мастера', blank=True, null=True, default='****')
    phone = models.CharField(max_length=250, verbose_name='телефон', blank=True, null=True)
    rating = models.IntegerField(verbose_name='рейтинг мастера', default=0)
    sum_orderbot = models.IntegerField(verbose_name='Кол-во зак в день', default=7)
    technique = models.ManyToManyField(Technique, related_name='tg_user', blank=True)
    city = models.ManyToManyField(City, related_name='tg_user', blank=True)
    district = models.ManyToManyField(District, verbose_name='район', related_name='tg_user',
                                      blank=True)
    active_orderbot = models.ForeignKey(OrderBot, verbose_name='активный заказ общения',
                                     related_name='active_user', blank=True,
                                     null=True, on_delete=models.SET_NULL)
    # choice_order = models.ForeignKey(Order, verbose_name='выбор заказа',
    #                                  related_name='choice_user', blank=True,
    #                                  null=True, on_delete=models.CASCADE)
    choice_orderbot = models.ManyToManyField(OrderBot, verbose_name='заказы могут выбрать', related_name='choice_user',
                                          blank=True)

    orderbot = models.ManyToManyField(OrderBot, verbose_name='заказ выбран', related_name='user',
                                   blank=True)
    show_phone = models.BooleanField(verbose_name='показать телефон', default=False)
    change_time = models.BooleanField(verbose_name='перенос времени', default=False)
    completed_block = models.BooleanField(verbose_name='нужен отчет', default=False)
    status_block = models.CharField(max_length=30, choices=STATUS_BLOCK, default='new')
    choice = models.BooleanField(verbose_name='Выбирает', default=False)
    percent = models.IntegerField(verbose_name='Процент компании', default=50)
    user = TGUserManager()
    objects = models.Manager()

    class Meta:
        verbose_name = 'ТГ Пользователь'
        verbose_name_plural = 'ТГ Пользователи'

    def __str__(self):
        return self.name


class TGAmoChat(models.Model):
    amo_leads_id = models.IntegerField(verbose_name='амо id сделки', blank=True, null=True)
    # tg_id = models.IntegerField(verbose_name='телеграмм id мастера', blank=True, null=True)
    text = models.CharField(max_length=250, verbose_name='сообщение', blank=True, null=True)
    amo2tg = models.BooleanField(verbose_name='из Амо в ТГ', default=False)
    issend = models.BooleanField(verbose_name='отправлено', default=False)
    iserror = models.BooleanField(verbose_name='Ошибка отправки', default=False)
    objects = models.Manager()

    class Meta:
        verbose_name = 'ТГ чат с амо'
        verbose_name_plural = 'ТГ чаты с амо'

    def __str__(self):
        return self.text
