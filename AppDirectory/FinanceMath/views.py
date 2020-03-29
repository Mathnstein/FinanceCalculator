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
    sTimeScale = 'Yearly'
    fBasePay = 78E3
    fVariablePayPercent = 12
    iSteps = 12

    # initial values
    fInitialSavings = 26*1E3
    fPercentSaved = 25
    fPercentRaise = 105
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
    data = [
            Bar(x = x_axis, y = Pay,
                name = sTimeScale+' Pay',
                marker_color='rgb(1,87,155)'
                ),
            Bar(x = x_axis, y = TaxedPay,
                name = sTimeScale+' Taxed Pay',
                marker_color='rgb(3,169,250)'
                ),
            Scatter(x = x_axis, y = Saved,
                    mode = 'lines+markers', name = 'Total Amount Saved',
                    marker_color='orange',
                    yaxis='y2')
            ]

    layout = Layout(
        title= 'Finances Over Time',
        xaxis= dict(title='Time'),
        yaxis= dict(title='Amount', color='rgb(1,87,155)'),
        yaxis2= dict(title = 'Total Saved', color = 'orange',
                overlaying = 'y', side = 'right', showgrid = False),
        legend= dict(x = 0, y = 1.0, bgcolor='rgba(255, 255, 255, 0)',
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
                name='Yearly Bonus', marker_color='rgb(179,229,252)'
            )
        ) 
    output_plot = {
        'data': data,
        'layout': layout
    }

    axis_html = plot(output_plot, output_type='div', include_plotlyjs=False, show_link=False, link_text='')

    context = {
        'plot': axis_html
    }
    return render(request, "FinanceMath/index.html", context=context)
