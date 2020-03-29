from django.shortcuts import render
from django.template import loader
from plotly.offline import plot
from plotly.graph_objs import Scatter, Bar, Layout
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
# Create your views here.

def index(request):
    oToday = datetime.datetime.today()
    sTimeScale = 'Monthly'
    fBasePay = 78E3
    fVariablePayPercent = 12
    iSteps = 12

    # initial values
    fInitialSavings = 26*1E3
    fPercentSaved = 25
    fPercentRaise = 115
    fIncomeTaxPercent = 31
    fBonusTaxPercent = 25

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

    Pay = (fBasePay/factor)*(fPercentRaise/100)**(iSteps/factor)
    Pay = np.around(Pay)
    TaxedPay = Pay*(1-fIncomeTaxPercent/100)
    TaxedPay = np.around(TaxedPay)

    Saved = np.cumsum(TaxedPay)*(fPercentSaved/100) + fInitialSavings
    Saved = np.around(Saved)

    # Plot
    axis = [
            Bar(x=x_axis, y=Pay,
                name=sTimeScale+' Pay',
                opacity=0.8),
            Bar(x=x_axis, y=TaxedPay,
                name =sTimeScale+' Taxed Pay'),
            Scatter(x=x_axis,y=Saved,
                    mode = 'lines', name = 'Total Amount Saved',
                    marker_color='orange')
            ]

    # layout = {
    #     title: 'Finances Over Time',
    #     xaxis: sTimeScale
    # }

    if sTimeScale == 'Yearly':
        Bonus = Pay*(fVariablePayPercent/100)
        Bonus = np.around(Bonus)
        axis.append(
            Bar(x = x_axis, y = Bonus,
                name='Yearly Bonus'
            )
        ) 

    axis_html = plot(axis,
               output_type='div',
               include_plotlyjs=False)

    context = {
        'axis_html': axis_html
    }
    return render(request, "FinanceMath/index.html", context=context)
