from django.shortcuts import render
from django.template import loader
from plotly.offline import plot
from plotly.graph_objs import Scatter
# Create your views here.

def index(request):
    x_data = [0,1,2,3]
    y_data = [x**2 for x in x_data]
    plot_div = plot([Scatter(x=x_data, y=y_data,
                        mode='lines', name='test',
                        opacity=0.8, marker_color='green')],
               output_type='div')
    plot_div2 = plot([Scatter(x=x_data, y=y_data,
                        mode='lines', name='test',
                        opacity=0.8, marker_color='red')],
               output_type='div')

    context = {
        'plot_div': plot_div,
        'plot_div2': plot_div2
    }
    return render(request, "FinanceMath/index.html", context=context)
