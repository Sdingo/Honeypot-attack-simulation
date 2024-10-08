import socket
import random
import time
import logging

# Set up logging
logging.basicConfig(filename='attack_simulation.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to simulate different types of attacks
def simulate_attack(port):
    attack_types = [
        "SYN Flood",     # Flooding with SYN packets
        "UDP Flood",     # Flooding with UDP packets
        "HTTP GET Request",  # Normal HTTP requests
        "HTTP POST Request", # Simulating data submission
        "Connection Timeout"  # Simulating timeout scenarios
    ]
    
    for i in range(10):  # Simulate 10 connection attempts
        attack_type = random.choice(attack_types)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Random delay to simulate real-world scenarios
                time.sleep(random.uniform(0.1, 1.0))
                
                if attack_type == "SYN Flood":
                    # Simulating SYN flood
                    sock.connect(("127.0.0.1", port))
                    logging.info(f"Attempt {i + 1}: {attack_type} on port {port} successful!")
                    print(f"Connection attempt {i + 1} to port {port} successful!")
                
                elif attack_type in ["HTTP GET Request", "HTTP POST Request"]:
                    sock.connect(("127.0.0.1", port))
                    if attack_type == "HTTP GET Request":
                        request = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
                    else:
                        request = "POST /data HTTP/1.1\r\nHost: localhost\r\nContent-Length: 0\r\n\r\n"
                    sock.sendall(request.encode('utf-8'))
                    response = sock.recv(1024)
                    logging.info(f"Attempt {i + 1}: {attack_type} on port {port} - Response: {response.decode()}")
                    print(f"Connection attempt {i + 1} to port {port} - Response received!")
                
                elif attack_type == "UDP Flood":
                    # Simulating a UDP flood
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.sendto(b"Flooding UDP packet", ("127.0.0.1", port))
                    logging.info(f"Attempt {i + 1}: {attack_type} on port {port} sent!")
                    print(f"Connection attempt {i + 1} to port {port} sent UDP packet!")
                
                elif attack_type == "Connection Timeout":
                    # Simulating a connection timeout
                    sock.settimeout(0.1)  # Set a short timeout
                    sock.connect(("127.0.0.1", port))
                    logging.info(f"Attempt {i + 1}: {attack_type} on port {port} successful!")
                    print(f"Connection attempt {i + 1} to port {port} successful!")
                    
        except socket.error as e:
            logging.error(f"Attempt {i + 1}: {attack_type} on port {port} failed: {e}")
            print(f"Connection attempt {i + 1} to port {port} failed: {e}")

# Main function to run the attack simulation
def run_attack_simulation(ports):
    for port in ports:
        print(f"Starting attack simulation on port {port}...")
        simulate_attack(port)

if __name__ == "__main__":
    ports_to_test = [8080, 8081, 8082]  # Specify the ports to test
    run_attack_simulation(ports_to_test)
