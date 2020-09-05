#!/usr/bin/env python3
"""
CONFIGURAÇÕES GLOBAIS
Módulo contendo funções comuns a todos os
scripts do 'notas_online', bem como variáveis
do professor, tais como turmas, disciplinas, etc.

Autor: Pedro P. Bittencourt
Contato: contato@pedrobittencourt.com.br
Site: pedrobittencourt.com.br
"""


###########
# IMPORTS #
###########

from selenium import webdriver
from getpass import getpass
import logging
import os
import sys
import platform


################
# MAIN PROGRAM #
################

class Main:

    def __init__(self, programa):
        """
        Exibe mensagem de início do programa e grava os
        atributos essenciais: credenciais do usuário
        (username, password), logger e driver
        """

        self.programa = programa

        # mensagem de BOAS VINDAS
        print('WELCOME!!\n')

        # credenciais do usuário
        self.username = str(input('Usuário: _ '))
        self.password = getpass('Senha: _ ')

        # inicializa o logger
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s  %(name)-12s %(levelname)s %(message)s',
            datefmt='%d-%b-%Y %H:%M:%S',
            filename=os.path.join(file_dir, 'notasonline.log'),
            filemode='a'
        )
        self.logger = logging.getLogger(self.programa)
        self.logger.setLevel(logging.INFO)
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s > %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        self.logger.addHandler(console)

        # inicializa o driver
        # o executável depende do SO do usuário
        drivers_dir = os.path.join(parent_dir, 'drivers')
        user_os = platform.system()
        if user_os == 'Linux':
            driver_exe = 'chromedriver'
        elif user_os == 'Windows':
            driver_exe = 'chromedriver.exe'
        else:
            pass
        driver_path = os.path.join(drivers_dir, driver_exe)
        self.driver = webdriver.Chrome(executable_path=driver_path)


    def login(self) -> bool:
        """
        Abre página de login, preenche com as credenciais do usuário
        e verifica se a url de retorno corresponde à página inicial
        do notas online, retornando True ou False.
        """
        # abre página de login
        self.driver.get('https://www.notasonline.com/pages/nol_logon.asp')

        # preenche credenciais do usuário
        self.driver.find_element_by_id('txtLogin').send_keys(self.username)
        self.driver.find_element_by_id('txtPassword').send_keys(self.password)
        self.driver.find_element_by_id('frmForm').submit()

        # verifica se o login foi efetuado, através da url atual
        if self.driver.current_url == 'https://www.notasonline.com/pages/home_teacher.asp':
            return True
        else:
            return False


    def errorquit(msg: str = 'ERRO NÃO ESPECIFICADO') -> str:
        """
        Quando falhar numa requisição importante, exibe
        mensagem de erro, registra no log, fecha o driver
        e encerra o programa.
        """
        self.logger.error(f'Não foi possível continuar devido ao seguinte problema: {msg}.')
        self.logger.info('O programa será encerrado agora. Verifique o registro para detalhes!')
        self.driver.quit()
        sys.exit(1)


#############
# VARIABLES #
#############

# caminho do arquivo
abs_path = os.path.abspath(__file__)
# diretório do arquivo
file_dir = os.path.dirname(abs_path)
# diretório parente
parent_dir = os.path.dirname(file_dir)

# Daqui para baixo, variáveis preenchidas via 'install.py'

