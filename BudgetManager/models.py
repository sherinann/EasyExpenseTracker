from django.db import models

# Create your models here.
from UserManagement.models import Profile


# class Budget(models.Model):
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     name = models.CharField(max_length=250)
#     color = models.IntegerField()
#
#     created = models.DateTimeField()
#
#
# class Income(models.Model):
#     budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
#     name = models.CharField(max_length=250)
#     amount = models.DecimalField(12, 2)
#
#     created = models.DateTimeField()
#
#
# class BudgetCategory(models.Model):
#     budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
#     name = models.CharField(max_length=250)
#     amount = models.DecimalField(12, 2)
#
#     created = models.DateTimeField()
#
#
# class Expense(models.Model):
#     category = models.ForeignKey(BudgetCategory, on_delete=models.CASCADE)
#     amount = models.DecimalField(12,2)
#
#     created = models.DateTimeField()