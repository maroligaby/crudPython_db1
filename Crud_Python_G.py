import sqlite3
from sqlite3 import Error, OperationalError
import os
from time import sleep
from IPython import get_ipython

def conectarBanco():
    conexao = None
    banco = 'crudPython.db'
   
    print(f'SQLite Versão: {sqlite3.version}\n')
   
    path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(path, banco)
    print(f'Banco de dados: [{full_path}]\n')
    
    if not os.path.isfile(full_path):
        continuar = input(f'Banco de dados não encontrado, deseja cliá-lo? \nSe sim então o banco será criado no diretório onde o programa está sendo executado [{os.getcwd()}]! [S/N]: ')
        
        if continuar.upper() != 'S':
            raise sqlite3.DatabaseError('Banco de dados não encontrado!')
           
    conexao = sqlite3.connect(full_path)
    print('BD aberto com sucesso!')
    
    return conexao

def criar_tabela(conexao):
    cursor = conexao.cursor()
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS funcionarios (
                        id INTEGER,
                        nome TEXT,
                        data_nascimento TEXT,
                        salario REAL
                    );
                    """)
    conexao.commit()

    if cursor:
        cursor.close()
        
def exibir_cabecalho(mensagem):
    mensagem = f'Rotina de {mensagem} de dados'

    print('\n' + '-' * len(mensagem))
    print(mensagem)
    print('-' * len(mensagem), '\n')

    id = input('ID (0 para voltar): ')

    return id

def mostrar_registro(registro):
    print('\n=========================')
    print('Registro')
    print('-------------------------')
    print('ID:', registro[0])
    print('Nome:', registro[1])
    print('Data de nascimento:', registro[2])
    print('Salário:', registro[3])
    print('=========================')

def tabela_vazia(conexao):
    cursor = conexao.cursor()
    cursor.execute('SELECT count(*) FROM funcionarios')
    resultado = cursor.fetchall()
    cursor.close()
    print(resultado)
    return resultado[0][0]== 0

def verificar_registro_existe(conexao, id):
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM funcionarios WHERE id=?', (id,))
    resultado = cursor.fetchone()
    cursor.close()

    return resultado 

def pausa():
    input('\nPressione <ENTER> para continuar')

def listar(conexao):
    if tabela_vazia(conexao):
        print('\n*** TABELA VAZIA ***')
        pausa()
        return

    cursor = conexao.cursor()

    print('\n----------------------')
    print('Listagem dos Registros')
    print('----------------------')

    cursor.execute('SELECT * FROM funcionarios')
    registros = cursor.fetchall()

    for registro in registros:
        print('ID:', registro[0])
        print('Nome:', registro[1])
        print('Data de nascimento:', registro[2])
        print('Salário:', registro[3])
        print('----------------------')

    pausa()

    cursor.close()

def incluir(conexao):
    id = exibir_cabecalho('inclusão')
    if int(id) == 0:
        return

    if verificar_registro_existe(conexao, id):
        print('\nID já existe!')
        sleep(2)
    else:
        nome = str(input('\nNome: '))
        data_nascimento = input('\nData de nascimento (formato:YYYY-MM-DD): ')
        salario = float(input('\nSalário: '))
        
        
        confirma = input('\nConfirma a inclusão [S/N]? ').upper()
        if confirma == 'S':
            comando = f'INSERT INTO funcionarios VALUES({id}, "{nome}","{data_nascimento}",{salario})'
            print("Registro incluido")
            sleep(2)

            cursor = conexao.cursor()
            cursor.execute(comando)
            conexao.commit()
            cursor.close()

def alterar(conexao):
    if tabela_vazia(conexao):
        print('\n*** TABELA VAZIA ***')
        pausa()
        return


    id = exibir_cabecalho('alteração')
    if int(id) == 0:
        return

    resultado = verificar_registro_existe(conexao, id)

    if not resultado:
        print('\nID não existe!')
        sleep(2)
    else:
        mostrar_registro(resultado)
        
        
        print("Qual campo deseja alterar?")
        print('1- Nome')
        print('2- Data de nascimento')
        print('3- Salário')
        print('0 para voltar')
        campo = input("Digite o número: ")
        print('============================')
        
        if campo == "1":
            nome = str(input('\nDigite o novo nome: '))
    
            confirma = input('\nConfirma a alteração [S/N]? ').upper()
            if confirma == 'S':
                cursor = conexao.cursor()
                cursor.execute('UPDATE funcionarios SET nome=? WHERE id=?', (nome, id))
                print("Dados alterados")
                sleep(2)
                conexao.commit()
                cursor.close()
                
        elif campo == "2":
            data_nascimento = input('\nDigite a nova data de nascimento: ')
    
            confirma = input('\nConfirma a alteração [S/N]? ').upper()
            if confirma == 'S':
                cursor = conexao.cursor()
                cursor.execute('UPDATE funcionarios SET data_nascimento=? WHERE id=?', (data_nascimento, id))
                print("Dados alterados")
                sleep(2)
                conexao.commit()
                cursor.close()
            
        elif campo == "3":
            salario = float(input('\nDigite o novo salário: '))
    
            confirma = input('\nConfirma a alteração [S/N]? ').upper()
            if confirma == 'S':
                cursor = conexao.cursor()
                cursor.execute('UPDATE funcionarios SET salario=? WHERE id=?', (salario, id))
                print("Dados alterados")
                sleep(2)
                conexao.commit()
                cursor.close()
        elif campo == "0":
            return alterar(conexao)
        else:
            print('Opção inválida!')
            sleep(2)

def excluir(conexao):
    if tabela_vazia(conexao):
        print('\n*** TABELA VAZIA ***')
        pausa()
        return

    id = exibir_cabecalho('exclusão')
    if int(id) == 0:
        return

    resultado = verificar_registro_existe(conexao, id)

    if not resultado:
        print('\nID não existe!')
        sleep(2)
    else:
        mostrar_registro(resultado)

        confirma = input('\nConfirma a exclusão [S/N]? ').upper()
        if confirma == 'S':
            cursor = conexao.cursor()
            cursor.execute('DELETE FROM funcionarios WHERE id=?', (id, ))
            print("\nRegistro excluido\n")
            sleep(2)
            conexao.commit()
            cursor.close()
            
def buscar(conexao):
    if tabela_vazia(conexao):
        print('\n*** TABELA VAZIA ***')
        pausa()
        return
    
    cursor = conexao.cursor()

    print('\n------------------')
    print('Busca de Registros')
    print('------------------')
    print("1- ID")
    print('2- Nome')
    print('3- Data de nascimento')
    print('4- Salário')
    campo = input("\nQual campo deseja buscar?: ")
    
    if campo == "1":
        idBusca = input("\nDigite o ID para busca: ")
        
        cursor.execute(f"SELECT *  FROM funcionarios WHERE id LIKE '{idBusca}%'")
        registro = 0
        print("\n--------------")    
        for i in cursor:
            print(i)
            registro = registro +1 
        print("--------------")    
        print("Busca encerrada!")
        if registro == 0:
           print ('Resultado não encontrado!')
        cursor = conexao.cursor()
        cursor.close()
        pausa()
        
    elif campo == "2":
        nomeBusca = input("\nDigite o nome para busca: ")
        
        cursor.execute(f"SELECT *  FROM funcionarios WHERE nome LIKE '%{nomeBusca}%'")
        registro = 0
        print("\n--------------")    
        for i in cursor:
            print(i)
            registro = registro +1 
        print("--------------")    
        print("Busca encerrada!")
        if registro == 0:
           print ('Resultado não encontrado!')
        cursor = conexao.cursor()
        cursor.close()
        pausa()
        
    
    elif campo == "3":
        dataBusca = input('\nDigite a de data de nascimento (YYYY-MM-DD) para busca: ')
                   
        cursor.execute(f"SELECT * FROM funcionarios WHERE data_nascimento LIKE '%{dataBusca}%'")
        registro = 0
        print("\n--------------")    
        for i in cursor:
            print(i)
            registro = registro +1 
        print("--------------")    
        print("Busca encerrada!")
        if registro == 0:
           print ('Resultado não encontrado!')
        cursor = conexao.cursor()
        cursor.close()
        pausa()
        
    elif campo == "4":
        salarioBusca = input('\nDigite o salario para busca: ')
                   
        cursor.execute(f"SELECT * FROM funcionarios WHERE salario LIKE '%{salarioBusca}%'")
        registro = 0
        print("\n--------------")    
        for i in cursor:
            print(i)
            registro = registro +1 
        print("--------------")    
        print("Busca encerrada!")
        if registro == 0:
           print ('Resultado não encontrado!')
        cursor = conexao.cursor()
        cursor.close()
        pausa()

def menu(conexao):
    menuConf = True
    while menuConf == True:
        print('--------------')
        print('MENU DE OPÇÕES')
        print('--------------')
        print('1. Incluir dados')
        print('2. Alterar dados')
        print('3. Excluir dados')
        print('4. Listar dados')
        print('5. Buscar dados')
        print('6. Sair')

        try:
            opcao = int(input('\nOpção [1-6]: '))
        except ValueError:
            opcao = 0
    
        if opcao == 1:
            incluir(conexao)
        elif opcao == 2:
            alterar(conexao)
        elif opcao == 3:
            excluir(conexao)
        elif opcao == 4:
            listar(conexao)
        elif opcao == 5:
            buscar(conexao)
        elif opcao == 6:
            menuConf = False
            
    return opcao
   
if __name__ == '__main__':
    conn = None

    while True:
        try:
            conn = conectarBanco()
            criar_tabela(conn)

            if menu(conn) == 6:
                break
        except OperationalError as e:
            print('Erro operacional:', e)
        except sqlite3.DatabaseError as e:
            print('Erro database:', e)
            raise SystemExit()
        except Error as e:
            print('Erro SQLite3:', e)
            raise SystemExit()
        except Exception as e:
            print('Erro durante a execução do sistema!')
            print(e)
        finally:
            if conn:
                print('Liberando a conexão...')
                conn.commit()
                conn.close()
    sleep(2)
    print('Encerrando...')
    