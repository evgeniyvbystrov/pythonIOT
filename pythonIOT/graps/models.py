from django.db import models

class IOTData (models.Model):

    datetime = models.DateTimeField('Дата')
    device = models.CharField('Устройство', max_length=25)
    value = models.DecimalField('Значение', decimal_places=5, max_digits=10)

    def __str__(self):
        return '{} / {} / {}'.format(self.datetime, self.device, self.value)

    class Meta:
        verbose_name = 'IOT Data'

class Tasks (models.Model):

    datetime = models.DateTimeField('Дата')
    device = models.CharField('Устройство', max_length=25)
    task = models.DecimalField('Значение', decimal_places=5, max_digits=10)

    def __str__(self):
        return '{} / {} / {}'.format(self.datetime, self.device, self.value)

    class Meta:
        verbose_name = 'Task'