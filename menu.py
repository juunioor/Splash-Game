import pygame, sys, random, socket, time, threading

#DEFININDO CONEXÕES
PORT = 5050
FORMATO = 'utf-8'
SERVER = "192.168.0.107" #Endereço do server
ADDR = (SERVER, PORT)

#PEGANDO O IP DA MAQUINA
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#VARIAVEIS DE CONTROLE PRA COMEÇAR O GAME
inimigo_conectado = False
atleta = 0
atleta_inimigo = 0   #Essa variavel muda quando receber um atleta inimigo
localizacao_inimigo = 20
posicao_aliado = 20



########################################################################################################################################################################################################################################################################
def matchInicio():
    global inimigo_conectado
    msg = client.recv(1024).decode() # mudar para 1024 se der merda
    if (msg == 'COMECE'):
      inimigo_conectado = True
    else:
      inimigo_conectado = False

def verificarInicio():
    thread_inicio = threading.Thread(target=matchInicio)
    thread_inicio.start()

def handle_mensagens():
    while(True):
        global localizacao_inimigo
        global atleta_inimigo

        msg = client.recv(1024).decode() # mudar para 1024 se der merda
        print("ESSA MENSAGEM QUE CHEGOU:", msg)

        # conteúdo da mensagem
        mensagem_splitada = msg.split("=")

        # quem enviou
        porta_recebido = mensagem_splitada[0]

        # msg recebida (pode ser a pontuacao ou um atleta)
        msg_recebida = mensagem_splitada[1]

        msg_recebida_int = int(msg_recebida)

        porta_client = client.getsockname()[1]
        print("ESSA É A PORTA DO CLIENT", str(porta_client))
        print("ESSA É A PORTA QUE IREMOS COMPARAR", porta_recebido)

        #Verificação se a pontuação recebida da msg é do inimigo
        if (porta_recebido != str(porta_client)):
            if(msg_recebida_int == 0 or msg_recebida_int == 1 or msg_recebida_int == 2 or msg_recebida_int == 3 or msg_recebida_int == 4 or msg_recebida_int == 5 or msg_recebida_int == 6):
                atleta_inimigo = msg_recebida_int
            else:
                localizacao_inimigo = msg_recebida_int

        


def enviar(mensagem):
    #print("ESSA É A MENSAGEM QUE ESTAMOS ENVIANDO PARA O SERVIDOR REPASSAR:", mensagem)
    client.send(mensagem.encode(FORMATO))

def enviar_mensagem(pontuacao_vida):
    thread1 = threading.Thread(target=handle_mensagens)
    thread1.start()
    mensagem = "msg=" + str(pontuacao_vida)
    enviar(mensagem)

def enviar_atleta(atleta):
    thread_atleta = threading.Thread(target=handle_mensagens)
    thread_atleta.start()
    mensagem = "msg=" + str(atleta)
    enviar(mensagem)

def enviar_IP():
    nome = socket.gethostbyname(socket.gethostname())
    enviar("IP=" + nome)

def iniciar_envio():
    enviar_IP()
    

def iniciar():
    thread2 = threading.Thread(target=iniciar_envio)
    thread2.start()



########################################################################################################################################################################################################################################################################
pygame.init()    
screen = pygame.display.set_mode((1280, 632))
pygame.display.set_caption("Splash")
screen.fill((255,255,255))

#CORES
AMARELO  = (234, 196, 58)
BRANCO = (255, 255, 255)

#FONTES USADAS
import pygame.freetype
pygame.freetype.init()
fonteTexto = pygame.freetype.Font("Fontes/upheavtt.ttf", 45)

def get_pygame_events():
  pygame_events = pygame.event.get()
  return pygame_events



########################################################################################################################################################################################################################################################################
#TECLAS
keys_pressed = get_pygame_events()

