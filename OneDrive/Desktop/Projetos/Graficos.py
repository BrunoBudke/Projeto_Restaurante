from tkinter import Tk, Label, Entry, Button, Toplevel, messagebox, ttk
import pymysql

class AdminJanela():
    def __init__(self):
        self.root = Tk()
        self.root.title("Painel Administrativo - Master")
        self.root.geometry("500x500")
        
        Label(self.root, text="Bem-vindo ao Painel do Administrador!", font=("Arial", 14)).pack(pady=20)
        Button(self.root, text="Sair do Sistema", command=self.root.destroy, bg="red", fg="white").pack(pady=10)
        
        
        Button(self.root, text='Pedidos', width=20, bg='#2e4682').pack(pady=10)
        Button(self.root, text='Cadastro', width=20, bg='#485A88', command=self.CadastrarProduto).pack(pady=10)
        
        self.root.mainloop()

    def CadastrarProduto(self):
    
        self.cadastrar = Toplevel(self.root) 
        self.cadastrar.title("Cadastrar Produtos")
        self.cadastrar["bg"] = '#524f4f' 
        
        
        Label(self.cadastrar, text='Cadastre o produto', bg='#524f4f', fg='white').grid(row=0, column=0, columnspan=4, padx=5, pady=5)
        
        Label(self.cadastrar, text='nome', bg='#524f4f', fg='white').grid(row=1, column=0, columnspan=1, padx=5, pady=5)
        self.nome = Entry(self.cadastrar)
        self.nome.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        
        Label(self.cadastrar, text='ingredientes', bg='#524f4f', fg='white').grid(row=2, column=0, columnspan=1, padx=5, pady=5)
        self.ingredientes = Entry(self.cadastrar)
        self.ingredientes.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
        
        Label(self.cadastrar, text='grupo', bg='#524f4f', fg='white').grid(row=3, column=0, columnspan=1, padx=5, pady=5)
        self.grupo = Entry(self.cadastrar)
        self.grupo.grid(row=3, column=1, columnspan=2, padx=5, pady=5)
        
        Label(self.cadastrar, text='precos',bg='#524f4f', fg='white').grid(row=4, column=0, columnspan=1, padx=5, pady=5)
        self.preco = Entry(self.cadastrar)
        self.preco.grid(row=4, column=1, columnspan=2, padx=5, pady=5)

class JanelaPadrao():
    def __init__(self):
        self.root = Tk()
        self.root.title("Painel Padrão")
        self.root.geometry("400x400")
        Label(self.root, text="Bem-vindo, Usuário Padrão!", font=("Arial", 12)).pack(pady=20)
        self.root.mainloop()

