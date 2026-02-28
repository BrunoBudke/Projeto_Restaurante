import pymysql
import pymysql.cursors

conexao = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='erp',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
    
    )

autentico = False

def logar_cadastrar():
    usuario_existente = 0
    autenticado = False
    usuario_mestre = False

    if decisao == 1:
        nome = input("Digite seu nome: ")
        senha = input("Digite sua senha: ")

        for linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                if linha['nivel'] == '1':
                    usuario_mestre = False
                elif linha['nivel'] == '2':
                    usuario_mestre = True
                    autenticado = True
                else:
                    autenticado = False

                if not autenticado:
                    print('Usuario ou senha incorretos. Tente novamente,')
        
        if decisao == 2:
            nome = input("Digite seu nome: ")
            senha = input("Digite a sua senha: ")
            
            for linha in resultado:
                if nome == linha['nome'] and senha == linha['senha']:
                    usuario_existente = 1
            
            if usuario_existente == 1:
                print('Usuario ja cadastrado. Tente um nome ou senha  diferente. ')
            elif usuario_existente == 0:
                try:
                    with conexao.cursor() as cursor:
                        cursor.execute('insert into cadastro(nome, senha, nivel) values(%s, %s, %s)', (nome, senha, 1))
                        conexao.commit()
                except:
                    print("erro ao inserir os dados no banco de dados.")

                                    
                                    
                        

                    



            

while not autentico:
    decisao = int(input('Digite 1 para cadastrar ou 2 para fazer login: '))

    try:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios")
            resultado = cursor.fetchall()
        
    except:
        print('Erro ao acessar o banco de dados.')

            
    


 

            
           

       






