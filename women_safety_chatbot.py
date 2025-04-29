import tkinter as tk
from tkinter import messagebox
import requests
import pandas as pd

# Load the crime dataset (replace with your actual path)
data = pd.read_csv('/Users/kusumasurendrapaul/Desktop/Womenmain/CrimesOnWomen.csv')

# Function to categorize crime rate into High, Medium, or Low
def categorize_crime_rate(crime_rate):
    if crime_rate > 1000:
        return "High"
    elif 500 <= crime_rate <= 1000:
        return "Medium"
    else:
        return "Low"

# Function to calculate the crime rate based on the dataset
def calculate_crime_rate(state, crime_type):
    # Filter data for the specific state
    state_data = data[data['State'].str.lower() == state.lower()]
    
    if state_data.empty:
        return "No crime data available for this state."
    
    # Assuming the dataset has columns 'Rape', 'Eve Teasing', 'Murder', 'Robbery', 'Theft', 'Domestic Violence', 'Waiting Time'
def calculate_crime_rate(state, crime_type):
    # Filter data for the specific state
    state_data = data[data['State'].str.lower() == state.lower()]
    
    if state_data.empty:
        return "No crime data available for this state."
    
    # Crime type logic
    crime_type = crime_type.lower()
    
    if crime_type == "rape":
        crime_rate = state_data['Rape'].values[0]
    elif crime_type == "eve teasing":
        crime_rate = state_data['Eve Teasing'].values[0]
    elif crime_type == "murder":
        crime_rate = state_data['Murder'].values[0]
    elif crime_type == "robbery":
        crime_rate = state_data['Robbery'].values[0]
    elif crime_type == "theft":
        crime_rate = state_data['Theft'].values[0]
    elif crime_type == "domestic violence":
        crime_rate = state_data['Domestic Violence'].values[0]
    elif crime_type == "waiting time":
        crime_rate = state_data['Waiting Time'].values[0]
    else:
        # If the crime type is not one of the specified, sum all the relevant columns
        crime_rate = state_data[['Rape', 'Eve Teasing', 'Murder', 'Robbery', 'Theft', 'Domestic Violence']].sum(axis=1).values[0]
    
    # Categorize crime rate as High, Medium, or Low
    category = categorize_crime_rate(crime_rate)
    
    return f"Crime Rate: {crime_rate} (Category: {category})"

# Function to fetch live crime news using NewsAPI
def fetch_crime_news(crime_type, state):
    api_key = 'your_newsapi_key'  # Replace with your NewsAPI key
    url = f'https://newsapi.org/v2/everything?q={crime_type}+{state}&apiKey={api_key}&language=en&pageSize=5'
    
    try:
        response = requests.get(url)
        news_data = response.json()
        
        if news_data["status"] == "ok" and news_data["totalResults"] > 0:
            articles = news_data["articles"][:5]  # Get top 5 articles
            news_list = "\n".join([f"{article['title']} - {article['description']}" for article in articles])
        else:
            news_list = f"No recent crime news found for {crime_type} in {state}. Here's some general information:\n\n" \
                        "1. A rise in crime rates in urban areas has been reported across India.\n" \
                        "2. Authorities are taking steps to combat increasing criminal activity."
        
    except Exception as e:
        news_list = f"Error fetching crime news: {str(e)}"
    
    return news_list

# Dummy safety tips and emergency contacts
def safety_measures():
    safety_message = """
    Safety Tips:
    1. Stay vigilant and avoid isolated areas.
    2. If you feel threatened, alert authorities immediately.
    3. Keep your phone charged and easily accessible.

    Emergency Contacts:
    Police: 100
    Women Helpline: 1091
    Ambulance: 108
    """
    return safety_message

# Function to analyze safety and provide analytics
def analyze_safety(state, issue_type):
    # Get crime rate
    crime_message = calculate_crime_rate(state, issue_type)
    
    if "No crime data" in crime_message:
        return crime_message  # If no data is found, return error message

    # Get live news based on the crime type and state
    crime_news = fetch_crime_news(issue_type, state)
    
    # Prepare the safety measures and emergency contacts
    safety_message = safety_measures()
    
    # Prepare full message combining crime rate, news, and safety tips
    full_message = f"Crime Type: {issue_type}\nState: {state}\n\n{crime_message}\n\n{crime_news}\n\n{safety_message}"
    return full_message

# Function to process user queries
def process_query():
    user_input = entry.get()
    
    try:
        # Split the user input by comma to get state and crime type
        parts = user_input.split(',')
        if len(parts) < 2:
            raise ValueError("Please provide both state and issue type.")
        
        state = parts[0].strip()  # Extract the state
        issue_type = parts[1].strip()  # Extract the crime type
        
        # Get safety analysis and crime news
        safety_message = analyze_safety(state, issue_type)
        
        # Display result in chat window
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"User: {user_input}\nBot: {safety_message}\n\n")
        chat_display.config(state=tk.DISABLED)
        entry.delete(0, tk.END)

    except Exception as e:
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"User: {user_input}\nBot: Sorry, I couldn't understand that. Please follow the format: State, Crime Type.\n\n")
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

# Show initial greeting
chat_display.config(state=tk.NORMAL)
chat_display.insert(tk.END, "Bot: Hi, how can I help you?\n\n")
chat_display.config(state=tk.DISABLED)

# Run the chatbot interface
root.mainloop()
