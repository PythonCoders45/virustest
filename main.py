import tkinter as tk
import socket
import os
import time

# --- 1. CONFIGURATION VARIABLES ---
amount_of_windows = 2      # Total windows to display (Root + Toplevels)
IP_REPEAT_COUNT = 10       # How many times the IP address is repeated in the file
FILE_CREATION_INTERVAL = 1000 # Time in milliseconds between file creations (1000 = 1 second)
FILE_COUNTER = 0           # Global counter for unique file naming

# --- 2. FUNCTION TO FIND IP ADDRESS ---
def find_local_ip():
    """Finds and returns the local IP address of the computer."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80)) 
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception:
        return "Not Connected (IP not found)"

# --- 3. FUNCTION TO CONTINUOUSLY CREATE FILES ---
def create_ip_file_continuously(root, ip_address, repeat_count):
    """
    Creates a new .txt file and schedules itself to run again.
    This simulates continuous file creation.
    """
    global FILE_COUNTER
    FILE_COUNTER += 1
    
    filename = f"ip_log_{FILE_COUNTER}.txt"
    
    try:
        # Create the content: IP address repeated multiple times
        ip_content = f"{ip_address}\n" * repeat_count
        
        # Add a timestamp and file info
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        content = f"--- Logged on: {timestamp} ---\nFile Number: {FILE_COUNTER}\n\n{ip_content}"
        
        # Write the file to your computer's local directory
        with open(filename, 'w') as f:
            f.write(content)
            
        print(f"Created file: {filename}")
        
    except Exception as e:
        print(f"Error writing file: {e}")
        
    # --- The "Continuous" part: Schedule this function to run again ---
    # We schedule this function to run again after the defined interval
    root.after(FILE_CREATION_INTERVAL, lambda: create_ip_file_continuously(root, ip_address, repeat_count))


# --- 4. FUNCTION TO CREATE ALL WINDOWS AND START THE PROCESS ---
def create_app_windows(num_windows):
    """
    Creates the main window(s) and initiates the continuous file creation loop.
    """
    if num_windows < 1:
        print("Error: The number of windows must be 1 or greater.")
        return

    # Find the IP address ONCE
    ip_to_display = find_local_ip()
    display_text = f"IP: {ip_to_display}"

    # --- Create the Primary Window (Root) ---
    root = tk.Tk()
    root.title(f"Window 1 (Main) - Total: {num_windows}")
    root.geometry("350x120+50+50") 

    main_label = tk.Label(root, text="Continuous File Creation Active!", font=("Arial", 14, "bold"))
    main_label.pack(pady=5)
    
    ip_label = tk.Label(root, text=display_text, font=("Arial", 12))
    ip_label.pack(pady=5)
    
    # --- Create Secondary Windows (Toplevel) ---
    for i in range(2, num_windows + 1):
        offset = i * 40
        secondary_window = tk.Toplevel(root)
        secondary_window.title(f"Window {i} (Secondary)")
        secondary_window.geometry(f"300x100+{50 + offset}+{50 + offset}")
        secondary_label = tk.Label(secondary_window, text=display_text, font=("Arial", 12))
        secondary_label.pack(pady=35)

    # --- START THE CONTINUOUS FILE CREATION LOOP ---
    print("\n--- Starting Continuous File Creation ---\n")
    create_ip_file_continuously(root, ip_to_display, IP_REPEAT_COUNT)

    # --- Start the Application ---
    root.mainloop()


# --- Program Execution ---
if __name__ == "__main__":
    create_app_windows(amount_of_windows)
