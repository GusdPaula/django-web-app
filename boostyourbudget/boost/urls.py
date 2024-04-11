from django.contrib import admin
from django.urls import path
from . import views

app_name = "boost"
urlpatterns = [
        path('', views.boost, name='boost'),
        path('expenses/', views.expenses, name='expenses'),
        path('expenses/api/data', views.get_expense_api_data, name='api_expenses_data'),
        path('incomes/', views.incomes, name='incomes'),
        path('savings/', views.savings, name='savings'),
        path('expenses/update_expense/<str:pk>', views.updateExpense, name='update_expense'),
        path('expenses/update_savings/<str:pk>', views.updateSavings, name='update_savings'),
        path('expenses/update_income/<str:pk>', views.updateIncome, name='update_income'),
        path('expenses/delete_expense/<str:pk>', views.deleteExpense, name='delete_expense'),
        path('expenses/delete_savings/<str:pk>', views.deleteSavings, name='delete_savings'),
        path('expenses/delete_income/<str:pk>', views.deleteIncome, name='delete_income'),
        path('expenses/expense_categories/', views.expensesCat, name='expense_categories'),
        path('expenses/income_categories/', views.incomesCat, name='income_categories'),
        path('expenses/savings_categories/', views.savingsCat, name='savings_categories'),
        path('expenses/delete_expense_cat/<str:pk>', views.deleteExpenseCat, name='delete_expense_cat'),
        path('expenses/delete_income_cat/<str:pk>', views.deleteIncomeCat, name='delete_income_cat'),
        path('expenses/delete_savings_cat/<str:pk>', views.deleteSavingsCat, name='delete_savings_cat'),
]