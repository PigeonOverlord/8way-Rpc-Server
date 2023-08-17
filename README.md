
# XML-RPC Server Script Usage Documentation

##Prerequisites

Requires [TSduck](https://tsduck.io) installation

## Introduction:


This script implements an XML-RPC server for managing media streaming processes on a DTA-2115 8-way DekTec device. It allows clients to remotely start and stop media streams on different ports, as well as retrieve the status of each port's streaming process.

The script utilises the `xmlrpc.server` module from Python's standard library to create the XML-RPC server. It exposes three main functions: `play`, `stop`, and `get_port_status`.


## Server Configuration:


To configure the XML-RPC server to work within your network environment, you need to modify the values of the parameters to match your specific setup. Ensure that the IP address, port, and video folder paths are accurate and accessible to both the script and the clients that will be making requests.

### Configuration

![config](https://github.com/PigeonOverlord/8way-Rpc-Server/assets/85998646/d4ae82f6-d028-4314-aa5d-01bf4e8640ff)

*   **SERVER\_IP**: Specifies the IP address on which the XML-RPC server will listen for incoming requests. It should be set to the IP address of the machine where the script is running. Clients will connect to this address to send XML-RPC requests.
    

*   Use `ip address` on command line to check your IP address
    

*   **SERVER\_PORT**: The port number on which the XML-RPC server will listen. Clients will use this port number to establish connections and communicate with the server.
    
*   **MOUNT\_VIDEO\_FOLDER**: Path to a mounted video folder for streaming.
    
*   **LOCAL\_VIDEO\_FOLDER**: Path to a local video folder for streaming.
    



# Functions:

*   **play**: This function is used to start a media streaming process on a specified port. Clients can provide the port number, frequency, and video file name to initiate streaming. The function ensures that streams are started only on valid ports and handles cases where a port is already in use.
    
*   **stop**: Clients can call this function to stop a media streaming process on a specified port. The function gracefully terminates the stream on the given port, preventing any further streaming on that port until requested again.
    
*   **get\_port\_status**: This function allows clients to retrieve the status of all streaming ports. It returns a dictionary that indicates whether each port is running a stream and provides the process ID (PID) of the associated process if applicable.
    

## play

Starts a media streaming process on the specified port.

![play](https://github.com/PigeonOverlord/8way-Rpc-Server/assets/85998646/ae217d70-1de2-4696-93a1-b7abdfdb3625)


**Parameters:**

*   `port`: The port number (0-7) on which to start the stream.
    
*   `freq`: The frequency of the stream.
    
*   `videoFile`: The name of the video file without extension.
    

**Returns:**

*   Success: A message confirming the process start.
    
*   Port is invalid: A message indicating an invalid port number.
    
*   Port is already in use: A message indicating the port is already streaming.
    

## stop

Stops a media streaming process on the specified port.

![stop](https://github.com/PigeonOverlord/8way-Rpc-Server/assets/85998646/207197ec-137d-4509-a72c-96c14b68ac28)

**Parameters:**

*   `port`: The port number (0-7) on which to stop the stream.
    

**Returns:**

*   Success: A message confirming the process termination.
    
*   Port is invalid: A message indicating an invalid port number.
    
*   Port is not in use: A message indicating the port is not streaming.
    

## get\_port\_status

Retrieves the status of all streaming ports.

![port_status](https://github.com/PigeonOverlord/8way-Rpc-Server/assets/85998646/53e914e8-d283-496d-9b81-20911a46beaf)


**Returns:**

*   A dictionary containing the status of each port and its associated process PID (if running).
    



## Registering Functions

After defining the required functions, the script registers these functions on the XML-RPC server instance. This step makes the functions available for remote procedure calls from clients. Additionally, the script initiates the server to start processing incoming requests.

![function_register](https://github.com/PigeonOverlord/8way-Rpc-Server/assets/85998646/775dc945-1391-4812-8e2e-900f24cc770d)

*   The `register_function` method is called on the `server` instance for each function.
    
*   The first argument is the function to be registered.
    
*   The second argument is a string that represents the function's name as it will be exposed to clients during XML-RPC calls.
    

## Starting the Server

To start the server run the server script i.e:

`python3 rpcServer.py`

To start processing incoming XML-RPC requests, the script utilizes a `try` block to initiate the server and serve requests indefinitely. A graceful exit is implemented to handle a `KeyboardInterrupt` event (typically triggered by pressing `Ctrl + C`).

![server_start](https://github.com/PigeonOverlord/8way-Rpc-Server/assets/85998646/e63b5fde-d54f-4f24-9927-8af5e78ac820)

*   The `__name__` special variable is used to check if the script is being run as the main program.
    
*   If the script is executed directly (not imported as a module), the server initialization and serving block will be executed.
    
*   Within the `try` block:
    
    *   The message `'Serving..'` is printed to the console to indicate that the server is up and running.
        
    *   The `serve_forever` method of the `server` instance is called to continuously process incoming requests.
        
*   In the event of a `KeyboardInterrupt` (Ctrl+C), the `except KeyboardInterrupt` block:
    
    *   Prints the message `'Exiting'` to the console to indicate a graceful shutdown.
        


