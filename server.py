import socket
import threading
import time


# conexões
SERVER_IP = socket.gethostbyname(socket.gethostname()) #Pegar o enderço de ip
PORT = 5050 #pegar a porta
ADDR = (SERVER_IP, PORT) # IP do server e porta usada
FORMATO = 'utf-8' # decodificar a mensagem 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #classe do socket e tipo de entrada e saída (TCP)
server.bind(ADDR) 

conexoes = [] # registro de conexões



def enviar_mensagem_todos(mensagem):  # Manda a mensagem para todas as conexoes
    global conexoes
    for conexao in conexoes:
        print(f"[ENVIANDO] Enviando mensagens para {conexao['addr']}")
        conexao['conn'].send(mensagem.encode())
        time.sleep(0.333)


def handle_clientes(conn, addr):
    print(f"[NOVA CONEXAO] Um novo usuario se conectou pelo endereço {addr}") # imprime o endereço do cliente que se conectou
    global conexoes
    global mensagens
    nome = False # nome do cliente

    while(True):
        msg = conn.recv(1024).decode(FORMATO) #128 tamanho máximo da mensagem
        if(msg): #verifica a mensagem
            if(msg.startswith("IP=")): # se a mensagem for um IP
                mensagem_separada = msg.split("=") # separa a mensagem em duas 
                nome = mensagem_separada[1] # nome está no índice 1 do array
                mapa_da_conexao = {  # objeto com todas as informações do mapa da conexão
                    "conn": conn,
                    "addr": addr,
                    "nome": nome,
                    "last": 0
                }
                conexoes.append(mapa_da_conexao) #adiciona ao array que guarda as conexões
                #enviar_mensagem_individual(mapa_da_conexao) #faz ele receber todas as mensagens até agora
                ###### QUANDO TIVER DUAS CONEXÕES, COMECE O JOGO
                if len(conexoes) == 2:
                    for conexao in conexoes:
                        mensagem_de_envio = 'COMECE'
                        conexao['conn'].send(mensagem_de_envio.encode())

            elif msg.startswith("msg="):  # Se a mensagem for uma mensagem (Jogador)
                porta = conn.getpeername()[1]
                mensagem_separada = msg.split("=")  # Separa o conteúdo da mensagem
                mensagem = str(porta) + "=" + mensagem_separada[1]  # Agora enviaremos a porta em vez do IP
                
                enviar_mensagem_todos(mensagem)



def start():
    i = 0
    print("[INICIANDO] Iniciando Socket")
    while(i < 2):
        server.listen() # socket ouvindo cliente
        conn, addr = server.accept() # aceita entrada do cliente, fica esperando
        thread = threading.Thread(target=handle_clientes, args=(conn, addr)) #thread que chama a funçao handle clientes
        thread.start() #inicia a thread
        i+=1

    # começa o jogo quando a conexão está feita
    
start()


