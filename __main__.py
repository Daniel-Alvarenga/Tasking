import json
import argparse
import hashlib
from datetime import datetime, timedelta

class TaskManager:
    def __init__(self):
        self.dados = self.carregar_dados()
        self.usuario_logado = None
        self.inicializar_logins()
        if self.dados['logins'] and 'usuario' in self.dados['logins'][-1]:
            ultimo_login = self.dados['logins'][-1]
            data_hora_login = datetime.fromisoformat(ultimo_login['data_hora'])
            agora = datetime.now()
            limite_tempo = agora - timedelta(hours=1)

            if data_hora_login >= limite_tempo:
                self.usuario_logado = ultimo_login['usuario']

    def carregar_dados(self):
        try:
            with open('dados.json', 'r') as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            dados = {'usuarios': {}, 'tarefas': {}, 'logins': []}
        return dados

    def salvar_dados(self):
        with open('dados.json', 'w') as arquivo:
            json.dump(self.dados, arquivo)

    def criar_hash(self, senha):
        sha256 = hashlib.sha256()
        sha256.update(senha.encode('utf-8'))
        return sha256.hexdigest()

    def cadastrar_usuario(self, nome, senha):
        if nome in self.dados['usuarios']:
            print(f"Usuário '{nome}' já existe.")
        else:
            senha_hash = self.criar_hash(senha)
            self.dados['usuarios'][nome] = senha_hash
            self.dados['tarefas'][nome] = []
            self.salvar_dados()
            print(f"Usuário '{nome}' cadastrado com sucesso!")

    def verificar_senha(self, senha, senha_hash):
        return self.criar_hash(senha) == senha_hash

    def login(self, nome):
        if nome not in self.dados['usuarios']:
            print("Usuário não encontrado.")
            return

        senha = input("Digite a senha: ")

        for _ in range(4):
            if self.verificar_senha(senha, self.dados['usuarios'][nome]):
                print("Login bem-sucedido!")
                self.usuario_logado = nome
                self.atualizar_logins()
                return
            else:
                senha = input("Senha incorreta. Digite a senha novamente: ")

        print("Você excedeu o número máximo de tentativas de login.")

    def inicializar_logins(self):
        if 'logins' not in self.dados:
            self.dados['logins'] = []

    def atualizar_logins(self):
        agora = datetime.now().isoformat()
        login_atual = {'usuario': self.usuario_logado, 'data_hora': agora}
        self.dados['logins'].append(login_atual)
        self.salvar_dados()

    def get_data(self):
        if self.usuario_logado:
            expiracao = datetime.fromisoformat(self.dados['logins'][-1]['data_hora']) + timedelta(hours=1)
            agora = datetime.now()
            if agora <= expiracao:
                print(f"Status de login: Logado")
                print(f"Nome de usuário: {self.usuario_logado}")
                print(f"Expira em: {expiracao}")
            else:
                self.usuario_logado = None
                print("Status de login: Não logado (tempo de expiração atingido)")
                self.salvar_dados()
        else:
            print("Status de login: Não logado")

    def cadastrar_tarefa(self, titulo, descricao):
        if self.usuario_logado:
            tarefa = {'titulo': titulo, 'descricao': descricao, 'estado': "Não concluída"}
            self.dados['tarefas'][self.usuario_logado].append(tarefa)
            self.salvar_dados()
            print("Tarefa cadastrada com sucesso.")
        else:
            print("Você precisa fazer o login primeiro.")

    def marcar_tarefa_como_concluida(self, indice):
        if self.usuario_logado:
            if self.usuario_logado:
                if self.usuario_logado in self.dados['tarefas'] and self.dados['tarefas'][self.usuario_logado]:
                    try:
                        indice = int(indice) - 1
                        if 0 <= indice < len(self.dados['tarefas'][self.usuario_logado]):
                            tarefa = self.dados['tarefas'][self.usuario_logado][indice]
                            if tarefa['estado'] != "Concluída":
                                tarefa['estado'] = "Concluída"
                                self.salvar_dados()
                                print(f"Tarefa '{tarefa['titulo']}' foi marcada como concluída!")
                            else:
                                print("Essa tarefa já está marcada como concluída.")
                        else:
                            print("Número de tarefa inválido.")
                    except ValueError:
                        print("Número de tarefa inválido.")
                else:
                    print("Nenhuma tarefa encontrada para este usuário.")
            else:
                print("Você precisa fazer o login primeiro.")

    def visualizar_tarefas(self):
        if self.usuario_logado:
            if self.usuario_logado in self.dados['tarefas']:
                for i, tarefa in enumerate(self.dados['tarefas'][self.usuario_logado]):
                    
                    list = []

                    list.append(str(i))
                    list.append(tarefa['titulo'])
                    list.append(tarefa['descricao'])
                    list.append(tarefa['estado'])

                    max_v = max(len(x) for x in list)

                    print( "┌─────────────┬" + "─" * (max_v + 2) + "┐")
                    print(f"│ ID          │ {i+1}" + " " * ((max_v + 1) - len(str(i + 1))) + "│")
                    print(f"│ TITLE       │ {tarefa['titulo']}" + " " * ((max_v + 1) -len(str(tarefa['titulo']))) + "│")
                    print(f"│ DESCRIPTION │ {tarefa['descricao']}" + " " * ((max_v + 1) -len(str(tarefa['descricao']))) + "│")
                    print(f"│ ESTADO      │ {tarefa['estado']}" + " " * ((max_v + 1) -len(str(tarefa['estado']))) + "│")
                    print( "└─────────────┴" + "─" * (max_v + 2) + "┘\n")
                print("Digite 'conclude' seguido do número da tarefa para marcar como concluída.")
            else:
                print("Nenhuma tarefa encontrada para este usuário.")
        else:
            print("Você precisa fazer o login primeiro.")


    def excluir_tarefa(self, indice):
        if self.usuario_logado:
            if self.usuario_logado:
                if self.usuario_logado in self.dados['tarefas'] and self.dados['tarefas'][self.usuario_logado]:
                    try:
                        indice = int(indice) - 1
                        if 0 <= indice < len(self.dados['tarefas'][self.usuario_logado]):
                            tarefa_removida = self.dados['tarefas'][self.usuario_logado].pop(indice)
                            self.salvar_dados()
                            print(f"Tarefa '{tarefa_removida['titulo']}' excluída com sucesso!")
                        else:
                            print("Número de tarefa inválido.")
                    except ValueError:
                        print("Número de tarefa inválido.")
                else:
                    print("Nenhuma tarefa encontrada para este usuário.")
            else:
                print("Você precisa fazer o login primeiro.")

