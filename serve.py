#!/usr/bin/env python3
"""Μικρός server για το ElectroLab Suite (HTTP ή HTTPS).
Χρήση:
  python3 serve.py              -> http://localhost:8080  (δουλεύει ως PWA στον ίδιο υπολογιστή)
  python3 serve.py --https      -> https://<IP-του-υπολογιστή>:8443 (αυτο-υπογεγραμμένο πιστοποιητικό, για δοκιμή στο τοπικό δίκτυο)
Για ΠΡΑΓΜΑΤΙΚΟ έμπιστο HTTPS στο κινητό (εγκατάσταση PWA), τρέξε το http και άνοιξε σήραγγα:
  cloudflared tunnel --url http://localhost:8080
"""
import argparse, http.server, os, socket, ssl, subprocess

class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                      '.webmanifest': 'application/manifest+json', '.js': 'text/javascript'}
    def end_headers(self):
        if self.path.split('?')[0].endswith(('sw.js', 'index.html', '/')):
            self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1)); return s.getsockname()[0]
    except OSError:
        return '127.0.0.1'
    finally:
        s.close()

def make_cert(ip):
    if os.path.exists('cert.pem') and os.path.exists('key.pem'):
        return
    subprocess.check_call(['openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-nodes', '-days', '365',
                           '-keyout', 'key.pem', '-out', 'cert.pem', '-subj', '/CN=electrolab',
                           '-addext', f'subjectAltName=DNS:localhost,IP:127.0.0.1,IP:{ip}'])

ap = argparse.ArgumentParser()
ap.add_argument('--https', action='store_true')
ap.add_argument('--port', type=int)
a = ap.parse_args()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
ip = lan_ip()
port = a.port or (8443 if a.https else 8080)
srv = http.server.ThreadingHTTPServer(('0.0.0.0', port), Handler)
if a.https:
    make_cert(ip)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain('cert.pem', 'key.pem')
    srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
    print(f'HTTPS: https://{ip}:{port}  (ο browser θα προειδοποιήσει για το πιστοποιητικό)')
else:
    print(f'HTTP: http://localhost:{port}  ·  δίκτυο: http://{ip}:{port}')
print('Ctrl+C για έξοδο')
try:
    srv.serve_forever()
except KeyboardInterrupt:
    pass
