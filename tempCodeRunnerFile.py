import tkinter as tk
from tkinter import messagebox
from sklearn.ensemble import IsolationForest
import pandas as pd
import random

# Load the data from the CSV file
data = pd.read_csv('/Users/kusumasurendrapaul/Downloads/CrimesOnWomenData.csv')

# Checking the first few rows of the dataset to understand its structure
print(data.head())

# Preprocessing data (we will focus on crime-related columns)
# For example, we can combine 'Rape' and 'DV' columns for the analysis
data['crime_rate'] = data[['Rape', 'DV']].sum(axis=1)  # Add up crime rates from relevant columns

# Fit an IsolationForest model to simulate anomaly detection
model = IsolationForest()
model.fit(data[['Rape', 'DV', 'crime_rate']])

# Dummy preventive measures based on crime rates and severity
def safety_measures(crime_rate, risk_level):
    if risk_level == "High":
        return "Avoid the area, try to stay in well-lit areas, and travel with others."
    elif risk_level == "Medium":
        return "Stay alert and avoid walking alone after dark."
    elif risk_level == "Low":
        return "The area is relatively safe, but always be cautious."
    return "No specific advice available."

# Function to calculate severity and provide assistance
def analyze_safety(state, issue_type):
    # Simulate some form of risk based on the state and crime rate
    state_data = data[data['State'].str.lower() == state.lower()]

    if state_data.empty:
        return "Sorry, I don't have data for that state."

    crime_rate = state_data['crime_rate'].values[0]
    
    # Assign risk level based on crime rate
    if crime_rate > 1000:  # Adjust threshold based on your dataset
        risk_level = "High"
    elif crime_rate > 500:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    # Provide details about the risk and safety measures
    safety_message = f"Crime Rate: {crime_rate:.2f}\nRisk Level: {risk_level}\n"
    safety_message += safety_measures(crime_rate, risk_level)
    
    return safety_message

# Function to process user queries
def process_query():
    user_input = entry.get()
    
    try:
        # Splitting the user input into state name and issue type (for simplicity, just state for now)
        parts = user_input.split(',')
        if len(parts) < 2:
            raise ValueError("Please provide both state and issue type.")
        
        state = parts[0].strip()
        issue_type = parts[1].strip()
        
        # Get safety analysis
        safety_message = analyze_safety(state, issue_type)
        
        # Display result in chat window
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"User: {user_input}\nBot: {safety_message}\n\n")
        chat_display.config(state=tk.DISABLED)
        entry.delete(0, tk.END)

    except Exception as e:
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"User: {user_input}\nBot: Sorry, I couldn't understand that.\n\n")
        chat_display.config(state=tk.DISABLED)
        entry.delete(0, tk.END)

# Initialize the GUI
root = tk.Tk()
root.title("Women Safety Analytics Chatbot")
root.geometry("500x500")

# Create the chat display area
chat_display = tk.Text(root, height=20, width=60, wrap=tk.WORD, state=tk.DISABLED)
chat_display.pack(padx=10, pady=10)

# Create the input field
entry = tk.Entry(root, width=60)
entry.pack(padx=10, pady=10)

# Create a send button
send_button = tk.Button(root, text="Send", width=20, command=process_query)
send_button.pack(pady=10)

# Run the chatbot interface
root.mainloop()
