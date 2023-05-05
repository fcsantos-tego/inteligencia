#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import sys

def write_log(message, log_file_path):
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"{datetime.now()}: {message}\n")

api_token = "a8d83bcc-5d05-44ed-be76-cd872d880dd2"

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {api_token}"
}

url = "https://api.movidesk.com/public/v1/tickets"

# Calculate the date 30 days ago
date_30_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%dT00:00:00')

# Add a filter to the request to get only tickets created in the last 30 days
params = {
    "$filter": f"createdDate ge {date_30_days_ago}",
    "$select": "lifetimeWorkingTime"
}

response = requests.get(url, headers=headers, params=params)

if '__file__' in globals():
    script_directory = os.path.dirname(os.path.abspath(__file__))
else:
    script_directory = os.path.abspath('')

log_file_path = os.path.join(script_directory, "log.txt")

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)
    
    # Save DataFrame to an Excel file in the same folder as the script
    excel_filename = os.path.join(script_directory, "movidesk_data.xlsx")
    df.to_excel(excel_filename, index=False)
    
    success_message = f"Data successfully saved to {excel_filename}"
    print(success_message)
    write_log(success_message, log_file_path)
else:
    error_message = f"Error {response.status_code}: {response.text}"
    print(error_message)
    write_log(error_message, log_file_path)


# In[ ]:




