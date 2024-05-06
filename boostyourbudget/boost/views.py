from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expenses, ExpenseCategory, IncomeCategory, Incomes, Savings, SavingsCategory
from .forms import ExpenseForm, ExpenseCatForm, IncomeForm, IncomeCatForm, SavingsCatForm, SavingsForm
from datetime import datetime
from django.db.models import Sum
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
import pandas as pd


fin_dict = {'Expenses':
            [{'form': ExpenseForm},
             {'model': Expenses},
             {'categories': ExpenseCategory},
             {'cat_form': ExpenseCatForm},
             {'fyn_type': 'Expense'},
             {'fyn_type_plural': 'Expenses'}],
             "Incomes":
             [{'form': IncomeForm},
               {'model': Incomes},
               {'categories': IncomeCategory},
               {'cat_form': IncomeCatForm},
               {'fyn_type': 'Income'},
               {'fyn_type_plural': 'Incomes'}],
               "Savings":
             [{'form': SavingsForm},
               {'model': Savings},
               {'categories': SavingsCategory},
               {'cat_form': SavingsCatForm},
               {'fyn_type': 'Saving'},
               {'fyn_type_plural': 'Savings'}]}



def finDataAdd(request, fintype):
    form = fin_dict[fintype][0]['form']
    if request.method == 'POST':
        form = fin_dict[fintype][0]['form'](request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.date_created = datetime.now().today()
            obj.save()
            return redirect('boost:fin-data-add', fintype)
             
    database = fin_dict[fintype][1]['model'].objects.all()
    fin_type = fin_dict[fintype][4]['fyn_type']
    fin_type_plural = fin_dict[fintype][5]['fyn_type_plural']
    
    context = {'form': form,
               'database': database,
               'fin_type': fin_type,
               'fin_type_plural': fin_type_plural}
    
    return render(request, 'boost/fin-data-add.html', context)


@login_required(login_url='home:login')
def finCatAdd(request, fintype):
    
    form = fin_dict[fintype][3]['cat_form']
    if request.method == 'POST':
        form = fin_dict[fintype][3]['cat_form'](request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.date_created = datetime.now().today()
            obj.save()
            return redirect('boost:fin-categories', fintype)
            
    database = fin_dict[fintype][2]['categories'].objects.all()
    fin_type = fin_dict[fintype][4]['fyn_type']
    fin_type_plural = fin_dict[fintype][5]['fyn_type_plural']
    
    context = {'form': form,
               'database': database,
               'fin_type': fin_type,
               'fin_type_plural': fin_type_plural}
    
    
    return render(request, 'boost/fin-categories.html', context)


@login_required(login_url='home:login')
def finDataUpdate(request, fintype, pk):
    data = fin_dict[fintype][1]['model'].objects.get(id=pk)
    form = fin_dict[fintype][0]['form'](instance=data)
    if request.method == 'POST':
        form = fin_dict[fintype][0]['form'](request.POST, instance=data)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            
            return redirect('boost:fin-data-add', fintype)

    database = database = fin_dict[fintype][1]['model'].objects.all()
    fin_type = fin_dict[fintype][4]['fyn_type']
    fin_type_plural = fin_dict[fintype][5]['fyn_type_plural']
    
    context = {'form': form,
               'database': database,
               'fin_type': fin_type,
               'fin_type_plural': fin_type_plural}
    return render(request, 'boost/fin-data-update.html', context)


@login_required(login_url='home:login')
def finDataDelete(request, fintype, pk):
    data = fin_dict[fintype][1]['model'].objects.get(id=pk)

    if request.method == 'POST':
        data.delete()
        return redirect('boost:fin-data-add', fintype)

    fin_type = fin_dict[fintype][4]['fyn_type']
    fin_type_plural = fin_dict[fintype][5]['fyn_type_plural']
    context = {'data': data,
               'fin_type': fin_type,
               'fin_type_plural': fin_type_plural}
    return render(request, 'boost/fin-data-delete.html', context)


@login_required(login_url='home:login')
def finCatDelete(request, fintype, pk):
    category = fin_dict[fintype][2]['categories'].objects.get(id=pk)

    if request.method == 'POST':
        category.delete()
        return redirect('boost:fin-categories', fintype)

    fin_type = fin_dict[fintype][4]['fyn_type']
    fin_type_plural = fin_dict[fintype][5]['fyn_type_plural']
    context = {'data': category,
               'fin_type': fin_type,
               'fin_type_plural': fin_type_plural}
    return render(request, 'boost/fin-cat-delete.html', context)


def get_expense_api_data(request, *args, **kwargs):

    sort_order = ['January','February','March','April','May','June','July','August','September','October','November','December']

    exp_df = pd.DataFrame(Expenses.objects.filter(user=request.user).all().values('date_created', 'amount'))
    categories = dict()

    if exp_df.empty:
        default_items_exp = [0]
        labels_exp = [0]
    
    else:
        categories['expenses'] = pd.unique(pd.DataFrame(Expenses.objects.filter(user=request.user).all().values('categories')).categories.values).tolist()
    
        exp_df['date_created'] = pd.to_datetime(exp_df['date_created'])
        exp_df = pd.DataFrame(exp_df.groupby(exp_df['date_created'].dt.strftime('%B'))['amount'].sum())
        exp_df["date_created"] = exp_df.index
        exp_df.index = pd.CategoricalIndex(exp_df["date_created"], categories=sort_order, ordered=True)
        exp_df = exp_df.sort_index().reset_index(drop=True)

        default_items_exp = exp_df.amount.tolist()
        labels_exp = exp_df.date_created.tolist()
    
    inc_df = pd.DataFrame(Incomes.objects.filter(user=request.user).all().values('date_created', 'amount'))
    

    if inc_df.empty:
        default_items_inc = [0]
        labels_inc = [0]
    
    else:
        categories['incomes'] = pd.unique(pd.DataFrame(Incomes.objects.filter(user=request.user).all().values('categories')).categories.values).tolist()
        
        inc_df['date_created'] = pd.to_datetime(inc_df['date_created'])
        inc_df = pd.DataFrame(inc_df.groupby(inc_df['date_created'].dt.strftime('%B'))['amount'].sum())
        inc_df["date_created"] = inc_df.index
        inc_df.index = pd.CategoricalIndex(inc_df["date_created"], categories=sort_order, ordered=True)
        inc_df = inc_df.sort_index().reset_index(drop=True)
        
        default_items_inc = inc_df.amount.tolist()
        labels_inc = inc_df.date_created.tolist()
    try:
        net_df = pd.merge(inc_df, exp_df, how='outer', on='date_created')
        net_df = net_df.fillna(0)
        net_df['amount'] = net_df['amount_x'] - net_df['amount_y']
        net_df.index = pd.CategoricalIndex(net_df["date_created"], categories=sort_order, ordered=True)
        net_df = net_df.sort_index().reset_index(drop=True)

        default_items_net = net_df.amount.tolist()
        labels_net = net_df.date_created.tolist()

    except KeyError:
        if inc_df.empty:
            net_df = exp_df
        
        elif exp_df.empty:
            net_df = inc_df
        
        net_df.index = pd.CategoricalIndex(net_df["date_created"], categories=sort_order, ordered=True)
        net_df = net_df.sort_index().reset_index(drop=True)

        default_items_net = net_df.amount.tolist()
        labels_net = net_df.date_created.tolist()
        
    savings_df = pd.DataFrame(Savings.objects.filter(user=request.user).all().values('date_created', 'amount'))

    if savings_df.empty:
        default_items_savings = [0]
        labels_savings = [0]

    else:
        categories['savings'] = pd.unique(pd.DataFrame(Savings.objects.filter(user=request.user).all().values('categories')).categories.values).tolist()
        
        savings_df['date_created'] = pd.to_datetime(savings_df['date_created'])
        savings_df = pd.DataFrame(savings_df.groupby(savings_df['date_created'].dt.strftime('%B'))['amount'].sum())
        savings_df["date_created"] = savings_df.index
        savings_df.index = pd.CategoricalIndex(savings_df["date_created"], categories=sort_order, ordered=True)
        savings_df = savings_df.sort_index().reset_index(drop=True)

        default_items_savings = savings_df.amount.tolist()
        labels_savings = savings_df.date_created.tolist()

    labels = {'expenses': labels_exp, 
              'incomes': labels_inc,
              'net': labels_net,
              'savings': labels_savings}
    
    default_items = {'expenses': default_items_exp,
                     'incomes': default_items_inc,
                     'net': default_items_net,
                     'savings': default_items_savings}

    data = {
        'labels': labels,
        'default': default_items,
        'categories': categories
    }

    return JsonResponse(data, safe=False) 



@login_required(login_url='home:login')
def boost(request):

    expenses_total = Expenses.objects.filter(user=request.user).aggregate(Sum('amount'))

    if not expenses_total['amount__sum'] == None:
        expenses_total = expenses_total['amount__sum']
    else:
        expenses_total = 0
    
    incomes_total = Incomes.objects.filter(user=request.user).aggregate(Sum('amount'))

    if not incomes_total['amount__sum'] == None:
        incomes_total = incomes_total['amount__sum']
    else:
        incomes_total = 0

    savings_total = Savings.objects.filter(user=request.user).aggregate(Sum('amount'))

    if not savings_total['amount__sum'] == None:
        savings_total = savings_total['amount__sum']
    else:
        savings_total = 0

    currentDateTime = datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")
    net = incomes_total - expenses_total

    context = {'net': net, 
               'expenses_total': expenses_total, 
               'incomes_total': incomes_total,
               'savings_total': savings_total,
               'year': year}

    return render(request, 'boost/home.html', context)


# @login_required(login_url='home:login')
# def expenses(request):
    
#     form = ExpenseForm()
#     if request.method == 'POST':
#         form = ExpenseForm(request.POST)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.user = request.user
#             obj.date_created = datetime.now().today()
#             obj.save()
#             return redirect('boost:expenses')
            
            
#     expenses = Expenses.objects.all()
#     context = {'form': form, 'expenses': expenses}
#     return render(request, 'boost/expenses.html', context)


# @login_required(login_url='home:login')
# def updateExpense(request, pk):
#     expense = Expenses.objects.get(id=pk)
#     form = ExpenseForm(instance=expense)
#     if request.method == 'POST':
#         form = ExpenseForm(request.POST, instance=expense)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.user = request.user
#             obj.save()
#             return redirect('boost:expenses')

#     context = {'form': form, 'expenses': expenses}
#     return render(request, 'boost/update_expense.html', context)


# @login_required(login_url='home:login')
# def deleteExpense(request, pk):
#     expense = Expenses.objects.get(id=pk)

#     if request.method == 'POST':
#         expense.delete()
#         return redirect('boost:expenses')

#     context = {'expense': expense}
#     return render(request, 'boost/delete_expense.html', context)


# @login_required(login_url='home:login')
# def expensesCat(request):
    
#     form = ExpenseCatForm()
#     if request.method == 'POST':
#         form = ExpenseCatForm(request.POST)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.user = request.user
#             obj.date_created = datetime.now().today()
#             obj.save()
#             return redirect('boost:expense_categories')
            
#     expense_categories = ExpenseCategory.objects.all()
#     context = {'form': form, 'expense_categories': expense_categories}
#     return render(request, 'boost/expense_cat.html', context)


# @login_required(login_url='home:login')
# def deleteExpenseCat(request, pk):
#     expense_category = ExpenseCategory.objects.get(id=pk)

#     if request.method == 'POST':
#         expense_category.delete()
#         return redirect('boost:expense_categories')

#     context = {'expense_category': expense_category}
#     return render(request, 'boost/delete_expense_cat.html', context)


# @login_required(login_url='home:login')
# def incomes(request):
    
#     form = IncomeForm()
#     if request.method == 'POST':
#         form = IncomeForm(request.POST)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.user = request.user
#             obj.date_created = datetime.now().today()
#             obj.save()
#             return redirect('boost:incomes')
                       
#     incomes = Incomes.objects.all()
#     context = {'form': form, 'incomes': incomes}
#     return render(request, 'boost/incomes.html', context)


# @login_required(login_url='home:login')
# def updateIncome(request, pk):
#     income = Incomes.objects.get(id=pk)
#     form = IncomeForm(instance=income)
#     if request.method == 'POST':
#         form = IncomeForm(request.POST, instance=income)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.user = request.user
#             obj.save()
#             return redirect('boost:incomes')

#     context = {'form': form, 'incomes': incomes}
#     return render(request, 'boost/update_income.html', context)


# @login_required(login_url='home:login')
# def deleteIncome(request, pk):
#     income = Incomes.objects.get(id=pk)

#     if request.method == 'POST':
#         income.delete()
#         return redirect('boost:incomes')

#     context = {'income': income}
#     return render(request, 'boost/delete_income.html', context)


# @login_required(login_url='home:login')
# def incomesCat(request):
    
#     form = IncomeCatForm()
#     if request.method == 'POST':
#         form = IncomeCatForm(request.POST)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.user = request.user
#             obj.date_created = datetime.now().today()
#             obj.save()
#             return redirect('boost:income_categories')
            
#     income_categories = IncomeCategory.objects.all()
#     context = {'form': form, 'income_categories': income_categories}
#     return render(request, 'boost/income_cat.html', context)


# @login_required(login_url='home:login')
# def deleteIncomeCat(request, pk):
#     income_category = IncomeCategory.objects.get(id=pk)

#     if request.method == 'POST':
#         income_category.delete()
#         return redirect('boost:income_categories')

#     context = {'income_category': income_category}
#     return render(request, 'boost/delete_income_cat.html', context)


# @login_required(login_url='home:login')
# def savings(request):
    
#     form = SavingsForm()
#     if request.method == 'POST':
#         form = SavingsForm(request.POST)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.user = request.user
#             obj.date_created = datetime.now().today()
#             obj.save()
#             return redirect('boost:savings')
            
#     savings = Savings.objects.all()
#     context = {'form': form, 'savings': savings}
#     return render(request, 'boost/savings.html', context)


# @login_required(login_url='home:login')
# def savingsCat(request):
    
#     form = SavingsCatForm()
#     if request.method == 'POST':
#         form = SavingsCatForm(request.POST)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.user = request.user
#             obj.date_created = datetime.now().today()
#             obj.save()
#             return redirect('boost:savings_categories')
            
#     savings_categories = SavingsCategory.objects.all()
#     context = {'form': form, 'savings_categories': savings_categories}
#     return render(request, 'boost/savings_cat.html', context)


# @login_required(login_url='home:login')
# def updateSavings(request, pk):
#     saving = Savings.objects.get(id=pk)
#     form = SavingsForm(instance=saving)
#     if request.method == 'POST':
#         form = SavingsForm(request.POST, instance=saving)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.user = request.user
#             obj.save()
#             return redirect('boost:savings')

#     context = {'form': form, 'savings': savings}
#     return render(request, 'boost/update_savings.html', context)


# @login_required(login_url='home:login')
# def deleteSavings(request, pk):
#     saving = Savings.objects.get(id=pk)

#     if request.method == 'POST':
#         saving.delete()
#         return redirect('boost:savings')

#     context = {'savings': saving}
#     return render(request, 'boost/delete_savings.html', context)


# @login_required(login_url='home:login')
# def deleteSavingsCat(request, pk):
#     savings_category = SavingsCategory.objects.get(id=pk)

#     if request.method == 'POST':
#         savings_category.delete()
#         return redirect('boost:savings_category')

#     context = {'savings_category': savings_category}
#     return render(request, 'boost/delete_savings_cat.html', context)
