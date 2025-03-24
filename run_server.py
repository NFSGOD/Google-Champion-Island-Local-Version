import http.server
import socketserver
import webbrowser
import os
import subprocess
import sys

PORT = 8000  # Change this if needed
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

def kill_existing_process(port):
    """Find and kill any process using the specified port."""
    try:
        result = subprocess.run(["netstat", "-ano"], capture_output=True, text=True, check=True)
        for line in result.stdout.splitlines():
            if f":{port}" in line:
                pid = line.strip().split()[-1]
                if pid.isdigit():
                    print(f"🔴 Killing process {pid} using port {port}...")
                    subprocess.run(["taskkill", "/PID", pid, "/F"], check=True)
                    print("✅ Port freed successfully!")
    except subprocess.CalledProcessError:
        print("⚠️ No existing process found on the port.")

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/shutdown":
            print("🔴 Received shutdown signal. Stopping server...")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Server shutting down")
            shutdown_server()
        else:
            super().do_GET()

def shutdown_server():
    """Stops the server and exits the script."""
    global httpd
    print("✅ Shutting down the server...")
    httpd.server_close()  # Close the server
    sys.exit(0)  # Exit the script

# Kill any process using the port before starting
kill_existing_process(PORT)

# Change working directory to the project folder
os.chdir(PROJECT_DIR)

# Start the server
httpd = socketserver.TCPServer(("", PORT), Handler)
print(f"🚀 Serving at http://localhost:{PORT}")

# Open the game in the default web browser
webbrowser.open(f"http://localhost:{PORT}/index.html")

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    shutdown_server()
