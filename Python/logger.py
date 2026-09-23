import serial
import time

# Configure the serial port
ser = serial.Serial('/dev/ttyUSB0', 500000)

print("Recording 10 seconds of heartbeat data...")

with open('heartbeat_data.csv', 'w') as f:
    # Write a simple CSV header
    f.write("adc_value\n") 
    
    # Record for exactly 10 seconds
    t_end = time.time() + 10 
    while time.time() < t_end:
        try:
            # Read the line, decode it, and strip invisible characters
            line = ser.readline().decode('utf-8').strip()
            if line.isdigit():
                f.write(line + '\n')
        except Exception:
            pass
            
print("Recording complete! Saved to heartbeat_data.csv")
ser.close()