#SONS
musicamenu = pygame.mixer.Sound("Sons/musicamenu.wav")
musicatema = pygame.mixer.Sound("Sons/musicatema.wav")
click = pygame.mixer.Sound("Sons/click.wav")
start_som = pygame.mixer.Sound("Sons/start.wav")
gameover_som = pygame.mixer.Sound("Sons/gameover.wav")
acerto_lixeira = pygame.mixer.Sound("Sons/acerto_lixeira.wav")
erro = pygame.mixer.Sound("Sons/erro_lixeira.wav")
inimigoconectado = pygame.mixer.Sound("Sons/conectado.wav")
somcontagem = pygame.mixer.Sound("Sons/somcontagem.wav")
comecoujogo = pygame.mixer.Sound("Sons/somcomecou.wav")
onda = pygame.mixer.Sound("Sons/onda.wav")
selecionar = pygame.mixer.Sound("Sons/selecionar.wav")
vitoriasom = pygame.mixer.Sound("Sons/vitoriasom.wav")
derrotasom = pygame.mixer.Sound("Sons/derrotasom.wav")

#BARRAS ALIADAS
barraa = pygame.image.load('Props/barra_aliada.png')

barra_aliada = [pygame.image.load('Props/Barra/0.gif'),pygame.image.load('Props/Barra/200.gif'),pygame.image.load('Props/Barra/400.gif'),pygame.image.load('Props/Barra/600.gif'),
                pygame.image.load('Props/Barra/800.gif'),pygame.image.load('Props/Barra/1000.gif'),pygame.image.load('Props/Barra/1200.gif'),
                pygame.image.load('Props/Barra/1400.gif'),pygame.image.load('Props/Barra/1600.gif'),pygame.image.load('Props/Barra/1800.gif')]

#BARRAS INIMIGAS
barrai = pygame.image.load('Props/barra_inimiga.png')

barra_inimiga = [pygame.image.load('Props/Barra/0inimiga.gif'),pygame.image.load('Props/Barra/200inimiga.gif'),pygame.image.load('Props/Barra/400inimiga.gif'),pygame.image.load('Props/Barra/600inimiga.gif'),
                pygame.image.load('Props/Barra/800inimiga.gif'),pygame.image.load('Props/Barra/1000inimiga.gif'),pygame.image.load('Props/Barra/1200inimiga.gif'),
                pygame.image.load('Props/Barra/1400inimiga.gif'),pygame.image.load('Props/Barra/1600inimiga.gif'),pygame.image.load('Props/Barra/1800inimiga.gif')]

#FUNDO DO MENU
fundo_inicio_img = [pygame.image.load("Inicio/1.png"),pygame.image.load("Inicio/2.png"),pygame.image.load("Inicio/3.png"),pygame.image.load("Inicio/4.png"),pygame.image.load("Inicio/5.png"),
                    pygame.image.load("Inicio/6.png"),pygame.image.load("Inicio/7.png"),pygame.image.load("Inicio/8.png"),pygame.image.load("Inicio/9.png"),pygame.image.load("Inicio/10.png"),
                    pygame.image.load("Inicio/11.png"),pygame.image.load("Inicio/12.png")]

#FUNDO ALTERNATIVO
fundo_alternativo = [pygame.image.load("Inicio/Alternativo/1.png"),pygame.image.load("Inicio/Alternativo/2.png"),pygame.image.load("Inicio/Alternativo/3.png"),pygame.image.load("Inicio/Alternativo/4.png"),pygame.image.load("Inicio/Alternativo/5.png"),
                     pygame.image.load("Inicio/Alternativo/6.png"),pygame.image.load("Inicio/Alternativo/7.png"),pygame.image.load("Inicio/Alternativo/8.png"),pygame.image.load("Inicio/Alternativo/9.png"),pygame.image.load("Inicio/Alternativo/10.png"),
                     pygame.image.load("Inicio/Alternativo/11.png")]

#FUNDO DO MATCH
fundo_selecao_img = [pygame.image.load("Selecao/1.png"),pygame.image.load("Selecao/2.png"),pygame.image.load("Selecao/3.png"),pygame.image.load("Selecao/4.png"),pygame.image.load("Selecao/5.png")]

#FUNDO DO MATCH
pre_selecao_img = [pygame.image.load("Selecao/ANS_1.png"),pygame.image.load("Selecao/ANS_2.png"),pygame.image.load("Selecao/ANS_3.png"),pygame.image.load("Selecao/ANS_4.png"),pygame.image.load("Selecao/ANS_5.png")]

#EFEITOS
estrelas_img = [pygame.image.load("Selecao/ESTRELA_1.png"),pygame.image.load("Selecao/ESTRELA_2.png"),pygame.image.load("Selecao/ESTRELA_3.png"),pygame.image.load("Selecao/ESTRELA_4.png"),pygame.image.load("Selecao/ESTRELA_5.png")]

