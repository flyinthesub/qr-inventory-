import http.server
import ssl

PORT = 8443  # HTTPS port

handler = http.server.SimpleHTTPRequestHandler
httpd = http.server.HTTPServer(("0.0.0.0", PORT), handler)

# Use SSLContext instead of ssl.wrap_socket
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain("cert.pem")

httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print(f"Serving HTTPS on https://0.0.0.0:{PORT}")
httpd.serve_forever()
