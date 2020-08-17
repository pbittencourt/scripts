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


# configuration
turmas = {
    '6A': ('6º Ano EF', '6º ANO A'),
    '6B': ('6º Ano EF', '6º ANO B'),
    '7A': ('7º Ano EF', '7º ANO 2020'),
    '8A': ('8º Ano EF', '8º ANO 2020'),
    '9A': ('9º Ano EF', '9º ANO 2020'),
    '1A': ('1ª Série EM', '1º MÉDIO 2020'),
    '2A': ('2ª Série EM', '2º MÉDIO 2020'),
    '3A': ('3ª Série EM', '3º MÉDIO 2020')
}

disciplinas = {
    'DG': 'Desenho Geométrico',
    'FIS': 'Física',
    'GMT': 'Matemática'
}

##############################
# SETUP LOGGING
##############################

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s %(levelname)s %(message)s',
                   datefmt='%d-%b-%Y %H:%M:%S',
                   filename='auladigital.log',
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

# ask for user and pass
username = str(input('Usuário: _ '))
password = getpass.getpass('Senha: _ ')

# abre página
browser = webdriver.Firefox(executable_path=r'/home/monolito/selenium_drivers/geckodriver')
browser.get('https://login.plurall.net/login')
logger.info('Acesso à página efetuado!')

# faz login
try:
    browser.find_element_by_id('username').send_keys(username)
    browser.find_element_by_id('password').send_keys(password)
    browser.find_element_by_name('loginForm').submit()
    logger.info('Login efetuado com sucesso.')
except:
    logger.error('Não foi possível efetuar o login.')
sleep(5)

# acesssa página de aula digital
browser.get('https://maestro.plurall.net/#/streaming')
logger.info('Página de aula digital acessada.')
sleep(15)

# seleciona perfil de professor 
try:
    browser.find_element_by_xpath("//*[@aria-label = 'Professor']").click()
    logger.info('Perfil de professor selecionado.')
except:
    # entrou direto na conta de professor
    logger.error('Entrou direto na conta ou deu erro. Analisar!!')
sleep(15)

# le csv contendo aulas para criar
with open('/home/monolito/scripts/maestro/auladigital.csv') as file:
    handle = reader(file)
    line_count = 0
    for row in handle:
        if line_count > 0:
            turma, disciplina, titulo, dia, horario = row
            success = True
            logger.info(f'Inserindo registro {line_count} ...')

            # abre menu de séries
            try:
                browser.find_element_by_xpath("//*[@aria-label='Ano/Serie']").click()
            except:
                logger.error(f'Não foi possível abrir o menu de séries.')
                success = False
            sleep(2)

            # seleciona a série desejada
            sel_serie = turmas[turma][0]
            try:
                browser.find_element_by_xpath("//*[@aria-label = '" + sel_serie + "']").click()
                logger.info(f'Selecionou a série {sel_serie}.')
            except:
                logger.error(f'Não foi possível selecionar a série {sel_serie}.')
                success = False
            sleep(3)

            # abre menu de turmas/disciplinas
            try:
                browser.find_element_by_xpath("//*[@aria-label='Turma/Disciplina']").click()
            except:
                logger.error(f'Não foi possível abrir menu de disciplinas.')
                success = False
            sleep(2)

            # seleciona a turma/disciplina desejada
            sel_disciplina = turmas[turma][1] + '-' + disciplinas[disciplina]
            try:
                browser.find_element_by_xpath("//*[@aria-label = '" + sel_disciplina + "']").click()
                logger.info(f'Selecinou a disciplina {sel_disciplina}.')
            except:
                logger.error(f'Não foi possível selecionar a disciplina {sel_disciplina}.')
                success = False
            sleep(3)

            # clica em criar nova aula
            try:
                browser.find_element_by_xpath("/html/body/div[3]/div[2]/md-content/div/div/div[1]/div[1]/div[2]/div[3]/button").click()
                logger.info('Clicou em criar nova aula.')
            except:
                logger.error('Não foi possível clicar em criar nova aula.')
                success = False
            sleep(3)

            # título da aula: limpa e seta valor
            try:
                aula_titulo = browser.find_element_by_xpath("//*[@ng-model='lesson.settings.title']")
                aula_titulo.clear()
                aula_titulo.send_keys(titulo)
                logger.info(f'Inseriu título da aula: {titulo}.')
            except:
                logger.error(f'Não foi possível inserir título da aula: {titulo}.')
                success = False
            sleep(2)

            # dia da aula: limpa e seta valor
            try:
                aula_dia = browser.find_element_by_xpath("//*[@ng-model='ctrl.defaultDate']")
                aula_dia.clear()
                aula_dia.send_keys(dia)
                logger.info(f'Inseriu a data {dia}.')
            except:
                logger.error(f'Não foi possível inserir a data {dia}.')
                success = False
            sleep(2)

            # horário da aula: limpa e seta valor
            try:
                aula_horario = browser.find_element_by_xpath("//*[@ng-model='ctrl.ngModel']")
                aula_horario.clear()
                aula_horario.send_keys(horario)
                logger.info(f'Inseriu o horário {horario}.')
            except:
                logger.error(f'Não foi possível inserir o horário {horario}.')
                success = False
            sleep(2)

            # salva a aula
            if success:
                try:
                    browser.find_element_by_xpath("//*[@ng-click='save()']").click()
                    logger.info('Aula adicionada com sucesso!')
                except:
                    logger.warning('Houve algum erro ao salvar a aula.')
            else:
                logger.warning('Não foi possível adicionar a aula por falha em uma ou mais requisições.')

            sleep(30)
            
        line_count += 1

logger.info(f'PROCESSO FINALIZADO!\n' +  '='*40)