#ATLETAS
atletas_img = [pygame.image.load("Selecao/ATLETA_0.png"),pygame.image.load("Selecao/ATLETA_1.png"),pygame.image.load("Selecao/ATLETA_2.png"),pygame.image.load("Selecao/ATLETA_3.png"),pygame.image.load("Selecao/ATLETA_4.png"),
               pygame.image.load("Selecao/ATLETA_5.png"),pygame.image.load("Selecao/ATLETA_6.png")]

#ATLETAS INFOS
atletasinfos_img = [pygame.image.load("Selecao/ATLETA0_INFO.png"),pygame.image.load("Selecao/ATLETA1_INFO.png"),pygame.image.load("Selecao/ATLETA2_INFO.png"),pygame.image.load("Selecao/ATLETA3_INFO.png"),pygame.image.load("Selecao/ATLETA4_INFO.png"),
                    pygame.image.load("Selecao/ATLETA5_INFO.png"),pygame.image.load("Selecao/ATLETA6_INFO.png")]

#FUNDOS LETRAS E BOTÕES
gameover_menu = pygame.image.load('Props/gameover.png')
vitoria_menu = pygame.image.load('Props/victory.png')

#BOTÕES E BASES
botoes = pygame.image.load('Props/botoes.png')
cancelar_selecao = pygame.image.load('Selecao/botao-cancelarselecao.png')
desenvolvedores = pygame.image.load('Props/desenvolvedores.png')
voltar = pygame.image.load('Props/voltar.png')
comojogar = pygame.image.load('Props/como_jogar.png')

#TESTE
botaoteste_conectado = pygame.image.load('Props/botaoteste_conectado.gif')

#CARREGAMENTO DE PARTIDA
conexao = [pygame.image.load('Conexao/1.png'),pygame.image.load('Conexao/2.png'),pygame.image.load('Conexao/3.png'),pygame.image.load('Conexao/4.png'),pygame.image.load('Conexao/5.png'),
            pygame.image.load('Conexao/6.png'),pygame.image.load('Conexao/7.png'),pygame.image.load('Conexao/8.png'),pygame.image.load('Conexao/9.png'),pygame.image.load('Conexao/10.png'),
            pygame.image.load('Conexao/11.png')]

contagem = [pygame.image.load('Conexao/Contagem/1.png'),pygame.image.load('Conexao/Contagem/2.png'),pygame.image.load('Conexao/Contagem/3.png'),pygame.image.load('Conexao/Contagem/4.png'),
            pygame.image.load('Conexao/Contagem/5.png'),pygame.image.load('Conexao/Contagem/6.png'),pygame.image.load('Conexao/Contagem/7.png'),pygame.image.load('Conexao/Contagem/8.png'),
            pygame.image.load('Conexao/Contagem/9.png'),pygame.image.load('Conexao/Contagem/10.png'),pygame.image.load('Conexao/Contagem/11.png'),pygame.image.load('Conexao/Contagem/12.png'),
            pygame.image.load('Conexao/Contagem/13.png'),pygame.image.load('Conexao/Contagem/14.png')]

jogarnovamente = [pygame.image.load('Props/Contador/0.png'),pygame.image.load('Props/Contador/1.png'),pygame.image.load('Props/Contador/2.png'),pygame.image.load('Props/Contador/3.png')]

fundofinal = pygame.image.load('Props/fundofinal.png')

contagemjogo = [pygame.image.load('Conexao/Contagem/Jogo/1.png'),pygame.image.load('Conexao/Contagem/Jogo/2.png'),pygame.image.load('Conexao/Contagem/Jogo/3.png'),pygame.image.load('Conexao/Contagem/Jogo/4.png')]

contageminiciar = [pygame.image.load('Conexao/Contagem/IniciarJogo/1.png'),pygame.image.load('Conexao/Contagem/IniciarJogo/2.png'),pygame.image.load('Conexao/Contagem/IniciarJogo/3.png'),pygame.image.load('Conexao/Contagem/IniciarJogo/4.png')]