def main():
    opcoes = ["login", "register", "new", "view", "remove", "getdata", "conclude", "help", "-h"]

    parser = argparse.ArgumentParser(description="Gerenciamento de tarefas")
    parser.add_argument("comando", nargs="?", choices=opcoes)
    args = parser.parse_args()

    if not args.comando:
        print("\nInsira uma ação válida:\n")
        for i, opcao in enumerate(opcoes):
            print(f"    - {opcao}")

    else:
        task_manager = TaskManager()
        if args.comando == "login":
            nome = input("Digite o nome de usuário: ")
            task_manager.login(nome)
        elif args.comando == "register":
            nome = input("Digite o nome de usuário: ")
            senha = input("Digite a senha: ")
            task_manager.cadastrar_usuario(nome, senha)
        elif args.comando == "new":
            if not task_manager.usuario_logado:
                print("Você precisa fazer o login primeiro.")
                return
            titulo = input("Digite o título da tarefa: ")
            descricao = input("Digite a descrição da tarefa: ")
            task_manager.cadastrar_tarefa(titulo, descricao)
        elif args.comando == "view":
            if not task_manager.usuario_logado:
                print("Você precisa fazer o login primeiro.")
                return
            task_manager.visualizar_tarefas()
        elif args.comando == "remove":
            if not task_manager.usuario_logado:
                print("Você precisa fazer o login primeiro.")
                return
            indice = input("Digite o número da tarefa que deseja excluir: ")
            task_manager.excluir_tarefa(indice)
        elif args.comando == "conclude":
            if not task_manager.usuario_logado:
                print("Você precisa fazer o login primeiro.")
                return
            indice = input("Digite o número da tarefa que deseja marcar como concluída: ")
            task_manager.marcar_tarefa_como_concluida(indice)
        elif args.comando == "getdata":
            task_manager.get_data()

if __name__ == "__main__":
    main()