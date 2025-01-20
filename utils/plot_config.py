from utils.overview_chart_create import add_plot_to_fig
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def setup_horizontal_bar(series, x_name, y_name, color_bottom, color_top, x_label, y_label, title):
    fig = px.bar(series, x=x_name, y=y_name, color=[color_bottom, color_top],
                color_discrete_map={color_bottom: color_bottom, color_top: color_top},
                labels={x_name: x_label, y_name: y_label},
                title=title, orientation='h')
    fig.update_layout(xaxis=dict(fixedrange=True, tickformat='.1%', showgrid=False),
                    yaxis=dict(fixedrange=True), title_x=0.5)
    fig.update_traces(texttemplate='%{x}', textposition='outside', showlegend=False)
    return fig

def setup_summary_chart(dataframe):
    """
    A setup function to create a figure visualizing every column in the accidents dataframe.
    """    

    accidents_plot = dataframe.copy()

    accidents_plot.Type_of_vehicle.loc[accidents_plot.Type_of_vehicle.str.contains('Lorry', case=False, na=False)] = 'Lorry'
    accidents_plot.Type_of_vehicle.loc[accidents_plot.Type_of_vehicle.str.contains('Public', case=False, na=False)] = 'Public'
    accidents_plot.Type_of_vehicle.loc[accidents_plot.Type_of_vehicle.str.contains('Pick up', case=False, na=False)] = 'Pick-up'

    accidents_plot.Area_accident_occured.loc[accidents_plot.Area_accident_occured.str.contains('AreasO', case=False, na=False)] = np.nan
    accidents_plot.Area_accident_occured.loc[accidents_plot.Area_accident_occured.str.contains('Recreational', case=False, na=False)] = 'Recreational areas'

    number_of_plots = 32
    plots_dimensions = [[2, 0, 1, 1],
                        [1, 1, 1, 1],
                        [2, 0, 1, 1],
                        [1, 2, 0, 1],
                        [2, 0, 1, 1],
                        [1, 1, 2, 0],
                        [2, 0, 1, 1],
                        [2, 0, 1, 1],
                        [1, 1, 1, 1],
                        [1, 2, 0, 1]]

    x_annotation_placements = [0.113, 0.419, 0.725, 1]
    y_annotation_placements = [1, 0.896, 0.792, 0.688, 0.577, 0.4735, 0.3695, 0.2586, 0.155, 0.051]

    plots_specs = []
    SETUP_placements = []
    SETUP_annotation_placements= []
    for row in range(0, len(plots_dimensions)):
        row_specs = []
        for col in range(0, len(plots_dimensions[row])):
            if plots_dimensions[row][col]:
                row_specs.append({'colspan': plots_dimensions[row][col]})
                SETUP_placements.append((row+1, col+1))
                SETUP_annotation_placements.append((x_annotation_placements[col + plots_dimensions[row][col] - 1], y_annotation_placements[row]))
            else:
                row_specs.append(None)
        plots_specs.append(row_specs)

    SETUP_shorten = [None] * number_of_plots
    for i, val in zip([11, 13, 15, 19, 29, 30], [20, 20, 20, 25, 20, 25]):
        SETUP_shorten[i] = val

    SETUP_cat = [None] * number_of_plots
    SETUP_cat[20] = (5,0)

    SETUP_categoryorder = [None] * number_of_plots
    for i in [1, 2, 4, 6, 7, 9]:
        SETUP_categoryorder[i] = 'array'

    SETUP_order = [None] * number_of_plots
    SETUP_order[1] = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    SETUP_order[2] = ['Under 18', '18-30', '31-50', 'Over 51']
    SETUP_order[4] = ['Illiterate', 'Writing & reading', 'Elementary school', 'Junior high school', 'High school', 'Above high school']
    SETUP_order[6] = ['No Licence', 'Below 1yr', '1-2yr', '2-5yr', '5-10yr', 'Above 10yr']
    SETUP_order[9] = ['Below 1yr', '1-2yr', '2-5yrs', '5-10yrs', 'Above 10yr']

    SETUP_range_multiplier = [1.25] * number_of_plots
    for i, val in zip([1, 2, 4, 6, 9], [1.5, 1.4, 1.45, 1.5, 1.5]):
        SETUP_range_multiplier[i] = val

    SETUP_rename = [None] * number_of_plots
    SETUP_rename[12] = ['Two-way (broken lines)', 'Two-way (undivided)', 'Other', 'Median strip', 'One-way', 'Two-way (solid lines)']

    SETUP_tickvals = [None] * number_of_plots
    SETUP_tickvals[20], SETUP_tickvals[21] = True, True

    fig = make_subplots(rows=len(plots_dimensions), cols=len(plots_dimensions[0]),  horizontal_spacing=0.1,
                        vertical_spacing=0.04, specs=plots_specs, subplot_titles=accidents_plot.columns)

    fig.update_layout(width=1500, height=300*len(plots_dimensions), bargap=0.05,
                    showlegend=False, title='Column Overview', title_font=dict(size=24))

    fig.add_shape(type="rect",
        xref="paper", yref="paper",
        x0=-0.0597, y0=-0.0334, x1=1.0705, y1=1.0354, 
        line=dict(
            color="RoyalBlue",
            width=2,
        ),
    )

    time_hours = accidents_plot.Time.str.split(pat=':').apply(lambda x:float(x[0])+float(x[1])/60)
    fig.add_trace(go.Histogram(x=time_hours, histnorm='probability', marker=dict(color='royalblue')), row=1, col=1)
    fig.update_xaxes(title='Hour of the day', tickmode='array', tickvals=list(range(0,24)), fixedrange=True, showgrid=True, row=1, col=1)
    fig.update_yaxes(title='Probability of accident', showgrid=True, fixedrange=True, row=1, col=1)

    time_null_count = accidents_plot.Time.isnull().sum()
    fig.add_annotation(text=f'Null counts<br>{time_null_count} ({round(time_null_count/accidents_plot.Time.count()*100)}%)', x=0.4217, y=1, xref='paper', yref='paper',
                    showarrow=False, bgcolor='white', bordercolor='black', borderpad=2.4)

    for i in range(1, number_of_plots):
        add_plot_to_fig(fig, accidents_plot.iloc[:, i], p_placement=SETUP_placements[i], p_annotation_placement=SETUP_annotation_placements[i],
                        p_shorten=SETUP_shorten[i], p_cat=SETUP_cat[i], p_categoryorder=SETUP_categoryorder[i], p_order=SETUP_order[i],
                        p_range_multiplier=SETUP_range_multiplier[i], p_rename=SETUP_rename[i], p_tickvals=SETUP_tickvals[i])


    fig.add_annotation(x=0.06, y=0.994, xref='paper', yref='paper', text='Two spikes', showarrow=False, bgcolor='white', bordercolor='black', borderpad=2.4)
    fig.add_annotation(x=0.135, y=0.96, xref='paper', yref='paper', ax=-60, ay=-70, arrowhead=2)
    fig.add_annotation(x=0.082, y=0.972, xref='paper', yref='paper', text=f'+{round(349/183*100-100)}%', showarrow=False)
    fig.add_annotation(x=0.315, y=0.99, xref='paper', yref='paper', ax=-260, ay=0, arrowhead=2)
    fig.add_annotation(x=0.2, y=0.989, xref='paper', yref='paper', text=f'+{round(633/463*100-100)}%', showarrow=False)

    fig.add_hline(y=np.average(accidents_plot.Day_of_week.value_counts(normalize=True).values), line=dict(color='rgba(0, 0, 0, 0.25)', dash='dash'), row=1, col=3)

    fig.add_annotation(x=0.84, y=0.84, xref='paper', yref='paper', text=f'No Licence<br>{accidents_plot.Driving_experience.value_counts()["No Licence"]}',
                    ax=20, ay=-90, bordercolor='black', borderpad=2.4, bgcolor='white', arrowhead=2)

    fig.add_annotation(x=0.435, y=0.05, xref='paper', yref='paper', text='Changing lanes sums up to ~27%', showarrow=False, bgcolor='white', bordercolor='black', borderpad=2.4)
    fig.add_annotation(x=0.322, y=0.0452, xref='paper', yref='paper', ax=40, ay=-15)
    fig.add_annotation(x=0.341, y=0.0395, xref='paper', yref='paper', ax=23, ay=-28)

    return fig