atletasfinal = [pygame.image.load('Props/Atletas/A0.png'),pygame.image.load('Props/Atletas/A1.png'),pygame.image.load('Props/Atletas/A2.png'),pygame.image.load('Props/Atletas/A3.png'),
                pygame.image.load('Props/Atletas/A4.png'),pygame.image.load('Props/Atletas/A5.png'),pygame.image.load('Props/Atletas/A6.png')]


fundojogo = [pygame.image.load('Conexao/Contagem/EmJogo/1.png'),pygame.image.load('Conexao/Contagem/EmJogo/2.png'),pygame.image.load('Conexao/Contagem/EmJogo/3.png'),pygame.image.load('Conexao/Contagem/EmJogo/4.png'),
             pygame.image.load('Conexao/Contagem/EmJogo/5.png'),pygame.image.load('Conexao/Contagem/EmJogo/6.png'),pygame.image.load('Conexao/Contagem/EmJogo/7.png'),pygame.image.load('Conexao/Contagem/EmJogo/8.png'),
             pygame.image.load('Conexao/Contagem/EmJogo/9.png'),pygame.image.load('Conexao/Contagem/EmJogo/10.png'),pygame.image.load('Conexao/Contagem/EmJogo/11.png')]

arbitro = pygame.image.load('Conexao/Contagem/EmJogo/arbitro.png')

sprites = [pygame.image.load('Sprites/A1FRENTE.png'), pygame.image.load('Sprites/A1COSTA.png'),
           pygame.image.load('Sprites/A2FRENTE.png'), pygame.image.load('Sprites/A2COSTA.png'),
           pygame.image.load('Sprites/A3FRENTE.png'), pygame.image.load('Sprites/A3COSTA.png'),
           pygame.image.load('Sprites/A4FRENTE.png'), pygame.image.load('Sprites/A4COSTA.png'),
           pygame.image.load('Sprites/A5FRENTE.png'), pygame.image.load('Sprites/A5COSTA.png'),
           pygame.image.load('Sprites/A6FRENTE.png'), pygame.image.load('Sprites/A6COSTA.png')]

spriteinicial = [pygame.image.load('Sprites/SpriteInicial/A0.png'),pygame.image.load('Sprites/SpriteInicial/A1.png'),pygame.image.load('Sprites/SpriteInicial/A2.png'),
                 pygame.image.load('Sprites/SpriteInicial/A3.png'),pygame.image.load('Sprites/SpriteInicial/A4.png'),pygame.image.load('Sprites/SpriteInicial/A5.png'),
                 pygame.image.load('Sprites/SpriteInicial/A6.png')]

spriterespiracao = [pygame.image.load('Sprites/Respiracao/0.png'),pygame.image.load('Sprites/Respiracao/1.png'),pygame.image.load('Sprites/Respiracao/2.png'),
              pygame.image.load('Sprites/Respiracao/3.png'),pygame.image.load('Sprites/Respiracao/4.png'),pygame.image.load('Sprites/Respiracao/5.png')]



musicamenu.play(-1)

########################################################################################################################################################################################################################################################################
#tela_inicial_menu
def fundo_inicio():
    musicatema.stop()
    sair = False 
    while not sair:      
        i = 0
        while i < 12:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #area_botao_jogo
                    if x > 453 and x < 822:
                        if y > 284 and y < 339:
                            click.play()
                            selecao_partida()
                            # Inicia conexão

                    #area_botao_sair
                    if x > 652 and x < 824:
                        if y > 363 and y < 408:
                            click.play()
                            botao_sair()

                    #area_botao_ajuda
                    if x > 453 and x < 620:
                        if y > 361 and y < 408:
                            click.play()
                            botao_ajuda()

                    #area_botao_creditos
                    if x > 1075 and x < 1247:
                        if y > 515 and y < 544:
                            click.play()
                            botao_creditos()

                    #area_botao_ligar_som
                    if x > 1176 and x < 1204:
                        if y > 572 and y < 595:
                            click.play()
                            musicamenu.stop()
                            musicamenu.play(-1)

                    #area_botao_desligar_som
                    if x > 1219 and x < 1246:
                        if y > 573 and y < 599:
                            click.play()
                            musicamenu.stop()

                if event.type == pygame.QUIT:
                    #print("sair")
                    pygame.quit()
            
            screen.blit(fundo_inicio_img[i],(0, 0))
            #botoes
            screen.blit(botoes,(0,0))

            pygame.time.delay(50)
            pygame.display.update()
            i += 1



