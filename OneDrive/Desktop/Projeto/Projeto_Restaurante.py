import matplotlib.pyplot as plt
import pymysql.cursors
import graficos as Tk


conexao  = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='erp',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

Autentico = False

def logarCadastrar(decisao, resultado):
    usuarioExistente = 0
    autenticado = False
    usuarioMaster = False

    if decisao == 1:
        nome = input('Digite seu nome: ')
        senha = input('Digite sua senha: ')

        for linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                autenticado = True
                if linha['nivel'] == 1:
                    usuarioMaster = False
                elif linha['nivel'] == 2:
                    usuarioMaster = True
                    break             
            else:
                autenticado = False     
        if not autenticado:
            print('Usuario ou senha incorretos')

    elif decisao == 2:
        print('Faça seu cadastro')
        nome = input('Digite seu nome: \n')
        senha = input('Digite a sua senha: \n')

        for linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                usuarioExistente = 1
                break

        if usuarioExistente == 1:
            print('Usuario ja existe tente um nome ou senha diferente')
        elif usuarioExistente == 0:
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('insert into cadastros (nome, senha, nivel) values (%s, %s, %s)', (nome, senha, '1'))
                    conexao.commit()
                    print('Cadastro realizado com sucesso')
                    autenticado = True
            except Exception:
                print('Erro ao inserir os dados no banco de dados')

    return autenticado, usuarioMaster             


def cadastrarProdutos():
    nome = input('Digite o nome do produto: ')
    ingredientes = input('Digite os ingredientes do produto: ')
    grupo = input('Digite o grupo do produto: ')
    preco = float(input('Digite o preço do produto: '))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('insert into produtos (nome, ingredientes, grupo, preco) values (%s, %s, %s, %s)', (nome, ingredientes, grupo, preco))
            conexao.commit()
            print('Produto cadastrado com sucesso ! ')
    except:
        print('Erro ao cadastrar produto')


def listarProdutos():
    produtos = []
    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from produtos')
            produtosCadastrados = cursor.fetchall()
            print(produtosCadastrados)
    except Exception:
        print('Erro ao iniciar banco de dados')
    for i in produtosCadastrados:
        produtos.append(i)
        if len(produtos) != 0:
            for i in range(len(produtos)):
                print(produtos[i])     
    else:
        print('Nenhum produto cadastrado')

def excluirProdutos():
    idproduto = int(input('Digite o id do produto que deseja excluir: '))
    try:
        with conexao.cursor() as cursor:
            cursor.execute(
                'delete from produtos where id = %s', (idproduto,)
            )
            conexao.commit()
            print('Produto excluido com sucesso ! ')
    except:
        print('Erro ao excluir produto')


def listarPedidos():

    pedidos = []
    decision = 0

    while decision != 2:
        pedidos.clear()
        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from pedidos')
                listaPedidos = cursor.fetchall()
        except:
            print('Erro ao iniciar banco de dados')
            break
        for i in listaPedidos:
            pedidos.append(i)

        if len(pedidos) != 0:
            for i in range(0, len(pedidos)):
                print(pedidos[i])
        else:
            print('Nenhum pedido feito')
        
        decision = int(input('Digite 1 para dar o produto com entregue  ou 2 para voltar: '))

        if decision == 1:
            idDeletar = int(input('Digite o id do pedido que deseja dar como entregue: '))

            try:
                with conexao.cursor() as cursor:
                    cursor.execute('delete from pedidos where id = %s', (idDeletar,))
                    conexao.commit()
                    print('Pedido dado como entregue com sucesso !')
            except:
                print('Erro ao dar pedido como entregue')