diarios = {
    '6ADG': '591D1214-CEC7-4511-B99D-38B64C224704',
    '6BDG': '2C350D3D-560B-4FE3-A6B8-9C3B4C1D7BB2',
    '7ADG': '860B570A-9F38-4384-93BA-8905AE76B98C',
    '8ADG': '570678BF-C4FD-4E26-BB11-9C19AA9BB457',
    '8AFIS': '6CDA5EAA-BB3C-4029-8F27-674B385E4689',
    '9ADG': 'C35A5E17-0299-4E6F-86A5-3BFCEAE34E87',
    '9AFIS': 'D61E769F-C1BF-4720-9F0F-28DB24889C73',
    '1AFIS': '993A3639-2A70-4748-8BB9-CF4BF24131FE',
    '1AGMT': '80A71A6F-1ED2-4267-8E93-FD74B5B77EA4',
    '2AFIS': '88A1A059-12DE-4676-9A28-E07EB47DE913',
    '2AGMT': 'E12A8904-21D6-4E1B-A1DA-99A66EAF400F',
    '3AFIS': '930B8C3A-450A-405D-A1ED-725FD1FC19E8',
    '3AGMT': 'E08722EA-267E-42DE-875E-35944FA616D9',
}
disciplinas = {
    'DG': 'Desenho Geométrico / Pedro Pompermayer Bittencourt',
    'FIS': 'Física / Pedro Pompermayer Bittencourt',
    'GMT': 'Geometria / Pedro Pompermayer Bittencourt',
}
turmas = {
    '6A': 'Sexto Ano / 1M6A / Manhã',
    '6B': 'Sexto Ano / 1M6B / Manhã',
    '7A': 'Sétimo Ano / 1M7A / Manhã',
    '8A': 'Oitavo Ano / 1M8A / Manhã',
    '9A': 'Nono Ano / 1M9A / Manhã',
    '1A': 'Primeira Série / 2M1A / Manhã',
    '2A': 'Segunda Série / 2M2A / Manhã',
    '3A': 'Terceira Série / 2M3A / Manhã',
}
ocorrencias = {
    'A': ['C6AE796F-E4BA-47C2-A725-98C36CD12E11', 'Não apresentou a lição de casa'],
    'B': ['AE890406-F8E3-442D-BF98-44498DC1F517', 'Lição de casa incompleta'],
    'C': ['743091FC-5899-477C-8C68-35A55343B70F', 'Não entregou trabalho (1a data)'],
    'D': ['733DA849-6942-44C4-B170-F3B7A97F518A', 'Não entregou trabalho (2a data)'],
    'E': ['E6F973C7-8146-450F-AE4F-02D2C2D451D1', 'Trabalho fora das especificações solicitadas.'],
    'F': ['7A80526B-387F-4743-87AF-DB2666CE6639', 'Não trouxe material'],
    'G': ['80860D8F-1152-43BE-ABE3-FCE16987F413', 'Atraso'],
    'H': ['3F67CD55-86B0-4C5F-9502-83F04CF3EE5A', 'Não fez atividades em classe'],
    'I': ['4B55A896-FDA8-484C-81C5-882E140C290E', 'Sem uniforme (Educação Física)'],
    'J': ['31F0C7AE-8528-463E-81E0-EF4B4F9A65C7', 'Outras ocorrências'],
    'K': ['40A94F21-D8A3-408F-AA30-10BE6F7BCE49', 'Não compareceu ao plantão.'],
    'L': ['B43C3E32-2BDC-47C3-90A3-B7004920E0CC', 'Não compareceu à aula - período intensivo de estudos'],
    'M': ['E8E54836-8579-49CC-B66A-57D7AC7D67C4', 'Não compareceu para a prova de recuperação.'],
    'N': ['4342E427-808E-4BE7-AF73-8E2540FA84C9', 'Não compareceu ao Exame.'],
    'O': ['BDD11FB6-BF3F-42C2-B7DB-B81D1CE2AE5E', 'Não realizou as atividades no Plurall.'],
    'P': ['8C8A120C-755E-4650-883B-1EB8D033513C', 'Não assistiu a aula síncrona (ao vivo).'],
    'Q': ['E07BC23B-5247-4494-9C95-9E7DB46A84E2', 'Não visualizou as atividades enviadas no PLURALL.'],
    'R': ['90D4F55A-B000-46BB-B90B-99D205911188', 'Não participou da avaliação síncrona.'],
}
