# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
sites = list(spacex_df['Launch Site'].unique())
sites.append("All Sites")

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options = [
                                    {'label':site,'value':site} for site in sites
                                ],
                                value = "All Sites",
                                placeholder = "Select a launch site",
                                searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min = 0,
                                max = 10000,
                                step=1000,
                                value = [min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart',component_property='figure'),
    Input(component_id='site-dropdown',component_property='value')
)
def updatePieChart(enteredSite):
    filteredDf = spacex_df
    if enteredSite == "All Sites":
        fig = px.pie(filteredDf, values = 'class',
        names = "Launch Site",
        title = "Success Rates for all the Sites")
        return fig
    else:
        filteredDf = filteredDf[filteredDf["Launch Site"] == enteredSite]
        valuesCount = filteredDf["class"].value_counts()
        fig = px.pie(
        names = filteredDf["class"].unique(),
        values = valuesCount,
        title = f"Success Rates for {enteredSite}")
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart',component_property='figure'),
    [Input(component_id='site-dropdown',component_property='value'),
    Input(component_id='payload-slider',component_property='value')]
)
def getScatterChartOfSuccess(selectedSite,selectedRange):
    launchData = spacex_df
    if selectedSite == "All Sites":
        fig = px.scatter(
            launchData,
            x = "Payload Mass (kg)",
            y = "class",
            color = "Booster Version Category",
            range_x = selectedRange
        )
        return fig
    else : 
        launchData = launchData[launchData["Launch Site"] == selectedSite]
        fig = px.scatter(
            launchData,
            x = "Payload Mass (kg)",
            y = "class",
            color = "Booster Version Category",
            range_x = selectedRange
        )
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
