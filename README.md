# Overview

This web app is an Energy Monitoring Dashboard designed to help users upload and visualize timestamped energy usage data. I created this project to improve my understanding of full-stack web development using Django, particularly in building dynamic, data-driven interfaces.

To run the web app locally, install the dependencies below, then use the command `python manage.py runserver` and visit `http://127.0.0.1:8000` in your browser. The homepage will guide you to upload data and view statistics and visualizations.

The purpose of this software is to simulate how an energy analyst or facility manager might inspect electricity usage trends over time based on sensor data or internal reports.

[Software Demo Video](DON'T FORGET TO ADD ME)

# Web Pages

- **Homepage (`/`)** – Introduces the app and links to the upload and visualization pages.
- **Upload Page (`/upload/`)** – Allows users to upload a `.csv` file with energy usage data. After uploading, it dynamically calculates and displays:
  - Total Usage
  - Minimum and Maximum Values
  - Average Load
- **Visualization Page (`/visualize/`)** – Generates and displays an interactive Plotly line chart showing energy usage trends over time. This graph is dynamically rendered using the uploaded CSV file.

# Development Environment

- **IDE**: Visual Studio Code
- **Language**: Python 3.11
- **Framework**: Django 5.2
- **Libraries**:
  - `pandas` – for CSV parsing and data analysis
  - `plotly` – for creating interactive graphs

# Useful Websites

* [Django Documentation](https://docs.djangoproject.com/en/5.2/)
* [Plotly for Python](https://plotly.com/python/)
* [RealPython Django Guide](https://realpython.com/tutorials/django/)

# Future Work

* Add database integration to persist uploads
* Include error handling for malformed or empty CSV files
* Add support for time range filtering and usage anomaly detection