import pandas as pd
import plotly.graph_objects as go

def add_plot_to_fig(figure, p_tab, record_count, p_placement=(), p_annotation_placement=(1,1), p_shorten=0, p_cat=(),
                    p_categoryorder='', p_order=[], p_tickvals=[], p_range_multiplier=1.25, p_rename=[]):
    
    # standardizing the columns names
    p_tab = p_tab.rename('categories')

    # calculating value_counts and shortening categorical values if needed
    if not p_shorten:
        probabilities = p_tab[(p_tab != 'na') & (p_tab != 'unknown') & (p_tab != 'Unknown')].value_counts(normalize=True).reset_index()
    else:
        probabilities = p_tab[(p_tab != 'na') & (p_tab != 'unknown') & (p_tab != 'Unknown')].value_counts(normalize=True).reset_index().assign(
            categories=lambda x: x['categories'].apply(lambda val: val if len(val)<=p_shorten else val[:p_shorten]+'...'))
        
    # concatening a given value if needed
    if p_cat:
        probabilities = pd.concat([probabilities, pd.DataFrame({'categories': [p_cat[0]], 'proportion': [p_cat[1]]})], ignore_index=True)

    # renaming the categorical values if needed
    if p_rename:
        probabilities['categories'] = p_rename

    # creating a bar chart
    figure.add_trace(go.Bar(x=probabilities['categories'], y=probabilities['proportion'], texttemplate='%{y}',
                         textposition='outside', textfont=dict(size=10), marker=dict(color='royalblue')), row=p_placement[0], col=p_placement[1])

    # preparing arguments to be used inside .update_xaxes
    update_xaxes_kwargs = {}
    update_xaxes_arguments = [
        ('fixedrange', True),
        ('tickfont', dict(size=10)),
        ('row', p_placement[0]),
        ('col', p_placement[1]),
        ('categoryorder', p_categoryorder),
        ('categoryarray', p_order)]
    if p_tickvals:
        update_xaxes_arguments.append(('tickvals', probabilities['categories']))
    for key, value in update_xaxes_arguments:
        if key=='tickvals' or value:
            update_xaxes_kwargs[key] = value

    # updating xaxes with prepared kwargs
    figure.update_xaxes(**update_xaxes_kwargs)

    # updating yaxes with set and given values
    figure.update_yaxes(fixedrange=True, row=p_placement[0], col=p_placement[1], showgrid=True, title='Probability of accident',
                        tickformat='.2f', range=[0, max(probabilities['proportion']) * p_range_multiplier])

    # adding an annotation with the null count
    null_count = p_tab.isnull().sum() + p_tab[p_tab == 'na'].count() + p_tab[p_tab == 'unknown'].count() + p_tab[p_tab == 'Unknown'].count()
    null_percent = round(null_count/record_count*100)
    figure.add_annotation(text=f' Null counts <br>{null_count} ({null_percent}%)', x=p_annotation_placement[0], y=p_annotation_placement[1],
                          xref='paper', yref='paper', showarrow=False, bgcolor='white', bordercolor=('black' if null_percent < 20 else 'red'), borderpad=2.4)