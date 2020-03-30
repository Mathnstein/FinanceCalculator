from django.shortcuts import render
from django.template import loader
from plotly.offline import plot
from plotly.graph_objs import Scatter, Bar, Layout
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta

from .forms import FinanceForm
# Create your views here.

def index(request):
    oToday = datetime.datetime.today()
    initial = {
        'fBasePay': 50E3,
        'fVariablePayPercent': 5.0,
        'iSteps': 5,
        'fInitialSavings': 0,
        'sTimeScale': 'Yearly',
        'fPercentRaise': 2.0,
        'fIncomeTaxPercent': 31.0,
        'fBonusTaxPercent': 50.0
    }
    if request.method == 'POST':
        form = FinanceForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
    else:
        form = FinanceForm(initial=initial)
        cleaned_data=initial
    fBasePay = cleaned_data['fBasePay']
    fVariablePayPercent = cleaned_data['fVariablePayPercent']
    iSteps = cleaned_data['iSteps']
    fInitialSavings = cleaned_data['fInitialSavings'] 
    sTimeScale = cleaned_data['sTimeScale'] 
    fPercentRaise = cleaned_data['fPercentRaise']
    fIncomeTaxPercent = cleaned_data['fIncomeTaxPercent']
    fBonusTaxPercent = cleaned_data['fBonusTaxPercent']

    # Fixed values
    fAggressivePercent = 25
    fModeratePercent = 18
    fSomePercent = 10

    # Create plotting vectors
    iSteps = np.arange(iSteps+1)
    if sTimeScale == 'Yearly':
        x_axis = iSteps + oToday.year
        factor = 1
    elif sTimeScale == 'Monthly':
        x_axis = [(oToday+relativedelta(months=+inc)).strftime('%b, %Y') for inc in iSteps]
        factor = 12
    elif sTimeScale == 'Bi-Weekly':
        x_axis = [(oToday+relativedelta(weeks=+2.0*inc)).strftime('%d %b, %Y') for inc in iSteps]
        factor = 26

    Pay = (fBasePay/factor)*(1+fPercentRaise/100)**(iSteps/factor)
    Pay = np.around(Pay)
    TaxedPay = Pay*(1-fIncomeTaxPercent/100)
    TaxedPay = np.around(TaxedPay)

    AggressiveSaved = np.cumsum(TaxedPay)*(fAggressivePercent/100) + fInitialSavings
    AggressiveSaved = np.around(AggressiveSaved)

    ModerateSaved = np.cumsum(TaxedPay)*(fModeratePercent/100) + fInitialSavings
    ModerateSaved = np.around(ModerateSaved)

    SomeSaved = np.cumsum(TaxedPay)*(fSomePercent/100) + fInitialSavings
    SomeSaved = np.around(SomeSaved)

    # Plot
    data = [
            Bar(x = x_axis, y = Pay,
                name = sTimeScale+' Pay',
                marker_color='#000839', text = Pay,
                texttemplate='%{text:.3s}', textposition='outside'
                ),
            Bar(x = x_axis, y = TaxedPay,
                name = sTimeScale+' Taxed Pay',
                marker_color='#005082', text = TaxedPay, texttemplate='%{text:.3s}', textposition='outside'
                ),
            Scatter(x = x_axis, y = AggressiveSaved,
                    mode = 'lines+markers', name = 'Aggressive Savings (25%)',
                    marker_color='#9d0b0b',
                    yaxis='y2'),
            Scatter(x = x_axis, y = ModerateSaved,
                    mode = 'lines+markers', name = 'Moderate Savings (18%)',
                    marker_color='#da2d2d',
                    yaxis='y2'),
            Scatter(x = x_axis, y = SomeSaved,
                    mode = 'lines+markers', name = 'Light Savings (10%)',
                    marker_color='#eb8242',
                    yaxis='y2')
            ]

    layout = Layout(
        title= 'Finances Over Time',
        xaxis= dict(title='Time'),
        yaxis= dict(title='Amount', color='#000839', range=[0, np.max(Pay*1.1)]),
        yaxis2= dict(title = 'Total Saved', color = '#da2d2d',
                overlaying = 'y', side = 'right', showgrid = False),
        legend= dict(x = 0, y = 1.1, bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)', orientation='h'),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1
    )

    if sTimeScale == 'Yearly':
        Bonus = Pay*(fVariablePayPercent/100)
        Bonus = np.around(Bonus)
        data.append(
            Bar(x = x_axis, y = Bonus,
                name='Yearly Bonus', marker_color='#00a8cc', text = Bonus, texttemplate='%{text:.3s}', textposition='outside'
            )
        ) 
    output_plot = {
        'data': data,
        'layout': layout
    }

    axis_html = plot(output_plot, output_type='div', include_plotlyjs=False, show_link=False, link_text='')

    context = {
        'plot': axis_html,
        'form': form
    }
    return render(request, "FinanceMath/index.html", context=context)