def gerarEstatisticas():
    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from produtos')
            produtos = cursor.fetchall()
            
        with conexao.cursor() as cursor:
            cursor.execute('select * from estatisticavendido')
            vendido = cursor.fetchall()
    except:
        print('Erro ao consultar o banco de dados')
        return 

    estado = int(input('Digite 0 para sair, 1 para pesquisar por nome ou 2 para pesquisar por grupo: '))

    if estado == 1:
        decisao3 = int(input('Digite 1 para pesquisar por valor ou 2 para pesquisar por unidade vendida: '))
        
        if decisao3 == 1:
            nomeProdutos = []
            valores = []

            
            for i in produtos:
                nomeProdutos.append(i['nome'])
                
                valores = []
                valores.clear()
                
                for h in range(len(vendido)):
                    somaValor = -1
                    for i in vendido:
                        if i['nome'] == nomeProdutos[h]:
                            somaValor += i['preco']
                            valores.append(0)
                        elif somaValor > 0:
                            valores.append(somaValor+1)
                            
                    plt.plot(nomeProdutos, valores)
                    plt.ylabel('Quantidade vendida em reais')
                    plt.xlabel('Produtos')
                    plt.show()
                    
                    if decisao3 == 2:
                        grupoUnico = []
                        grupoUnico.clear()
                        
                        try:
                            with conexao.cursor() as cursor:
                                cursor.execute('select * from produtos')
                                grupo = cursor.fetchall()
                        except Exception:
                            print('Erro na consulta')
                            
                            try:
                                with conexao.cursor() as cursor:
                                    cursor.execute('select * from estatisticavendido')
                                    vendidoGrupo = cursor.fetchall()
                            except Exception:
                                print('Erro na consulta')
                                
                                for i in grupo:
                                    grupoUnico.append(i['nome'])
                                    
                                    grupoUnico = sorted(set(grupoUnico))
                                    
                                    qntFinal = []
                                    qntFinal.clear()
                                    
                                    for h in range(0, len(grupoUnico)):
                                        qntUnitaria = 0
                                        for i in vendidoGrupo:
                                            if grupoUnico[h] == i['grupo']:
                                                qntUnitaria += 1
                                        qntFinal.append(qntUnitaria)
                                        
                                        plt.plot(grupoUnico, qntFinal)
                                        plt.ylabel('Quantidade vendida em unidades')
                                        plt.xlabel('Produtos')
                                        plt.show()
    elif estado == 2:
        decisao3 = int(input('Digite 1 para pesquisar por valor, 2 para pesquisar por unidade vendida ou 3 para visualizar a data das vendas: '))
        if decisao == 1:
            
            for i in produtos:
                nomeProdutos.append(i['grupo'])
                valores = []
                valores.clear()
                
                for h in range(len(vendido)):
                    somaValor = -1
                    for i in vendido:
                        if i['grupo'] == nomeProdutos[h]:
                            somaValor += i['preco']
                            if somaValor == -1:
                                valores.append(0)
                            elif somaValor > 0:
                                valores.append(somaValor+ 1)
                                
                                plt.plot(nomeProdutos, valores)
                                plt.ylabel('Quantidade vendida em reais')
                                plt.xlabel('Produtos')
                                plt.show()
                                
                    if decisao3 == 3:
                        
                        dataVendas = []
                        dataVendas.clear()
                        
                        try:
                            with conexao.cursor() as cursor:
                                cursor.execute('select * from estatisticavendido')
                                dataVendas = cursor.fetchall()
                                dataVendas = sorted(dataVendas, key=lambda x: x['data'])
                        except Exception:
                            print('Erro na consulta')
                            
                            dataUnica = []
                            dataUnica.clear()
                            
                            for i in dataVendas:
                                dataUnica.append(i['data'])
                                
                                dataUnica = sorted(set(dataUnica))
                                
                                qntFinal = []
                                qntFinal.clear()
                                
                                for h in range(0, len(dataUnica)):
                                    qntUnitaria = 0
                                    for i in dataVendas:
                                        if dataUnica[h] == i['data']:
                                            qntUnitaria += 1
                                    qntFinal.append(qntUnitaria)
                                    
                                    plt.plot(dataUnica, qntFinal)
                                    plt.ylabel('Quantidade vendida em unidades')
                                    plt.xlabel('Produtos')
                                    plt.show()





while not Autentico:
    decisao = int(input('Digite 1 para logar ou 2 para cadastrar: '))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from cadastros')
            resultado = cursor.fetchall()
        
        Autentico, usuarioMaster = logarCadastrar(decisao, resultado)
    except:
        print('Erro ao conectar com o banco de dados')

if Autentico == True:
    print('Bem vindo ao sistema')
    if usuarioMaster == True:
        while True: 
            decisaoUsuario = int(input('\nDigite:\n0 para sair\n1 para cadastrar produtos\n2 para listar produtos\n3 para listar pedidos/excluir\n4 para visualizar estatísticas:\n> '))
            
            if decisaoUsuario == 0:
                print("Saindo do sistema...")
                break
            elif decisaoUsuario == 1:
                cadastrarProdutos()
            elif decisaoUsuario == 2:
                listarProdutos()
            elif decisaoUsuario == 3:
                listarPedidos()
                delete = int(input('Digite 3 para excluir um produto ou 0 para voltar: '))
                if delete == 3:
                    excluirProdutos()
            elif decisaoUsuario == 4:
                gerarEstatisticas()