########################################################################################################################################################################################################################################################################
#tela_selecao
def selecao_partida():
    atleta = 0
    sair = False
    atleta_selecionado = False
    while not sair:      
        i = 0
        while i < 5:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]

                if event.type == pygame.QUIT:
                    #print("sair")
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                        #jogar
                        if x > 475 and x < 825:
                            if y > 540 and y < 600:
                                if atleta == 0:
                                    erro.play()
                                else:
                                    click.play()
                                    match_partida(atleta)
                                

                if event.type == pygame.MOUSEBUTTONDOWN:
                        #voltar
                        if x > 21 and x < 82:
                            if y > 18 and y < 60:
                                click.play()
                                fundo_inicio()
                                

                if event.type == pygame.MOUSEBUTTONDOWN:
                        #cancelar_selecao
                        if x > 180 and x < 243:
                            if y > 141 and y < 219:
                                click.play()
                                atleta = 0
                                atleta_selecionado = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                        #atleta_1
                        if x > 719 and x < 868:
                            if y > 19 and y < 219:
                                selecionar.play()
                                atleta = 1
                                atleta_selecionado = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                        #atleta_2
                        if x > 896 and x < 1045:
                            if y > 79 and y < 283:
                                selecionar.play()
                                atleta = 2
                                atleta_selecionado = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                        #atleta_3
                        if x > 1075 and x < 1226:
                            if y > 160 and y < 362:
                                selecionar.play()
                                atleta = 3
                                atleta_selecionado = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                        #atleta_4
                        if x > 718 and x < 867:
                            if y > 252 and y < 453:
                                selecionar.play()
                                atleta = 4
                                atleta_selecionado = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                        #atleta_5
                        if x > 896 and x < 1046:
                            if y > 315 and y < 515:
                                selecionar.play()
                                atleta = 5
                                atleta_selecionado = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                        #atleta_6
                        if x > 1075 and x < 1226:
                            if y > 394 and y < 595:
                                selecionar.play()
                                atleta = 6
                                atleta_selecionado = True
                            
                    
            screen.blit(fundo_selecao_img[i],(0, 0))
            if atleta_selecionado == False:
                screen.blit(pre_selecao_img[i],(0, 0))
                screen.blit(estrelas_img[i],(0, 0))
                screen.blit(atletas_img[0],(0, 0))
            else:
                screen.blit(estrelas_img[i],(0, 0))
                screen.blit(atletas_img[atleta],(0, 0))
                screen.blit(atletasinfos_img[atleta],(0, 0))
                screen.blit(cancelar_selecao,(0, 0))
            
            pygame.time.delay(50)
            pygame.display.update()
            i += 1



########################################################################################################################################################################################################################################################################              
def botao_sair():
    pygame.quit()



######################################################################################################################################################################################################################################################################## 
def botao_ajuda():
    sair = False 
    while not sair:      
        i = 0
        while i < 12:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    #print("Mouse Movendo X:", x)
                    #print("Mouse Movendo Y:", y)
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if x > 30 and x < 78:
                        if y > 30 and y < 73:
                            click.play()
                            fundo_inicio()

                if event.type == pygame.QUIT:
                    #print("sair")
                    pygame.quit()
            
            screen.blit(fundo_inicio_img[i],(0, 0))
            screen.blit(voltar,(0,0))
            screen.blit(comojogar,(0,0))
            
            pygame.time.delay(50)
            pygame.display.update()
            i += 1



########################################################################################################################################################################################################################################################################
def botao_creditos():
    sair = False 
    while not sair:      
        i = 0
        while i < 11:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if x > 30 and x < 78:
                        if y > 30 and y < 73:
                            click.play()
                            fundo_inicio()

                if event.type == pygame.QUIT:
                    #print("sair")
                    pygame.quit()
            
            screen.blit(fundo_alternativo[i],(0, 0))
            screen.blit(voltar,(0,0))
            screen.blit(desenvolvedores,(0,0))
            
            pygame.time.delay(50)
            pygame.display.update()
            i += 1




