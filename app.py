from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Classe para gerenciar Filas de atendimento
class FilaAtendimento:
    def __init__(self):
        self.fila = []
        self.proximo_numero = 1

    def gerar_senha(self):
        senha = self.proximo_numero
        self.fila.append(senha)
        self.proximo_numero += 1
        return senha
    
    def atender_cliente(self):
        if self.fila:
            return self.fila.pop(0)
        return None
    # listar todas as senhas (alunos vao fazer isso)

class RequisicaoHandler(BaseHTTPRequestHandler):
    fila_atendimento = FilaAtendimento()
    
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
    
    def do_POST(self):
        if self.path == "/gerar-senha":
            senha = self.fila_atendimento.gerar_senha()
            self._set_headers(201)
            self.wfile.write(json.dumps({"senha": senha}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"message": "Rota não encontrada."}).encode())
 
    def do_GET(self):
        if self.path == "/chamar-senha":
            senha = self.fila_atendimento.atender_cliente()
            if senha:
                self._set_headers(200)
                self.wfile.write(json.dumps({"senha": senha}).encode())
            else:
                self._set_headers(204)
                self.wfile.write(json.dumps({"message": "Não há senhas na fila."}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"message": "Rota não encontrada."}).encode())

def run():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, RequisicaoHandler)
    print("API rodando em http://localhost:8080")
    httpd.serve_forever()

if __name__ == "__main__":
    run()