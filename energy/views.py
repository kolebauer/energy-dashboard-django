from django.shortcuts import render
import pandas as pd
import plotly.express as px
from django.core.files.storage import FileSystemStorage

# Renders the homepage with intro and navigation
def home(request):
    return render(request, 'energy/home.html')

# Handles file upload, parses CSV, and computes usage stats
def upload_csv(request):
    context = {}

    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']

        # Save the uploaded file to the local filesystem
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)
        file_path = fs.path(filename)

        try:
            # Load CSV using pandas
            df = pd.read_csv(file_path, parse_dates=['timestamp'])
            df = df.sort_values('timestamp')

            # Calculate statistics
            context['total'] = df['usage'].sum()
            context['max'] = df['usage'].max()
            context['min'] = df['usage'].min()
            context['avg'] = round(df['usage'].mean(), 2)
            context['data_loaded'] = True

            # Store file path in session for chart generation
            request.session['csv_path'] = file_path

        except Exception as e:
            context['error'] = f"Error processing file: {e}"

    return render(request, 'energy/upload.html', context)

# Generates Plotly line chart from uploaded CSV data
def visualize(request):
    file_path = request.session.get('csv_path')
    context = {}

    if file_path:
        try:
            # Reload CSV and sort it
            df = pd.read_csv(file_path, parse_dates=['timestamp'])
            df = df.sort_values('timestamp')

            # Create Plotly line chart
            fig = px.line(df, x='timestamp', y='usage', title='Energy Usage Over Time')
            chart_html = fig.to_html(full_html=False)

            # Embed chart HTML in context
            context['chart'] = chart_html

        except Exception as e:
            context['error'] = f"Error generating chart: {e}"
    else:
        context['error'] = "No CSV uploaded yet."

    return render(request, 'energy/visualize.html', context)