########################################################################################################################################################################################################################################################################
#tela_match
def match_partida(atleta):
    global inimigo_conectado
    
    iniciar()

    client.connect(ADDR)
    
    sair = False 
    while not sair:      
        i = 1
        verificarInicio()  # Chama função que verifica se pode começar.
        while i < 10:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]

              #TESTE PARA QUANDO SE CONECTAR
                if event.type == pygame.MOUSEBUTTONDOWN:
                  if x > 1219 and x < 1246:
                      if y > 573 and y < 599:
                            click.play()
                            inimigo_conectado = True
                            

                  if event.type == pygame.QUIT:
                      #print("sair")
                      pygame.quit()
                    
            screen.blit(conexao[i],(0, 0))
            screen.blit(botaoteste_conectado,(0,0))
            screen.blit(atletasinfos_img[atleta],(0, 0))
            #botao-fechar
            if inimigo_conectado == False:
                teste = 0
              #screen.blit(conectando,(0, 0))
            else:
              c = 0
              screen.blit(conexao[10],(0, 0))
              screen.blit(atletasinfos_img[atleta],(0, 0))
              inimigoconectado.play()
              pygame.display.update()
              pygame.time.delay(1000)

              musicamenu.stop()
              onda.play()

              while c < 14:
                screen.blit(conexao[10],(0, 0))
                screen.blit(atletasinfos_img[atleta],(0, 0))
                screen.blit(contagem[c],(0, 0))
                pygame.display.update()
                pygame.time.delay(80)
                c += 1
              enviar_atleta(atleta) # aqui envia o atleta escohlido
              fundo_jogo(atleta)
              pygame.display.update()
 
            pygame.time.delay(70)
            pygame.display.update()
            i += 1



