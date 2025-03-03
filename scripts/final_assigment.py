import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Cargamos los datos
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Inicializamos la aplicación Dash
app = dash.Dash(__name__)

# Lista de años
year_list = [i for i in range(1980, 2024, 1)]

# Creamos el layout del dashboard
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", 
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': '24px'}),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            value='Recession Period Statistics',
            placeholder='Select a report type',
            style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}
        )
    ]),
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value=None,
            placeholder='Select-year',
            style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}
        )
    ]),
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex', 'flex-direction': 'column'})
])

# Callback para habilitar/deshabilitar el dropdown de año
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

# Callback para actualizar los gráficos
@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'), Input('select-year', 'value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', 
                           title="Average Automobile Sales Fluctuation Over Recession Period"))
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales', 
                          title="Average Automobile Sales by Vehicle Type During Recession"))
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type', 
                          title="Advertising Expenditure by Vehicle Type During Recession"))
        unemp_data = recession_data.groupby(['Vehicle_Type', 'unemployment_rate'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type',
                          labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                          title="Effect of Unemployment Rate on Vehicle Type and Sales"))
        return [
            html.Div(className='chart-item', children=[html.Div(R_chart1), html.Div(R_chart2)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(R_chart3), html.Div(R_chart4)], style={'display': 'flex'})
        ]
    elif selected_statistics == 'Yearly Statistics' and input_year:
        yearly_data = data[data['Year'] == input_year]
        yas = data.groupby('Year')['Automobile_Sales'].sum().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas, x='Year', y='Automobile_Sales', 
                           title="Total Yearly Automobile Sales"))
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(mas, x='Month', y='Automobile_Sales', 
                           title=f"Total Monthly Automobile Sales in {input_year}"))
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales', 
                          title=f"Average Vehicles Sold by Vehicle Type in {input_year}"))
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type', 
                          title=f"Total Advertising Expenditure by Vehicle Type in {input_year}"))
        return [
            html.Div(className='chart-item', children=[html.Div(Y_chart1), html.Div(Y_chart2)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(Y_chart3), html.Div(Y_chart4)], style={'display': 'flex'})
        ]
    else:
        return None

# Ejecutamos la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)