import enum
from datetime import datetime
from decimal import Decimal

from django.db import models, transaction
from django.db.models import prefetch_related_objects

from userprofile.models import Profile


class Budget(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    color = models.IntegerField()

    created = models.DateTimeField()

    @property
    def serialize(self):
        return {
            "name": self.name,
            "color": hex(self.color)
        }

    def set_color_hex(self, hex_val: str):
        self.color = int(hex_val, base=16)

    def get_color_hex(self):
        return hex(self.color)

    def get_serialized_income_set(self):
        return [i.serialize for i in self.income_set]

    def get_serialized_category_set(self):
        return [i.serialize for i in self.budgetcategory_set]

    def get_details(self):
        prefetch_related_objects([self], 'income_set', 'budgetcategory_set', 'budgetcategory_set__expense_set',
                                 'budgetcategory_set__recurringexpense_set')

        total_income = sum([i.amount for i in self.income_set])
        projected_expense = sum([i.amount for i in self.budgetcategory_set])
        projected_savings = sum([i.amount for i in self.savings_set])
        projected_cash_margin = total_income - projected_expense - projected_savings
        return {
            "budget": self.serialize,
            "income_list": [i.serialize for i in self.income_set],
            "budget_category_list": [i.get_serialized_expense_details() for i in self.budgetcategory_set],
            "savings_list": [i.serialize for i in self.savings_set],
            "total_income": total_income,
            "projected_expense": projected_expense,
            "projected_savings": projected_savings,
            "projected_cash_margin": projected_cash_margin
        }

    @classmethod
    def create(cls, name: str, color_hex: str):
        c = cls()
        c.name = name
        c.color = int(color_hex, base=16)
        c.save()
        return c


class AbstractBudgetParticular(models.Model):
    class Meta:
        abstract = True

    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    created = models.DateTimeField()

    @property
    def serialize(self):
        return {
            "name": self.name,
            "amount": self.amount,
            "created": self.created
        }

    @classmethod
    def create(cls, budget_id: int, name: str, amount: Decimal):
        c = cls()
        c.name = name
        c.amount = amount
        c.budget_id = budget_id
        c.save()
        return c


class Income(AbstractBudgetParticular):
    pass


class BudgetCategory(AbstractBudgetParticular):

    def get_serialized_expense_details(self):
        prefetch_related_objects([self], 'expense_set')
        total_expense = sum([i.amount for i in self.expense_set])
        return {
            "budget_category": self.serialize,
            "expense_list": [i.serialize for i in self.expense_set],
            "recurring_expense": [i.serialize for i in self.recurringexpense_set],
            "total_expense": total_expense
        }


class Savings(AbstractBudgetParticular):
    pass


class AbstractExpense(models.Model):
    class Meta:
        abstract = True

    category = models.ForeignKey(BudgetCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    particular = models.CharField(max_length=500)

    created = models.DateTimeField()

    @property
    def serialize(self):
        return {
            "amount": self.amount,
            "created": self.created
        }

    @classmethod
    def create(cls, category_id: int, amount: Decimal):
        c = cls()
        c.category_id = category_id
        c.amount = amount
        c.save()
        return c


class Expense(AbstractExpense):
    pass


class RecurringExpense(AbstractExpense):
    recurring_date = models.IntegerField()

    @classmethod
    def apply_expense(cls):
        current_date = datetime.now().day
        recurring_list = RecurringExpense.objects.filter(recurring_date=current_date)

        with transaction.atomic():
            for recurring_expense in recurring_list:
                expense = Expense()
                expense.category_id = recurring_expense.category_id
                expense.amount = recurring_expense.amount
                expense.particular = recurring_expense.particular
                expense.save()
