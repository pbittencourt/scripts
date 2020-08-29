#!/usr/bin/env python3
"""
AUTOMATIZANDO INSERÇÃO DE AULA DIGITAL
Acessa o site do plurall via selenium e
insere aulas digitais, cujos registros
se encontram em auladigital.csv.

Autor: Pedro P. Bittencourt
Email: contato@pedrobittencourt.com.br
Site: pedrobittencourt.com.br
"""

from selenium import webdriver
from time import sleep
from csv import reader
import logging
import getpass
import os
import sys


def login(username: str, password: str) -> None:
    """
    Recebe username e password do usuário e utiliza essas credenciais
    para tentar fazer login no sistema do notas online. Após a
    submissão do formulário, verifica se o conteúdo exibido corresponde
    à página inicial do sistema, retornando True ou False.
    """

    # abre página de login
    driver.get('https://login.plurall.net/login')
    logger.info(f'ACESSO À PÁGINA EFETUADO POR {username}!')

    # preenche credenciais do usuário
    driver.find_element_by_id('username').send_keys(username)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_name('loginForm').submit()
    sleep(10)

    # verifica se o login foi efetuado, através da url atual
    if driver.current_url == 'https://conta.plurall.net/':
        logger.info('Logou com sucesso!')
        return True
    else:
        logger.error('Não foi possível logar no sistema. Você digitou as credenciais corretas?')
        return False


def errorquit(msg: str = 'ERRO NÃO ESPECIFICADO') -> str:
    """
    Quando falhar numa requisição importante, exibe
    mensagem de erro, registra no log, fecha o driver
    e encerra o programa.
    """
    logger.error(f'Não foi possível continuar devido ao seguinte problema: {msg}.')
    logger.info('O programa será encerrado agora. Verifique o registro para detalhes!')
    driver.quit()
    sys.exit(1)


def title() -> str:
    """
    Just print some fancy header!
    """
    msg = '''
                                                         
 #    # ###### #       ####   ####  #    # ######        
 #    # #      #      #    # #    # ##  ## #             
 #    # #####  #      #      #    # # ## # #####         
 # ## # #      #      #      #    # #    # #      ###    
 ##  ## #      #      #    # #    # #    # #      ###    
 #    # ###### ######  ####   ####  #    # ######  #     
                                                  #      

███╗   ███╗ █████╗ ███████╗███████╗████████╗██████╗  ██████╗ ██╗
████╗ ████║██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗██║
██╔████╔██║███████║█████╗  ███████╗   ██║   ██████╔╝██║   ██║██║
██║╚██╔╝██║██╔══██║██╔══╝  ╚════██║   ██║   ██╔══██╗██║   ██║╚═╝
██║ ╚═╝ ██║██║  ██║███████╗███████║   ██║   ██║  ██║╚██████╔╝██╗
╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝
                                                                
    '''
    print(msg)


# globals
turmas = {
    '5A': ('5º Ano EF', '5 ANO A'),
    '5B': ('5º Ano EF', '5 ANO B'),
    '6A': ('6º Ano EF', '6º ANO A'),
    '6B': ('6º Ano EF', '6º ANO B'),
    '7A': ('7º Ano EF', '7º ANO 2020'),
    '8A': ('8º Ano EF', '8º ANO 2020'),
    '9A': ('9º Ano EF', '9º ANO 2020'),
    '1A': ('1ª Série EM', '1º MÉDIO 2020'),
    '2A': ('2ª Série EM', '2º MÉDIO 2020'),
    '3A': ('3ª Série EM', '3º MÉDIO 2020'),
}

disciplinas = {
    'DG': 'Desenho Geométrico',
    'FIS': 'Física',
    'GMT': 'Matemática',
    'CIE': 'Ciências',
    'QUI': 'Química',
}

##############################
# SETUP LOGGING
##############################

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s %(levelname)s %(message)s',
                   datefmt='%d-%b-%Y %H:%M:%S',
                   filename='./auladigital.log',
                   filemode='a')
# create logger object
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# handle which writes INFO messages to stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)

# format for console
formatter = logging.Formatter('%(levelname)-8s %(message)s')
console.setFormatter(formatter)

# add console handler to logger
logger.addHandler(console)

##############################
# END OF SETUP LOGGING
##############################

title()

# credenciais do usuário
username = str(input('Usuário: _ '))
password = getpass.getpass('Senha: _ ')