########################################################################################################################################################################################################################################################################
#tela_jogo_jogar
def fundo_jogo(atleta):
    musicamenu.stop()
    global localizacao_inimigo
    global atleta_inimigo
    global posicao_aliado

    

    localizacao_inimigo = 20
    posicao_aliado = 20
    barraaliada = 0
    barrainimiga = 0
    c = 0

    #PONTUACAO ALIADA    
    #vida = 3
    #pontuacao = 0
    #pontuacao_vida = str(pontuacao) + "-" + str(vida)
    atletafrente = 0
    atletacosta = 0
    if atleta == 1:
        atletafrente = 0
        atletacosta = 1
    if atleta == 2:
        atletafrente = 2
        atletacosta = 3
    if atleta == 3:
        atletafrente = 4
        atletacosta = 5
    if atleta == 4:
        atletafrente = 6
        atletacosta = 7
    if atleta == 5:
        atletafrente = 8
        atletacosta = 9
    if atleta == 6:
        atletafrente = 10
        atletacosta = 11

    sair = False
    i = 0
    j = 0
    k = 0
    respiracao = 200
    respiracaoaux = 1
    aux = 1
    
    while i < 4:
            screen.blit(fundojogo[i],(0, 0))
            screen.blit(spriteinicial[atleta],(20, 480))
            #INIMIGO
            screen.blit(spriteinicial[atleta_inimigo],(20, 420))
            screen.blit(barraa,(0,0))
            screen.blit(barrai,(0,0))
            screen.blit(spriterespiracao[respiracaoaux],(20, 520))
            screen.blit(contageminiciar[0],(0, 0))
            screen.blit(contagemjogo[i],(0, 0))
            pygame.time.delay(70)
            pygame.display.update()
            i += 1
            
    musicatema.play(-1)
    while j < 4:
            screen.blit(fundojogo[j],(0, 0))
            screen.blit(spriteinicial[atleta],(20, 480))
            #INIMIGO
            screen.blit(spriteinicial[atleta_inimigo],(20, 420))
            screen.blit(barraa,(0,0))
            screen.blit(barrai,(0,0))
            screen.blit(spriterespiracao[respiracaoaux],(20, 520))
            screen.blit(contageminiciar[j],(0, 0))
            if j < 3:
                somcontagem.play()
            else:
                comecoujogo.play()
            pygame.display.update()
            pygame.time.delay(1000)
            j += 1
    
    while not sair:
        while k < 11:
            if k == 10:
                k = 0
                
            pygame.display.update()
            screen.blit(fundojogo[k],(0, 0))
            #INIMIGO
            screen.blit(spriteinicial[atleta_inimigo],(localizacao_inimigo, 420))
            if posicao_aliado == 20: 
                screen.blit(spriteinicial[atleta],(posicao_aliado, 480))
            elif posicao_aliado >= 1100:
                onda.play()

                while c < 14:
                    screen.blit(fundojogo[k],(0, 0))
                    screen.blit(contagem[c],(0, 0))
                    pygame.display.update()
                    pygame.time.delay(80)
                    c += 1
                vitoria(atleta)
                pygame.display.update()

            #INIMIGO
            elif localizacao_inimigo >= 1100:
                while c < 14:
                    screen.blit(fundojogo[k],(0, 0))
                    screen.blit(contagem[c],(0, 0))
                    pygame.display.update()
                    pygame.time.delay(80)
                    c += 1
                derrota(atleta)
                pygame.display.update()

            else:
                screen.blit(spriteinicial[atleta],(posicao_aliado, 480))
                
            screen.blit(barra_aliada[barraaliada],(0, 0))
            screen.blit(barra_inimiga[barrainimiga],(0, 0))
            screen.blit(barraa,(0,0))
            screen.blit(barrai,(0,0))
            screen.blit(spriterespiracao[respiracaoaux],(posicao_aliado, 520))

   
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    
                if event.type == pygame.KEYDOWN:
                    tecla = pygame.key.name(event.key)
                    if tecla == 'space':
                        if respiracao >= 20:
                            screen.blit(fundojogo[k],(0, 0))
                            #INIMIGO
                            screen.blit(barra_aliada[barraaliada],(0, 0))
                            screen.blit(barra_inimiga[barrainimiga],(0, 0))
                            screen.blit(barraa,(0,0))
                            screen.blit(barrai,(0,0))
                            screen.blit(spriteinicial[atleta_inimigo],(localizacao_inimigo, 420))
                            screen.blit(spriterespiracao[respiracaoaux],(posicao_aliado, 520))
                            if aux == 1:
                                screen.blit(sprites[atletacosta],(posicao_aliado, 460))
                                aux -= 1
                            else:
                                screen.blit(sprites[atletafrente],(posicao_aliado, 440))
                                aux += 1
                                
                            posicao_aliado += 40 
                            respiracao -= 20

                            ## Vamos mandar mensagem da posição atual do nosso client. 
                            ## Pontuacao_vida passa ser posicao_aliado só
                            print("ENVIANDO POSICAO PARA TODOS!")
                            enviar_mensagem(posicao_aliado)

                        else:
                            screen.blit(fundojogo[k],(0, 0))
                            #INIMIGO
                            screen.blit(barra_aliada[barraaliada],(0, 0))
                            screen.blit(barra_inimiga[barrainimiga],(0, 0))
                            screen.blit(barraa,(0,0))
                            screen.blit(barrai,(0,0))
                            screen.blit(spriteinicial[atleta_inimigo],(localizacao_inimigo, 420))
                            screen.blit(spriteinicial[atleta],(posicao_aliado, 480))
                            screen.blit(spriterespiracao[respiracaoaux],(posicao_aliado, 520))
                            
                    elif tecla == 'f':
                        if respiracao <= 200:
                            respiracao += 100

                    # ESTAGIOS BARRA ALIADA
                    if(posicao_aliado >= 128 and posicao_aliado < 236):
                        barraaliada = 1
                    elif(posicao_aliado >= 236 and posicao_aliado < 344):
                        barraaliada = 2
                    elif(posicao_aliado >= 344 and posicao_aliado < 432):
                        barraaliada = 3
                    elif(posicao_aliado >= 432 and posicao_aliado < 560):
                        barraaliada = 4
                    elif(posicao_aliado >= 560 and posicao_aliado < 668):
                        barraaliada = 5
                    elif(posicao_aliado >= 668 and posicao_aliado < 776):
                        barraaliada = 6
                    elif(posicao_aliado >= 776 and posicao_aliado < 884):
                        barraaliada = 7
                    elif(posicao_aliado >= 884 and posicao_aliado < 992):
                        barraaliada = 8
                    elif(posicao_aliado >= 992 and posicao_aliado < 1100):
                        barraaliada = 9

                    # ESTAGIOS BARRA INIMIGA
                    if(localizacao_inimigo >= 128 and localizacao_inimigo < 236):
                        barrainimiga = 1
                    elif(localizacao_inimigo >= 236 and localizacao_inimigo < 344):
                        barrainimiga = 2
                    elif(localizacao_inimigo >= 344 and localizacao_inimigo < 432):
                        barrainimiga = 3
                    elif(localizacao_inimigo >= 432 and localizacao_inimigo < 560):
                        barrainimiga = 4
                    elif(localizacao_inimigo >= 560 and localizacao_inimigo < 668):
                        barrainimiga = 5
                    elif(localizacao_inimigo >= 668 and localizacao_inimigo < 776):
                        barrainimiga = 6
                    elif(localizacao_inimigo >= 776 and localizacao_inimigo < 884):
                        barrainimiga = 7
                    elif(localizacao_inimigo >= 884 and localizacao_inimigo < 992):
                        barrainimiga = 8
                    elif(localizacao_inimigo >= 992 and localizacao_inimigo < 1100):
                        barrainimiga = 9

                    # ESTAGIOS BARRA RESPIRACAO
                    if(respiracao >= 0 and respiracao < 20):
                        respiracaoaux = 0
                    elif(respiracao >= 20 and respiracao <= 80):
                        respiracaoaux = 5
                    elif(respiracao > 80 and respiracao <= 120):
                        respiracaoaux = 4
                    elif(respiracao > 120 and respiracao <= 160):
                        respiracaoaux = 3
                    elif(respiracao > 160 and respiracao <= 200):
                        respiracaoaux = 2
                    elif(respiracao >= 200):
                        respiracaoaux = 1
                    
                    pygame.display.update()
            pygame.time.delay(50)
            k += 1


