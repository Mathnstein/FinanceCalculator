from django import forms

class FinanceForm(forms.Form):
    fBasePay = forms.FloatField(label='Base Pay:', min_value=0, max_value=1E6) 
    fVariablePayPercent = forms.FloatField(label='Variable Pay Percent:', min_value=0, max_value=100)
    fPercentRaise = forms.FloatField(label='Expected annual raise:', min_value=0, max_value=100)
    choices = [
        ('Yearly', 'Yearly'),
        ('Monthly', 'Monthly'),
        ('Bi-Weekly', 'Bi-Weekly')]
    sTimeScale = forms.ChoiceField(label='Pay Schedule:', widget=forms.RadioSelect,choices=choices)
    iSteps = forms.IntegerField(label='Number of Pay Cycles:', min_value=1, max_value=60)
    fInitialSavings = forms.FloatField(label='Initial Savings:', min_value=0, max_value=1E6)
    fIncomeTaxPercent = forms.FloatField(label='Income Tax Percent:', min_value=0, max_value=100)
    fBonusTaxPercent = forms.FloatField(label='Bonus Tax Percent:', min_value=0, max_value=100)

    def __init__(self, *args, **kwargs):
        # Get 'initial argument if any
        initial_arguments = kwargs.get('initial', None)
        updated_initial = {}
        if initial_arguments:
            for key in kwargs['initial']:
                updated_initial[key] = initial_arguments.get(key, None)
        kwargs.update(initial=updated_initial)
        super(FinanceForm, self).__init__(*args, **kwargs)