class JanelaLogin():
    def __init__(self):
        try:
            self.root = Tk()
            self.root.title("Login")
            
            Label(self.root, text="Faça o login").grid(row=0, column=0, columnspan=2)
            
            Label(self.root, text="Usuario").grid(row=1, column=0)
            self.login = Entry(self.root)
            self.login.grid(row=1, column=1, padx=5, pady=5)
            
            Label(self.root, text="senha").grid(row=2, column=0)
            self.senha = Entry(self.root, show="*")
            self.senha.grid(row=2, column=1, padx=5, pady=5)
            
            Button(self.root, text="Login", bg="green3", width=10, command=self.verificar_login).grid(row=3, column=0, padx=5, pady=5)
            Button(self.root, text="Cadastrar", bg="orange", width=10, command=self.Cadastros).grid(row=3, column=1, padx=5, pady=5)
            Button(self.root, text="Listar Itens", bg="white", width=20, command=self.visualizar_cadastro).grid(row=5, column=0, columnspan=2, padx=5, pady=5)

            self.root.mainloop()
            
        except Exception as e:
            print(f"Erro ao inicializar a janela: {e}")

    
    def mostrarProdutosBackend(self):
        try:
            conexao = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='erp',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            print("Erro ao acessar o banco")
            return # Sai da função se não conectou
            
        try:
            with conexao.cursor() as cursor:
                cursor.execute("SELECT * FROM produtos")
                Resultados = cursor.fetchall() # Corrigido: Faltavam os parênteses ()
        except:
            print("Erro ao consultar")
            return
        
        self.tree.delete(*self.tree.get_children())
        
        linhaV = []
        
        for linha in Resultados:
            linhaV.append(linha['nome'])
            linhaV.append(linha['ingredientes'])
            linhaV.append(linha['grupo'])
            linhaV.append(linha['preco'])
            
            # Corrigido: 'end' precisa estar entre aspas
            self.tree.insert("", 'end', values=linhaV, iid=linha['id'], tag=1)
            
            linhaV.clear() # Corrigido: Faltavam os parênteses ()
            
    
    def CadastrarProdutoBackend(self):
        nome = self.nome.get()
        ingredientes = self.ingredientes.get()
        grupo = self.grupo.get()
        preco = self.preco.get()
        
        try:
            conexao = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='erp',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            print("Erro ao conectar ao banco")
            return
            
        try:
            with conexao.cursor() as cursor:
                # Corrigido: Formatação do SQL arrumada
                cursor.execute("INSERT INTO produtos(nome, ingredientes, grupo, preco) VALUES (%s, %s, %s, %s)", (nome, ingredientes, grupo, preco))
                conexao.commit()
        except Exception as e:
            print(f"Erro ao fazer a consulta: {e}")
            
        self.mostrarProdutosBackend() # Corrigido: Letra inicial arrumada e parênteses adicionados

    def verificar_login(self):
        usuario = self.login.get()
        senha = self.senha.get()
        
        try:
            conexao = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                database='erp',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor  
            )
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            messagebox.showerror("Erro", "Falha na conexão com o banco de dados.")
            return

        autenticado = False
        usuarioMaster = False

        try:
            with conexao.cursor() as cursor:
                sql = "SELECT * FROM cadastros WHERE nome = %s AND senha = %s"
                cursor.execute(sql, (usuario, senha))
                resultado = cursor.fetchone()
                
                if resultado:
                    autenticado = True
                    if resultado['nivel'] == 2:
                        usuarioMaster = True
        except Exception as e:
            print(f"Erro ao executar a consulta SQL: {e}")
            messagebox.showerror("Erro", "Erro ao realizar consulta no banco.")
            return
        finally:
            conexao.close()
            
        if not autenticado:
            messagebox.showerror("Erro de Login", "Usuário ou senha incorretos.")
        else:
            self.root.destroy() 
            
            if usuarioMaster:
                messagebox.showinfo("Login Bem-Sucedido", "Bem-vindo, usuário master!")
                AdminJanela() 
            else:
                messagebox.showinfo("Login Bem-Sucedido", "Bem-vindo, usuário padrão!")
                JanelaPadrao()
                
    def Cadastros(self):
        Label(self.root, text="Chave de segurança").grid(row=4, column=0, pady=5, padx=5)
        self.codigoSeguranca = Entry(self.root, show='*')
        self.codigoSeguranca.grid(row=4, column=1, pady=5, padx=10)
        Button(self.root, text='Confirmar cadastro', width=15, bg='blue', command=self.cadastroBackend).grid(row=5, column=1, columnspan=3, pady=5, padx=10)

    def cadastroBackend(self):
        codigoPadrao = '123456' 
        
        if self.codigoSeguranca.get() == codigoPadrao:
            if len(self.login.get()) <= 20:
                if len(self.senha.get()) <= 50:
                    
                    nome = self.login.get()
                    senha = self.senha.get()
                
                    try:
                        conexao = pymysql.connect(
                            host='localhost',
                            user='root',
                            password='',
                            database='erp',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor  
                        )
                    except Exception as e:
                        print(f"Erro ao conectar ao banco de dados: {e}")
                        messagebox.showerror("Erro", "Falha na conexão com o banco de dados.")
                        return
                    
                    try:
                        with conexao.cursor() as cursor:
                            cursor.execute("INSERT INTO cadastros (nome, senha, nivel) VALUES (%s, %s, %s)", (nome, senha, 1))
                            conexao.commit()
                            messagebox.showinfo("Cadastro", "Usuario cadastrado com sucesso!")
                    except Exception as e:
                        print(f"Erro ao inserir dados no banco: {e}")
                        messagebox.showerror("Erro", "Erro ao salvar no banco.")
                    finally:
                        conexao.close()
                else:
                    messagebox.showerror("Erro", "Digite uma senha com no máximo 50 caracteres.")
            else:
                messagebox.showerror("Erro", "Digite um nome com no máximo 20 caracteres.")
        else:
            messagebox.showerror("Erro", "Código de segurança incorreto.")

    def UpdateBackend(self):
        try:
            conexao = pymysql.connect(
                host='localhost',
                user='root',  
                password='',
                database='erp',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return
            
        try:
            with conexao.cursor() as cursor:
                cursor.execute("SELECT * FROM cadastros")
                resultados = cursor.fetchall()
        except Exception as e:
            print(f"Erro ao fazer a consulta: {e}")
            conexao.close()
            return
                
        try:
            self.tree.delete(*self.tree.get_children())
            
            for linha in resultados:
                linhaV = [linha['id'], linha['nome'], linha['senha'], linha['nivel']]
                self.tree.insert("", 'end', values=linhaV, iid=linha['id'])
        except Exception as e:
            print(f"Erro ao mostrar dados na tabela: {e}")
        finally:
            conexao.close()

    def visualizar_cadastro(self):
        self.vc = Toplevel(self.root)
        self.vc.resizable(False, False)
        self.vc.title("Visualizar Cadastros")
            
        self.tree = ttk.Treeview(self.vc, selectmode='browse', column=('column1', 'column2', 'column3', 'column4'), show='headings')
            
        self.tree.column("column1", width=40, minwidth=40, stretch=False)
        self.tree.heading('#1', text='ID')
            
        self.tree.column("column2", width=100, minwidth=100, stretch=False)
        self.tree.heading('#2', text='Usuário')
            
        self.tree.column("column3", width=100, minwidth=100, stretch=False)
        self.tree.heading("#3", text='Senha')
            
        self.tree.column("column4", width=40, minwidth=40, stretch=False)
        self.tree.heading('#4', text='Nível')
            
        self.tree.grid(row=0, column=0, padx=10, pady=10)
        
        self.mostrarProdutosBackend()
        self.UpdateBackend()

if __name__ == "__main__":
    JanelaLogin()
