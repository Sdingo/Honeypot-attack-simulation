import socket
import threading
import time
import requests
from collections import defaultdict

# Function to get geolocation based on IP address
def get_geolocation(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        return response.json()
    except Exception as e:
        print(f"Geolocation error: {e}")
        return {}

# Function to generate dynamic responses based on previous interactions
def generate_dynamic_response(interaction_count):
    responses = [
        "Hello! How can I assist you today?",
        "Welcome back! Do you have more questions?",
        "It's great to see you again! What can I help with?",
        "Hi there! What would you like to know?",
        "Thanks for reaching out again! How can I assist?"
    ]
    
    if interaction_count < len(responses):
        return responses[interaction_count]
    else:
        return "I'm here to help with anything you need!"

# Function to analyze traffic and flag suspicious activity
def analyze_traffic(ip):
    # Simple threshold for suspicious activity
    threshold = 5
    ip_counter[ip] += 1

    if ip_counter[ip] > threshold:
        print(f"[ALERT] Suspicious activity detected from {ip}! Number of connections: {ip_counter[ip]}")

# Function to handle incoming connections
def handle_client(conn, addr, interaction_count):
    print(f"Connection from {addr} has been established!")

    # Get geolocation
    geolocation = get_geolocation(addr[0])
    print(f"Geolocation data: {geolocation}")

    # Analyze traffic for the current IP
    analyze_traffic(addr[0])

    # Generate a dynamic response
    response_message = generate_dynamic_response(interaction_count)
    conn.sendall(response_message.encode('utf-8') + b'\n')

    # Simulate some processing
    time.sleep(1)
    conn.close()

# Global variable to track IP connection counts
ip_counter = defaultdict(int)

# Modify the start_honeypot function to keep track of interactions
def start_honeypot():
    host = '127.0.0.1'
    port = 8080
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()

    print(f"Honeypot is listening on port {port}...")
    interaction_count = 0  # Counter for interactions

    while True:
        conn, addr = sock.accept()
        # Pass the interaction count to the handle_client function
        client_thread = threading.Thread(target=handle_client, args=(conn, addr, interaction_count))
        client_thread.start()
        interaction_count += 1  # Increment the interaction count

if __name__ == "__main__":
    start_honeypot()