# inicializa driver
driver = webdriver.Chrome(executable_path=r'./../drivers/chromedriver')

# verifica login
if login(username, password):

    # acesssa página de aula digital
    driver.get('https://maestro.plurall.net/#/streaming')
    logger.info('Página de aula digital acessada.')
    sleep(15)

    # verifica existência de popup para seleção de perfil
    try:
        driver.find_element_by_xpath("//*[@aria-label = 'perfil']")
        profile = True
    except:
        profile = False

    if profile:
        # seleciona perfil de professor 
        try:
            driver.find_element_by_xpath("//*[@aria-label = 'Professor']").click()
            logger.info('Perfil de professor selecionado.')
        except:
            errorquit('não foi possível selecionar perfil de professor')
        sleep(10)

    # le csv contendo aulas para criar
    with open('./auladigital.csv') as file:
        handle = reader(file)
        line_count = 0
        for row in handle:
            if line_count > 0:
                turma, disciplina, titulo, dia, horario = row
                logger.info(f'Inserindo registro {line_count} ...')

                # abre menu de séries
                try:
                    driver.find_element_by_xpath("//*[@aria-label='Ano/Serie']").click()
                except:
                    errorquit('não foi possível abrir o menu de séries')
                sleep(2)

                # seleciona a série desejada
                sel_serie = turmas[turma][0]
                try:
                    driver.find_element_by_xpath("//*[@aria-label = '" + sel_serie + "']").click()
                    logger.info(f'Selecionou a série {sel_serie}.')
                except:
                    errorquit(f'não foi possível selecionar a série {sel_serie}')
                sleep(3)

                # abre menu de turmas/disciplinas
                try:
                    driver.find_element_by_xpath("//*[@aria-label='Turma/Disciplina']").click()
                except:
                    errorquit(f'não foi possível abrir menu de disciplinas')
                sleep(2)

                # seleciona a turma/disciplina desejada
                sel_disciplina = turmas[turma][1] + '-' + disciplinas[disciplina]
                try:
                    driver.find_element_by_xpath("//*[@aria-label = '" + sel_disciplina + "']").click()
                    logger.info(f'Selecinou a disciplina {sel_disciplina}.')
                except:
                    errorquit(f'não foi possível selecionar a disciplina {sel_disciplina}')
                sleep(3)

                # clica em criar nova aula
                try:
                    driver.find_element_by_xpath("/html/body/div[3]/div[2]/md-content/div/div/div[1]/div[1]/div[2]/div[3]/button").click()
                    logger.info('Clicou em criar nova aula.')
                except:
                    errorquit('não foi possível clicar em criar nova aula')
                sleep(3)

                # título da aula: limpa e seta valor
                try:
                    aula_titulo = driver.find_element_by_xpath("//*[@ng-model='lesson.settings.title']")
                    aula_titulo.clear()
                    aula_titulo.send_keys(titulo)
                    logger.info(f'Inseriu título da aula: {titulo}.')
                except:
                    errorquit(f'não foi possível inserir título da aula: {titulo}')
                sleep(2)

                # dia da aula: limpa e seta valor
                try:
                    aula_dia = driver.find_element_by_xpath("//*[@ng-model='ctrl.defaultDate']")
                    aula_dia.clear()
                    aula_dia.send_keys(dia)
                    logger.info(f'Inseriu a data {dia}.')
                except:
                    errorquit(f'não foi possível inserir a data {dia}')
                sleep(2)

                # horário da aula: limpa e seta valor
                try:
                    aula_horario = driver.find_element_by_xpath("//*[@ng-model='ctrl.ngModel']")
                    aula_horario.clear()
                    aula_horario.send_keys(horario)
                    logger.info(f'Inseriu o horário {horario}.')
                except:
                    errorquit(f'não foi possível inserir o horário {horario}')
                sleep(2)

                # salva a aula
                try:
                    driver.find_element_by_xpath("//*[@ng-click='save()']").click()
                    logger.info('Aula adicionada com sucesso!')
                except:
                    logger.warning('Houve algum erro ao salvar a aula.')

                sleep(30)
                
            line_count += 1

    logger.info(f'PROCESSO FINALIZADO!\n' +  '='*40)
else:
    logger.error('Encerrando programa devido ausência de credenciais.')

# encerra driver
driver.quit()
