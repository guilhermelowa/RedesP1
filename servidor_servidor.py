import socket
from util_comUDP import *
# Achar jeito melhro pra importar
from sensor_sensor import *
from threading import Thread
from util_protocoloCom import *
from queue import Queue

#import comunicacaoTCP

class Servidor:

    def __init__(self):
        # Dados
        self.sensores = {}
        self.id_sensores = []
        self.medicos = {}
        self.endereco_medicos = []

        # UDP
        self.socketUDP = abrirSocketUDP(int(input("Digite a porta da comunicacao UDP: ")))
        threadOuvirUDP = Thread(target = self.receber_mensagem, args=(self.socketUDP,))
        threadOuvirUDP.start()

        # TCP
        # Abrir bocal e ouvir até receber nova conexão
        self.socketTCP = abrirSocketTCP(int(input("Digite a porta da comunicao TCP: ")))
        self.socketTCP.listen(10)
        # Ao receber nova conexão, aceita a conexão e coloca o socket desta na fila lista_conexoes
        lista_conexoes = Queue()
        thread_abrir_conexoes = Thread(target = aceitar_conexoes, args=(self.socketTCP, lista_conexoes))
        thread_abrir_conexoes.start()
        
        # Socket é retirado da fila e passado para função de ouvir, p/ que servidor registre as mensagens do socket.
        # Recebe tupla contendo socket e endereço
        bocal = lista_conexoes.get()
        endereço = bocal[1]
        bocal = bocal[0]
        thread_ouvir_TCP = Thread(target = self.receber_mensagem, args=(bocal, endereço))
        thread_ouvir_TCP.start()

    def receber_mensagem(self, bocal, endereço=('','')):
        while True:
            mensagem, addr = ouvir_socket(bocal)
            print("Recebido: ", mensagem, end="|")       
            # Caso seja UDP ele recebeu msg,endereço. Caso seja TCP recebeu só msg. Diferenciar:
            if (None == addr):
                print("De: ", endereço)
                porta = endereço[1]
                endIP = str(endereço[0])
            else:
                print("De: ", addr)
                porta = addr[1]
                endIP = str(addr[0])

            if (mensagem == None):
                self.repita_mensagem(end_IP, bocal)
            else:
                print(" - - - - Executando comando: " + mensagem[0] + " - - - - ")
                if ('0' == mensagem[0]):
                    self.cadastrarSensor(mensagem[1:], bocal)
                elif ('1' == mensagem[0]):
                    self.atualizarSensor(mensagem[1:])
                elif ('2' == mensagem[0]):
                    self.cadastrarMedico(mensagem[1:])
                elif ('3' == mensagem[0]):
                    self.atualizarMedico(mensagem[1:])
                else:
                    self.repitaMensagem(endIP, porta)

    def cadastrarSensor(self, mensagem, bocal):
        # Separa o CPF do ID        
        cpf = mensagem.split(caracter_separador)
        identificador = cpf[1]
        cpf = cpf[0]

        # Cadastra novo sensor
        novoSensor = Sensor(cpf, identificador)
        self.sensores[identificador] = novoSensor
        print("Cadastrado sensor: " + self.sensores[identificador].cpf)

        # Adiciona ID do sensor na lista de sensores
        self.id_sensores.append(identificador)
    
        # Adiciona endereço do sensor na lista de endereços
#        endereço_completo = str(endereço) + ";" + str(porta)
        #self.endereco_sensores.append(endereço_completo)
        #print("No endereço: ", endereço_completo)
        
        # Resposta ao cadastro
        resposta = '0'
        # Envia resposta final do servidor ao sensor, antes de fechar conexão
        enviar_TCP(resposta, bocal)
        print("Enviado: " + resposta)
        
    def atualizarSensor(self, mensagem):
        # Atualiza os dados do sensor correspondente ao endereço recebido
        mensagem = mensagem.split(caracter_separador)
        identificador = mensagem[0]
        self.sensores[identificador].bpm = mensagem[1]
        self.sensores[identificador].pressao = int(mensagem[2])
        self.sensores[identificador].movimento = bool("True" == mensagem[3])
        print("Atualizando sensor: " + identificador)
        print("BPM: " + self.sensores[identificador].bpm + " Pressao: " + str(self.sensores[identificador].pressao) + " Movimento: " + str(self.sensores[identificador].movimento))
        
    def cadastrar_medico(self, mensagem):
        print("Cadatrar medico")
                
    def autenticar_medico(self, mensagem):
        print("Autenticar medico")

    def enviar_risco(self, mensagem):
        print("Atualizar medico")

    def enviar_monitorado(self, mensagem):
        print("Enviando paciente monitorado")

    def repitaMensagem(self, mensagem):
        print("Repita mensagem")
            
            
            
            
servidor = Servidor()