########################################################################################################################################################################################################################################################################
def carregamento(atleta):
    j = 0
    c = 0
    while j < 4:
        if j == 3:
            screen.blit(jogarnovamente[j],(0, 0))
            pygame.display.update()
            onda.play()
            while c < 14:
                    screen.blit(fundofinal,(0, 0))
                    screen.blit(contagem[c],(0, 0))
                    pygame.display.update()
                    pygame.time.delay(80)
                    c += 1
            fundo_jogo(atleta)
            pygame.display.update()
            
        else:
            screen.blit(jogarnovamente[j],(0, 0))
            pygame.display.update()
            somcontagem.play()
            pygame.time.delay(1000)
            j += 1



########################################################################################################################################################################################################################################################################
def derrota(atleta):
    i = 0
    j = 0
    c = 0
    global atleta_inimigo
    derrotasom.play()
    while i < 4:
            screen.blit(fundo_alternativo[i],(0, 0))
            screen.blit(gameover_menu,(0,0))
            screen.blit(atletasfinal[atleta],(592, 257))
            screen.blit(atletasfinal[atleta_inimigo],(454, 292))
            screen.blit(contagemjogo[i],(0, 0))
            pygame.time.delay(70)
            pygame.display.update()
            i += 1
    musicatema.stop()
    musicamenu.play()
    sair = False 
    
    while not sair:
        screen.blit(fundofinal,(0,0))
        screen.blit(gameover_menu,(0,0))
        screen.blit(atletasfinal[atleta_inimigo],(592, 257))
        screen.blit(atletasfinal[atleta],(454, 292))
        pygame.display.update()
        pygame.time.delay(5000)
        carregamento(atleta)



########################################################################################################################################################################################################################################################################
def vitoria(atleta):
    i = 0
    global atleta_inimigo
    vitoriasom.play()
    while i < 4:
            screen.blit(fundo_alternativo[i],(0, 0))
            screen.blit(vitoria_menu,(0,0))
            screen.blit(atletasfinal[atleta],(592, 257))
            screen.blit(atletasfinal[atleta_inimigo],(454, 292))
            screen.blit(contagemjogo[i],(0, 0))
            pygame.time.delay(70)
            pygame.display.update() 
            i += 1
    musicatema.stop()
    musicamenu.play()
    sair = False 
    while not sair:
        screen.blit(fundofinal,(0,0))
        screen.blit(vitoria_menu,(0,0))
        screen.blit(atletasfinal[atleta],(592, 257))
        screen.blit(atletasfinal[atleta_inimigo],(454, 292))
        pygame.display.update()
        pygame.time.delay(5000)
        carregamento(atleta)


########################################################################################################################################################################################################################################################################

        
def main():
    fundo_inicio()
main()
