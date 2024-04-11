from django.forms import ModelForm
from .models import Expenses, ExpenseCategory, IncomeCategory, Incomes, Savings, SavingsCategory

class ExpenseForm(ModelForm):
    class Meta:
        model = Expenses
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ExpenseForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ExpenseCatForm(ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ExpenseCatForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class IncomeForm(ModelForm):
    class Meta:
        model = Incomes
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(IncomeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class IncomeCatForm(ModelForm):
    class Meta:
        model = IncomeCategory
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(IncomeCatForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



class SavingsForm(ModelForm):
    class Meta:
        model = Savings
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SavingsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class SavingsCatForm(ModelForm):
    class Meta:
        model = SavingsCategory
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SavingsCatForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
