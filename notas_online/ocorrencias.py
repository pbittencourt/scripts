#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from csv import reader
from time import sleep
from datetime import datetime
import logging
import sys


# configuration
turmas = {
    '6A': 'Sexto Ano / 1M6A / Manhã',
    '6B': 'Sexto Ano / 1M6B / Manhã',
    '7A': 'Sétimo Ano / 1M7A / Manhã',
    '8A': 'Oitavo Ano / 1M8A / Manhã',
    '9A': 'Nono Ano / 1M9A / Manhã',
    '1A': 'Primeira Série / 2M1A / Manhã',
    '2A': 'Segunda Série / 2M2A / Manhã',
    '3A': 'Terceira Série / 2M3A / Manhã'
}
disciplinas = {
    'DG': 'Desenho Geométrico / Pedro Pompermayer Bittencourt',
    'FIS': 'Física / Pedro Pompermayer Bittencourt',
    'GMT': 'Geometria / Pedro Pompermayer Bittencourt'
}
ocorrencias = {
    'sincrona': '8C8A120C-755E-4650-883B-1EB8D033513C'
}

##############################
# SETUP LOGGING
##############################

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s %(levelname)s %(message)s',
                   datefmt='%d-%b-%Y %H:%M:%S',
                   filename='ocorrencias.log',
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

# get username and password from CLI
if (len(sys.argv) == 3):
    username = sys.argv[1]
    password = sys.argv[2]
else:
    # we need to interrupt you, man ...
    logger.warning('Você não inseriu seus dados de usuário!')

# abre página
browser = webdriver.Chrome(executable_path=r'/home/monolito/selenium_drivers/chromedriver')
browser.get('https://www.notasonline.com/pages/nol_logon.asp')
logger.info('ACESSO À PÁGINA EFETUADO!')
sleep(2)

# login no sistema

browser.find_element_by_id('txtLogin').send_keys(username)
sleep(1)
browser.find_element_by_id('txtPassword').send_keys(password)
sleep(1)
browser.find_element_by_id('frmForm').submit()
logger.info('Logou com sucesso!')

# le csv com as ocorrências
with open('ocorrencias.csv') as handle:
    file = reader(handle)
    line_count = 0
    for row in file:
        if line_count > 0:
            data, turma, disciplina, num, ocorrencia, descricao = row
            num = int(num) - 1
            success = True

            # acessa a página de notificações
            browser.get('https://www.notasonline.com/pages/user_occurrence.asp')
            sleep(3)
            logger.info(f'Inserindo registro {line_count} ...')

            # insere data da ocorrência
            try:
                insert_data = browser.find_element_by_id('txtOccurrence_date')
                insert_data.clear()
                insert_data.send_keys(data)
                logger.info(f'Inseriu data {data}.')
            except:
                logger.error(f'Não foi possível inserir a data {data}. Algo deu errado!')
                success = False
            sleep(1)

            # insere turma
            try:
                insert_turma = Select(browser.find_element_by_id('selDivisions'))
                insert_turma.select_by_visible_text(turmas[turma])
                logger.info(f'Inseriu turma {turmas[turma]}.')
            except:
                logger.error(f'Não foi possível inserir a turma {turmas[turma]}. Verifique o registro!')
                success = False
            sleep(1)

            # insere disciplina
            try:
                insert_disciplina = Select(browser.find_element_by_id('selSubjects_Teachers'))
                insert_disciplina.select_by_visible_text(disciplinas[disciplina])
                logger.info(f'Inseriu disciplina {disciplinas[disciplina]}.')
            except:
                logger.error(f'''Não foi possível inserir a disciplina
                      {disciplinas[disciplina]}. Algo deu errado!''')
                success = False
            sleep(1)

            # recebe nome do estudante a partir do número
            with open(turma) as turma_arquivo:
                file = turma_arquivo.read()
                lista = file.split(',')
                estudante = lista[num]

            # insere estudante
            try:
                insert_estudante = Select(browser.find_element_by_id('selStudents'))
                insert_estudante.select_by_visible_text(estudante)
                logger.info(f'Inseriu estudante {str(num+1)} {estudante}.')
            except:
                logger.error(f'''Não foi possível inserir estudante {estudante}.
                      Algo deu errado!''')
                success = False
            sleep(1)

            # insere ocorrência
            try:
                insert_ocorrencia = Select(browser.find_element_by_id('selOccurrences_codes'))
                insert_ocorrencia.select_by_value(ocorrencias[ocorrencia])
                logger.info(f'Inseriu ocorrência: {ocorrencias[ocorrencia]}.')
            except:
                logger.error(f'''Não foi possível inserir ocorrência: {ocorrencias[ocorrencia]}.
                      Algo deu errado!''')
                success = False
            sleep(1)

            # insere descrição da ocorrência, se houver
            if (len(descricao) > 0):
                try:
                    insert_descricao = browser.find_element_by_id('txtOccurrence')
                    insert_descricao.clear()
                    insert_descricao.send_keys(descricao)
                    logger.info(f'Inseriu descrição: {descricao}.')
                except:
                    logger.error(f'''Não foi possível inserir descrição: {descricao}.
                                 Algo deu errado!!!''')
                    success = False
            sleep(1)

            # envia formulário
            if success:
                try:
                    '''ok_button = browser.find_element_by_xpath('//*[@id="OKbutton"]/a')
                    ok_button.click()'''
                    logger.info('Ocorrência adicionada!')
                except:
                    logger.warning('Houve algum erro ao enviar o formulário ...')
            else:
                logger.warning('''Não foi possível enviar o formulário por falha em uma 
                      ou mais requisições. Verifique o registro para maiores detalhes.''')
            sleep(1)
            
        line_count += 1

logger.info(f'PROCESSO FINALIZADO!\n' +  '='*40)
