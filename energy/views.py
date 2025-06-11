from django.shortcuts import render
import pandas as pd
import plotly.express as px
from django.core.files.storage import FileSystemStorage
import os

# Home page route
def home(request):
    return render(request, 'energy/home.html')

# Upload for simple analysis - shows basic stats and graphs
def upload_simple(request):
    context = {}

    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)
        file_path = fs.path(filename)

        try:
            df = pd.read_csv(file_path, parse_dates=['timestamp'])
            df = df.sort_values('timestamp')

            # Summary stats
            context['total'] = df['usage'].sum()
            context['max'] = df['usage'].max()
            context['min'] = df['usage'].min()
            context['avg'] = round(df['usage'].mean(), 2)
            context['data_loaded'] = True

            # Extra stats
            df['hour'] = df['timestamp'].dt.hour
            #df['weekday'] = df['timestamp'].dt.dayofweek
            context['peak_hour'] = df.groupby('hour')['usage'].mean().idxmax()
            #context['weekday_avg'] = round(df[df['weekday'] < 5]['usage'].mean(), 2)
            #context['weekend_avg'] = round(df[df['weekday'] >= 5]['usage'].mean(), 2)

            request.session['csv_path'] = file_path
            request.session['analysis_type'] = 'simple'

        except Exception as e:
            context['error'] = f"Error processing file: {e}"

    return render(request, 'energy/upload_simple.html', context)

# Upload for advanced analysis - shows statistical breakdown and anomaly detection
def upload_advanced(request):
    context = {}

    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)
        file_path = fs.path(filename)

        try:
            pd.read_csv(file_path, parse_dates=['timestamp'])  # validate format
            request.session['csv_path'] = file_path
            request.session['analysis_type'] = 'advanced'
            return analyze(request)

        except Exception as e:
            context['error'] = f"Error processing file: {e}"

    return render(request, 'energy/upload_advanced.html', context)

# Visualize the uploaded CSV with basic line and bar charts
def visualize(request):
    file_path = request.session.get('csv_path')
    context = {}

    if file_path:
        try:
            df = pd.read_csv(file_path, parse_dates=['timestamp'])
            df = df.sort_values('timestamp')

            fig_line = px.line(df, x='timestamp', y='usage', title='Energy Usage Over Time')
            context['chart_line'] = fig_line.to_html(full_html=False)

            df['hour'] = df['timestamp'].dt.hour
            hourly_avg = df.groupby('hour')['usage'].mean().reset_index()
            fig_bar = px.bar(hourly_avg, x='hour', y='usage', title='Average Hourly Usage')
            context['chart_bar'] = fig_bar.to_html(full_html=False)

        except Exception as e:
            context['error'] = f"Error generating chart: {e}"
    else:
        context['error'] = "No CSV uploaded yet."

    return render(request, 'energy/visualize.html', context)

# Advanced statistical analysis with anomaly detection
def analyze(request):
    context = {}
    file_path = request.session.get('csv_path')

    if not file_path or not os.path.exists(file_path):
        context['error'] = "No valid CSV file found."
        return render(request, 'energy/analyze.html', context)

    try:
        df = pd.read_csv(file_path, parse_dates=['timestamp'])
        df = df.sort_values('timestamp')

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        df['hour'] = df['timestamp'].dt.hour

        # --- Daily Averages ---
        daily_avg = df.groupby('date')['usage'].mean().reset_index(name='mean')
        daily_avg['date'] = pd.to_datetime(daily_avg['date'])
        fig_daily_avg = px.line(daily_avg, x='date', y='mean', title='Daily Average Usage')

        # --- Daily Std Dev ---
        daily_std = df.groupby('date')['usage'].std().reset_index(name='std')
        daily_std['date'] = pd.to_datetime(daily_std['date'])
        fig_daily_std = px.line(daily_std, x='date', y='std', title='Daily Usage Std Dev')

        # --- Hourly Mean/Variance ---
        hourly = df.groupby('hour')['usage'].agg(['mean', 'var']).reset_index()
        hourly_long = pd.melt(hourly, id_vars='hour', value_vars=['mean', 'var'],
                              var_name='variable', value_name='value')
        fig_hourly = px.line(hourly_long, x='hour', y='value', color='variable', title='Hourly Avg & Variance')

        # --- Anomaly Detection ---
        global_avg = df['usage'].mean()
        threshold = 25  # fixed deviation threshold
        anomaly_df = daily_avg.copy()
        anomaly_df['status'] = anomaly_df['mean'].apply(
            lambda x: 'ANOMALY DETECTED' if abs(x - global_avg) > threshold else 'OKAY'
        )

        anomaly_table = [
            {'date': row['date'].strftime('%Y-%m-%d'), 'mean': round(row['mean'], 2), 'status': row['status']}
            for _, row in anomaly_df.iterrows()
        ]

        # --- Add to context ---
        context['chart_summary'] = fig_daily_avg.to_html(full_html=False)
        context['chart_corr'] = fig_daily_std.to_html(full_html=False)
        context['chart_hourly'] = fig_hourly.to_html(full_html=False)
        context['daily_avg'] = round(global_avg, 2)
        context['daily_std'] = round(df['usage'].std(), 2)
        context['anomaly_table'] = anomaly_table

    except Exception as e:
        context['error'] = f"Data analysis failed: {e}"

    return render(request, 'energy/analyze.html', context)