from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import subprocess

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2')

# Server IP and port - change server IP accordingly
SERVER_IP = '192.168.10.162'
SERVER_PORT = 5000
# Video Path
MOUNT_VIDEO_FOLDER = "/mnt/PWstreams/"
LOCAL_VIDEO_FOLDER = "/home/rpcServer/singleservices/"

# Create an instance of SimpleXMLRPCServer
server = SimpleXMLRPCServer((SERVER_IP, SERVER_PORT), requestHandler=RequestHandler, allow_none=True)

# Dictionary to store the subprocess objects with port as keys
port_processes = {str(port): {'process': None, 'running': False} for port in range(8)}

# Function to start the media streaming process on the specified port
def play(port, freq, videoFile):
    port_str = str(port)

    if port_str not in port_processes:
        return f"Port {port_str} is invalid. Please choose port 0-7"

    if port_processes[port_str]['running']:
        return "Port is already in use."
        
    # video_path = f"{MOUNT_VIDEO_FOLDER}{videoFile}.ts" # mounted folder
    video_path = f"{LOCAL_VIDEO_FOLDER}{videoFile}.ts" # local folder

    args = [
        "/usr/bin/tsp",   # Path to the tsp executable
        "--verbose",       # Verbose mode enabled
        "-I", "file",      # Input mode set to 'file'
        video_path,        # Input video file path
        "--infinite",      # Streaming is infinite
        #"-P", "regulate",
        "-O", "dektec",    # Output mode set to 'dektec'
        "-c", port_str,    # Output channel (port) number
        "--modulation", "DVB-T",    # Modulation set to DVB-T
        "--frequency", str(freq)    # Frequency of the stream
    ]

    # Start the subprocess using Popen
    test_process = subprocess.Popen(args)
    port_processes[port_str]['process'] = test_process
    port_processes[port_str]['running'] = True

    return f"Port {port_str} process started successfully."


# Function to stop the media streaming process on the specified port
def stop(port):
    port_str = str(port)
    if port_str not in port_processes:
        return f"Port {port_str} is invalid. Please choose port 0-7"

    if not port_processes[port_str]['running']:
        return f"Port {port_str} is not in use."

    test_process = port_processes[port_str]['process']
    if test_process:
        # Terminate the subprocess
        test_process.terminate()
        port_processes[port_str]['process'] = None
        port_processes[port_str]['running'] = False
        return f"Port {port_str} process terminated successfully."


# Function to get the status of all ports
def get_port_status():
    # Convert the port_processes dictionary to a serializable format
    status_dict = {
        port: {
            'running': info['running'],
            'process_pid': info['process'].pid if info['process'] else None
        } for port, info in port_processes.items()
    }
    return status_dict


# Register the functions on the server
server.register_function(play, 'play')  
server.register_function(stop, 'stop')  
server.register_function(get_port_status, 'get_port_status')  


# Start serving the XML-RPC server
if __name__ == '__main__':
    try:
        print('Serving..')
        server.serve_forever()
    except KeyboardInterrupt:
        print('Exiting')  # Handle KeyboardInterrupt to gracefully exit the server on Ctrl+C
