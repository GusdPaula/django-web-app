from django.contrib import admin

# Register your models here.
from boost.models import ExpenseCategory, Expenses, IncomeCategory, Incomes

admin.site.register(Expenses)
admin.site.register(ExpenseCategory)
admin.site.register(IncomeCategory)
admin.site.register(Incomes)