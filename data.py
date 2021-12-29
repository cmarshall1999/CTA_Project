# Import Libraries
import pandas as pd
import numpy as np

# Plotly libraries
import plotly.express as px
import plotly.graph_objects as go

# Load Data
def getRuns():
    """
    Import and parse runs data into necessary data frames

    Output:
        parsed delay, headway, and runtime data
    """
    runs = pd.DataFrame()

    for i in range(34, 49):
        day = pd.read_excel('data/PublicSchedule.xlsx', sheet_name = i)
        
        data = np.array(day.loc[(day.loc[day['Unnamed: 0'].isna()].index[1]+1):, :])
        columns = list(day.loc[day.loc[day['Unnamed: 0'].isna()].index[1], :])
        df = pd.DataFrame(data = data, columns = columns)
        df = df.loc[:, df.columns.notnull()]

        runs = pd.concat([runs, df])
        runs = runs.reset_index(drop=True)
        runs = runs.replace(' ', np.nan)
        
        
    delays = runs.iloc[:, :16]
    headways = runs.iloc[:, 16:32]
    times = pd.concat([runs.iloc[:,0], runs.iloc[:, 32:]], axis = 1)

    return delays, headways, times

# Analysis Helpers
def getStats(df):
    """
    Return descriptive statistics table for dataframe 
    """
    return df.describe().round(1)

# Make Graphs
def showDist(df):
    # TODO: ADD TITLE AND AXIS LABELS
    """
    Create histogram for the distribution of a statistic at each station
    """
    fig = go.Figure()

    df_stats = getStats(df)

    for col in df_stats.columns:
        fig.add_trace(go.Histogram(x=df[f'{col}'], name = f'{col}'))

    # Overlay both histograms
    fig.update_layout(barmode='overlay')
    # Reduce opacity to see both histograms
    fig.update_traces(opacity=0.75)
    
    return fig

def showDelayProp(df):
    # TODO: Add trendlines
    # TODO: ADD TITLE AND AXIS LABELS
    """
    Creates viz of delay prop based on initial delay status
    """

    df_stats = getStats(df)

    x = np.array(df_stats.columns)
    all_runs = np.array(df.mean(numeric_only=True))
    delay_runs = np.array(df[df['Leave Linden'] >= 3].mean(numeric_only=True))
    early_runs = np.array(df[df['Leave Linden'] <= -3].mean(numeric_only=True))
    ontime_runs = np.array(df[(df['Leave Linden'] <= 3)&(df['Leave Linden'] >= -3)].mean(numeric_only=True))

    # Create traces
    d_prop_fig = go.Figure()

    d_prop_fig.add_trace(go.Scatter(x=x, y=all_runs,
                        mode='lines+markers',
                        name='all_runs'))
    d_prop_fig.add_trace(go.Scatter(x=x, y=delay_runs,
                        mode='lines+markers',
                        name='delay_runs'))
    d_prop_fig.add_trace(go.Scatter(x=x, y=early_runs,
                        mode='lines+markers',
                        name='early_runs'))
    d_prop_fig.add_trace(go.Scatter(x=x, y=ontime_runs,
                        mode='lines+markers',
                        name='ontime_runs'))

    return d_prop_fig

def showArrivalDelays(delays):
    arrival_delays = delays[delays['Linden'] > 5].dropna()
    
    # TODO: Clean up incomplete runs
    # TODO: rename runs

    delay_stats = getStats(delays)

    x = np.array(delay_stats.columns)

    # for i,row in arrival_delays.iterrows():
    np_arrival_delays = np.array(arrival_delays.iloc[:,1:])

    d_arr_fig = go.Figure()

    for run in np_arrival_delays:
        d_arr_fig.add_trace(go.Scatter(x=x, y=run,
                        mode='lines+markers',
                        name='all_runs'))

    return d_arr_fig

