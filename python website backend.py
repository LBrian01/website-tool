import http.server
import socketserver
import json
import datetime

# Get the port number as input
h = int(input("Port number:"))

# Custom request handler class, inheriting from SimpleHTTPRequestHandler
class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    
    # Handle GET requests
    def do_GET(self):
        # Get client IP address and access time
        client_ip = self.client_address[0]
        access_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Get accessed page path
        page_path = self.path
        
        # Construct data to write into the file
        log_entry = f"IP: {client_ip} - Time: {access_time} - Page: {page_path}\n"
        
        # Write data into the FAR.txt file
        with open('FAR.txt', 'a') as f:
            f.write(log_entry)
        
        # Call the parent class's do_GET method to continue serving file content
        http.server.SimpleHTTPRequestHandler.do_GET(self)

    # Handle POST requests
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        folder_path = data['folderPath']
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Folder processed successfully')

# Define the port number to listen on
PORT = h

# Create HTTP server, bind to specified address and port
handler = SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), handler)

# Print server start information
print("Server started at localhost:" + str(PORT))

# Keep the server running, accepting and handling requests
httpd.serve_forever()
