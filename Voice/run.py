# Launch an http server on localhost using a random port to serve files from
# the current working folder. Automatically open a web browser pointed at the
# root url as a convenience.

from http.server import SimpleHTTPRequestHandler
from http.server import HTTPServer
import webbrowser

# Create a localhost server, specify port 0 so it will pick one for us.
httpd = HTTPServer(("localhost", 0), SimpleHTTPRequestHandler)
print("Server started on port: " + str(httpd.server_port))

# Open the browser; if index.html exists it will be opened, otherwise the user
# will get a directory listing.
webbrowser.open_new_tab("http://localhost:" + str(httpd.server_port))
httpd.serve_forever()