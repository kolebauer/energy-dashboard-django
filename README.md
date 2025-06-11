# Overview

EcoPulse is a web-based energy analytics dashboard designed to process and visualize timestamped energy usage data. The project simulates how an energy analyst or facility manager might monitor and investigate electricity usage trends within a facility. It features both basic statistics and more advanced anomaly detection logic.

This dashboard was created to sharpen my full-stack development skills using Django and to explore practical data analysis workflows with Python, `pandas`, and `plotly`.

The data used simulates building-level or system-level electricity usage sampled at regular intervals. It includes both high-resolution hourly readings and lower-resolution daily aggregates to reflect different monitoring scenarios. Data was formatted manually to resemble real-world sensor or meter logs.

To run the web app locally, install the dependencies below, then use the command `python manage.py runserver` and visit `http://127.0.0.1:8000` in your browser. The homepage will guide you to upload data and view statistics and visualizations.

[Software Demo Video (Work In Progress)](Work In Progress)

# Web Pages

- **Homepage (`/`)** – Introduces the app and links to the upload and visualization tools.
- **Basic Upload (`/upload_simple/`)** – Upload CSV with timestamped energy usage data and get:
  - Total Usage
  - Minimum and Maximum Usage
  - Average Load
  - Peak Hour
  - Weekday vs Weekend Comparison
- **Advanced Upload (`/upload_advanced/`)** – Upload aggregated daily CSVs and receive:
  - Daily Mean Usage Chart
  - Standard Deviation Chart
  - Automated Anomaly Detection Table

# Data Analysis Results

The app answers the following key questions:

- What is the total energy usage in the given time period?
- When is energy usage at its peak during the day?
- How does weekday usage compare to weekend usage?
- Are there any days with unusually high or low usage patterns?
- Can we visually identify trends or spikes in energy consumption?

These insights are calculated automatically upon CSV upload and displayed as dynamic HTML tables or interactive Plotly charts.

# Development Environment

- **IDE**: Visual Studio Code
- **Language**: Python 3.11
- **Framework**: Django 5.2
- **Frontend**: Bootstrap 5
- **Visualization**: Plotly (for interactive graphs)
- **Data Analysis**: Pandas (for CSV parsing and statistics)

# Useful Websites

* [Django Documentation](https://docs.djangoproject.com/en/5.2/)
* [Plotly for Python](https://plotly.com/python/)
* [RealPython Django Guide](https://realpython.com/tutorials/django/)
* [Pandas Documentation](https://pandas.pydata.org/docs/)

# Future Work

* Add persistent data storage using PostgreSQL or SQLite
* Enable filtering by date range or time of day
* Expand anomaly detection with user-tunable thresholds and advanced detection logic
* Support exportable PDF or CSV reports for each analysis
* Add authentication for multi-user support