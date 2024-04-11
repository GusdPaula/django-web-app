from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=200, null=True, unique=True)
    date_created = models.DateField(null=True, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    def __str__(self) -> str:
        return self.name

class Expenses(models.Model):
    name = models.CharField(max_length=200, null=True)
    date_created = models.DateField(null=True, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    categories = models.ForeignKey(
        ExpenseCategory, 
        to_field='name', # ← Here
        on_delete=models.PROTECT
    )
    amount = models.FloatField(null=True)

    def __str__(self) -> str:
        return self.name


class IncomeCategory(models.Model):
    name = models.CharField(max_length=200, null=True, unique=True)
    date_created = models.DateField(null=True, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    def __str__(self) -> str:
        return self.name
    

class Incomes(models.Model):
    name = models.CharField(max_length=200, null=True)
    date_created = models.DateField(null=True, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    categories = models.ForeignKey(
        IncomeCategory, 
        to_field='name', # ← Here
        on_delete=models.PROTECT
    )
    amount = models.FloatField(null=True)

    def __str__(self) -> str:
        return self.name


class SavingsCategory(models.Model):
    name = models.CharField(max_length=200, null=True, unique=True)
    date_created = models.DateField(null=True, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    def __str__(self) -> str:
        return self.name


class Savings(models.Model):
    name = models.CharField(max_length=200, null=True)
    date_created = models.DateField(null=True, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    categories = models.ForeignKey(
        SavingsCategory, 
        to_field='name', # ← Here
        on_delete=models.PROTECT
    )
    amount = models.FloatField(null=True)

    def __str__(self) -> str:
        return self.name