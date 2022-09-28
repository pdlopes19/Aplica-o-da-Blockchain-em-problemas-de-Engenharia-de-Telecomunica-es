from hashlib import sha256
from datetime import datetime
import time
import socket
import os
import subprocess
import matplotlib.pyplot as plt
import numpy as np

secLevel = ''  # Nível de segurança. Este é denotado pelo número de zeros no início do hash, quanto mais 0's maior a segurança e maior o poder de processamento necessário para obtenção do nonce.
nomearquivo = 'RelatorioMensal-{}.txt'.format(datetime.now().strftime('%m-%Y'))
arquivo = open(nomearquivo, 'w')

class Blockchain:
    
    # Inicialização da classe: cria duas listas de blocos ( encriptados e não encriptados ) e o primeiro bloco ( gênesis )
    def __init__(self):
        self.blocks = []
        self.blocks_no_encrypt = []
        self.ul_data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.dl_data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.block_data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.cn_data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.set_genesis_block()

    
    # Criação do bloco gênesis, com data e horários atuais e hash anterior e indice 0
    # É o primeiro bloco da cadeia, como padrão, sua informação será "Genesis block", o índice é 0, por ser o primeiro e o hash anterior também, pois inexiste bloco anterior.
    def set_genesis_block(self):
        data1 = 'Genesis block'
        data2 = 'Genesis block'
        data3 = 'Genesis block'
        dt_object = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        prev_hash = 0
        index = 0
        self.hash_block(data1, data2, data3, dt_object, prev_hash, index)

    
    # Formação de um bloco, inclui a mineração do nonce
    # O bloco é a entidade que guarda a informação, que não será violada nem alterada. Seu formato foi padronizado como: Timestamp // Data // Previous Hash // Index // Nonce
    # O nonce é um número que adicionado ao bloco alterará seu hash até que seja atingido o número de zeros consecutivos ( Nível de segurança ) estipulado. É preciso "minerá-lo" usando processamento computacional. 
    def hash_block(self, data1, data2, data3, dt_object, prev_hash, index):
        hash = ''
        nonce = 1
        print('Obtaining nonce...')
        while not self.is_hash_valid(hash):
            block = '{} // {} // {} // {} // {} // {} // {}'.format(dt_object, data1, data2, data3, prev_hash, index, nonce)
            hash = sha256(block.encode()).hexdigest()
            nonce += 1
        os.system('cls||clear')
        print('Created block:')
        print('\nBlock [{}]: {}\n'.format(index,block))
        self.blocks.append(hash)
        self.blocks_no_encrypt.append(block)
        arquivo = open(nomearquivo, 'a')
        arquivo.write(block+'\n')
        arquivo.close()

    # Aquisição do hash anterior
    # O Previous Hash é necessário para que haja relação entre os blocos, formando uma cadeia. Caso o bloco anterior seja alterado, seu hash será alterado. Como o bloco atual é formado, também, pelo hash do anterior, ele também será alterado
    def get_last_hash(self):
        return self.blocks[-1]

    
    # Teste de validade do hash, de acordo com o nível de segurança escolhido
    # Se o hash gerado possuir N zeros consecutivos, de acordo com o nível de segurança, ele será um hash válido.
    def is_hash_valid(self, hash):
        return hash.startswith(secLevel)

    # Adição de um novo bloco
    def add_new_block(self, data1, data2, data3, dt_object):
        index = len(self.blocks)
        prev_hash = self.get_last_hash()
        self.hash_block(data1, data2, data3, dt_object, prev_hash, index)

    # Listagem de blocos encriptados
    def get_all(self):
        i = 0
        os.system('cls||clear')
        print('\nEncrypted blocks:')
        while(i < len(self.blocks)):
            print('[{}] '.format(i) + self.blocks[i])
            i+=1

    # Listagem de blocos não encriptados
    def get_all_no_encrypt(self):
        i = 0
        print('\nNon-Encrypted blocks:')
        while(i < len(self.blocks_no_encrypt)):
            print('[{}] '.format(i) + self.blocks_no_encrypt[i])
            i+=1

    # Função do menu para adição de blocos em uma Blockchain genérica
    def add_blocks(self):
        i = 1
    
        condicao = True
        while(condicao):
            
            os.system('cls||clear')
            print('Block format:')
            print('Block [index]: Data // Timestamp // Previous hash // Index // Nonce\n')
            print('Block [i] data: 0, to quit.\n')
            data1 = input('Block [{}] data: '.format(i))
            data2 = 0
            data3 = 0
            
            if data1 == '0':
                condicao = False
            else:
                self.add_new_block(data1, data2, data3)
                os.system('PAUSE')
                i+=1

    # Função do menu para busca de blocos em uma Blockchain genérica
    def search_blocks(self):

        cont = 0
        date = 'x'
        
        os.system('cls||clear')
        print('You can put on Date of info:')
        print()
        print('DD - search based only on day')
        print('DD/MM - search based on day and month')
        print('DD/MM/YYYY - search based on day, month and year')
        print('DD/MM/YYYY hh - search based on day, month, year and hour')
        print('DD/MM/YYYY hh:mm - search based on day, month, year, hour and minute')
        print()

        while(len(date) < 2 or len(date) > len('DD/MM/YYYY hh:mm:ss')):
            date = input('Date of info: ')
        
        os.system('cls||clear')        
        for i in range(0, len(self.blocks_no_encrypt)):
            date_block = ''
            block = self.blocks_no_encrypt[i]
            for j in range(0,len(date)):
                date_block += block[j]

            if( date == date_block ):
                print(block)
                date_block = ''
                cont += 1

        if(cont == 0):
            print('\nNo block found')
        else:
            print('\nFound blocks: {}'.format(cont))
    
    def show_graphics_dl(self,m=0):

        plt.figure(1)
        self.threat_info()
        label = ('01', '02', '03', '04', '05', '06', '07', '08',
         '09', '10', '11', '12', '13', '14', '15', '16',
         '17', '18', '19', '20', '21', '22', '23', '24',
         '25', '26', '27', '28', '29', '30', '31')

        index = np.arange(len(label))
        graph1 = plt.bar(index, self.dl_data, xerr = 0.75, bottom = 0)
        
        plt.xlabel('Day', fontsize=10)
        plt.ylabel('Download [Mbits/s]', fontsize=10)
        plt.xticks(index, label, fontsize=6, rotation=30)
        plt.title('Average Download Data')
        plt.grid()

        for i in range(0,31):
            plt.annotate(str(round(self.dl_data[i],3)),(i,self.dl_data[i]+0.1), fontsize = 6)

        plt.savefig('download-data-{}.pdf'.format(m), dpi=199)
        plt.close(1)

    def show_graphics_ul(self,m=0):

        plt.figure(2)
        
        label = ('01', '02', '03', '04', '05', '06', '07', '08',
         '09', '10', '11', '12', '13', '14', '15', '16',
         '17', '18', '19', '20', '21', '22', '23', '24',
         '25', '26', '27', '28', '29', '30', '31')

        index = np.arange(len(label))
        
        graph2 = plt.bar(index, self.ul_data, xerr = 0.75, bottom = 0)

        plt.xlabel('Day', fontsize = 10)
        plt.ylabel('Upload [Mbits/s]', fontsize = 10)
        plt.xticks(index, label, fontsize = 6, rotation = 30)
        plt.title('Average Upload Data')
        plt.grid()

        for i in range(0,31):
            plt.annotate(str(round(self.ul_data[i],3)),(i,self.ul_data[i]+0.1), fontsize = 6)

        plt.savefig('upload-data-{}.pdf'.format(str(m)), dpi=199)
        plt.close(2)


    def show_graphics_cn(self,m=0):

        plt.figure(3)
        
        label = ('01', '02', '03', '04', '05', '06', '07', '08',
         '09', '10', '11', '12', '13', '14', '15', '16',
         '17', '18', '19', '20', '21', '22', '23', '24',
         '25', '26', '27', '28', '29', '30', '31')

        index = np.arange(len(label))
        
        graph2 = plt.bar(index, self.cn_data, xerr = 0.75, bottom = 0)

        plt.xlabel('Day', fontsize = 10)
        plt.ylabel('Connection', fontsize = 10)
        plt.xticks(index, label, fontsize = 6, rotation = 30)
        plt.title('Connection Data')
        plt.grid()

        for i in range(0,31):
            plt.annotate(str(self.cn_data[i]),(i,self.cn_data[i]), fontsize = 6)

        plt.savefig('connection-data-{}.pdf'.format(str(m)), dpi=199)
        plt.close(3)

    # Formação de uma blockchain com dados diagnósticos da rede em que a máquina está conectada, criando um relatório mensal
    def network(self):

        contc = 0
        contdesc = 0
        somad = 0
        somau = 0
        diainicio = int(datetime.now().strftime('%d'))
        mesinicio = int(datetime.now().strftime('%m'))

        for i in range (0,3):            
            data1 = '{}'.format(self.downloadData())
            
            if data1 ==  'Download: No data':
                data2 = 'Upload: No data'
                status = 'Status da rede: Desconectado'
                data1f = 0
                data2f = 0
            else:
                data2 = '{}'.format(self.uploadData())
                if data1 != 'Download: No data':
                    data1f = float(data1[10]+ data1[11] + data1[12] + data1[13])
                    somad += data1f                        

                if data2 != 'Upload: No data':
                    data2f = float(data2[8] + data2[9] + data2[10] + data2[11])
                    somau += data2f
                    if int(datetime.now().strftime('%m')) == mesinicio:
                        self.average_download(data1f)
                        self.average_upload(data2f)
                        self.blocks_number_date()

                    
            if not(data1 == 'Download: No data' and data2 == 'Upload: No data'):
                status = 'Status da rede: Conectado'
                contc += 1
                if int(datetime.now().strftime('%m')) == mesinicio:
                    self.average_connected()
                
            else:
                time.sleep(100)
                contdesc += 1
                
            if int(datetime.now().strftime('%m')) == mesinicio:
                self.add_new_block(status, data1, data2, datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        
        os.system('cls||clear')
                       
        blockchain.get_all_no_encrypt()
        os.system('PAUSE')
        arquivo = open(nomearquivo, 'a')
        arquivo.write('\n\nObtained Results:'+'\nConnected: {:.4}%'.format(contc*1.0/(contc+contdesc)*100)+'\nDisconnected: {:.4}%\n'.format(contdesc*1.0/(contc+contdesc)*100)+
                      '\nAverage Download Speed: {:.4} MBits/s'.format(somad*1.0/contc)+
                      '\nAverage Upload Speed: {:.4} MBits/s'.format(somau*1.0/contc))
        
        arquivo.close()
        print(self.dl_data)
        print(self.ul_data)
        print(self.block_data)
        self.show_graphics_dl(int(datetime.now().strftime('%m'))-1)
        self.show_graphics_ul(int(datetime.now().strftime('%m'))-1)
        self.show_graphics_cn(int(datetime.now().strftime('%m'))-1)

    def average_download(self,dl):
        dia = int(datetime.now().strftime('%d'))
        self.dl_data[dia-1] += dl                             
        print(self.dl_data)

    def average_upload(self,ul):
        dia = int(datetime.now().strftime('%d'))
        self.ul_data[dia-1] += ul 
        print(self.ul_data)

    def average_connected(self):
        dia = int(datetime.now().strftime('%d'))
        self.cn_data[dia-1] += 100
        print(self.cn_data)

    def blocks_number_date(self):
        dia = int(datetime.now().strftime('%d'))
        self.block_data[dia-1] += 1                            
        print(self.block_data)

    def threat_info(self):
        for i in range(0,len(self.dl_data)):
            if self.block_data[i] != 0:
                self.dl_data[i] = self.dl_data[i]/self.block_data[i]

        for i in range(0,len(self.ul_data)):
            if self.block_data[i] != 0:
                self.ul_data[i] = self.ul_data[i]/self.block_data[i]

        for i in range(0,len(self.cn_data)):
            if self.block_data[i] != 0:
                self.cn_data[i] = self.cn_data[i]/self.block_data[i]

        print(self.dl_data)
        print(self.ul_data)
        print(self.cn_data)
            
    # Número de blocos criados
    def blocks_number(self):
        return str(len(self.blocks))

    def downloadData(self):
        out = ''
        print('Testing download speed...')
        try:
            out = str(subprocess.check_output("python _speedtest.py", shell=True))
        except subprocess.CalledProcessError as e:
            print(e.output)
        data = ''
        
        for i in range(0, len(out)):
            if(out[i] == 'D' and out[i+1] == 'o' and out[i+2] == 'w' and out[i+3] == 'n'):
                for j in range(i, i+22):
                    data = data+out[j]

        if len(data) < 2:
            data = 'Download: No data'

        print(data)    
        return data

    def uploadData(self):
        out = ''
        print('Testing upload speed...')
        try:
            out = str(subprocess.check_output("python _speedtest.py", shell=True))
        except subprocess.CalledProcessError as e:
            print(e.output)
        data = ''

        for i in range(0, len(out)):
            if(out[i] == 'U' and out[i+1] == 'p' and out[i+2] == 'l' and out[i+3] == 'o'):
                for j in range(i, i+20):
                    data = data+out[j]
                    
        if len(data) < 2:
            data = 'Upload: No data'
            
        print(data)
        return data

    def autolabel(rects, xpos='center'):
        ha = {'center': 'center', 'right': 'left', 'left': 'right'}
        offset = {'center': 0, 'right': 1, 'left': -1}

        for rect in rects:
            height = rect.get_height()
            plt.annotate('{}'.format(height),
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(offset[xpos]*3, 3),
            textcoords="offset points",
            ha=ha[xpos], va='bottom',size = 5.3)
            
if __name__ == '__main__':
        
    i = 0 
    n = -1
    operacao = -1
    
    while(n < 1 or n > 10): 
        n = int(input('Security level (1-10): '))
        
    while(i<n):
        secLevel += '0'
        i+=1
    blockchain = Blockchain()

    os.system('PAUSE')

    os.system('cls||clear')
        
    while(True):

        os.system('cls||clear')
        
        print('Menu')
        print()
        print('1 - Add a block')
        print('2 - Blocks list')
        print('3 - Search informations')
        print('4 - Network status validation')
        print('0 - Exit\n')
        
        while(operacao < 0 or operacao > 4):
            operacao = int(input('Operation: '))

        if(operacao == 0):
            arquivo = open(nomearquivo, 'a')
            arquivo.write('\nTotal number of blocks: '+blockchain.blocks_number()+'\n')
            arquivo.close()
            exit(0)

        if(operacao == 1):
            operacao = -1
            blockchain.add_blocks()
            print()
            os.system('PAUSE')

        if(operacao == 2):
            operacao = -1
            blockchain.get_all()
            blockchain.get_all_no_encrypt()
            print()
            os.system('PAUSE')

        if(operacao == 3):
            operacao = -1
            blockchain.search_blocks()
            print()
            os.system('PAUSE')

        if(operacao == 4):
            operacao = -1
            blockchain.network()
            os.system('PAUSE')
            exit(0)
            
                           
