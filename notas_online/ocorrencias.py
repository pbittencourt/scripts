#!/usr/bin/env python3
"""
AUTOMATIZANDO REGISTROS NO NOTAS ONLINE
Acessa notasonline via selenium e insere
registros contidos em ocorrencias.csv

Autor: Pedro P. Bittencourt
Email: contato@pedrobittencourt.com.br
Site: pedrobittencourt.com.br
"""

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from csv import reader
from time import sleep
import logging
import getpass
import os


def login(username: str, password: str) -> None:
    """
    Recebe username e password do usuário e utiliza essas credenciais
    para tentar fazer login no sistema do notas online. Após a
    submissão do formulário, verifica se o conteúdo exibido corresponde
    à página inicial do sistema, retornando True ou False.
    """

    # abre página de login
    driver.get('https://www.notasonline.com/pages/nol_logon.asp')
    logger.info(f'ACESSO À PÁGINA EFETUADO POR {username}!')
    sleep(1)

    # preenche credenciais do usuário
    driver.find_element_by_id('txtLogin').send_keys(username)
    sleep(0.3)
    driver.find_element_by_id('txtPassword').send_keys(password)
    sleep(0.3)
    driver.find_element_by_id('frmForm').submit()

    # verifica se o login foi efetuado, através da url atual
    if driver.current_url == 'https://www.notasonline.com/pages/home_teacher.asp':
        logger.info('Logou com sucesso!')
        return True
    else:
        logger.error('Não foi possível logar no sistema. Você digitou as credenciais corretas?')
        return False


# globals
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
    'A': 'C6AE796F-E4BA-47C2-A725-98C36CD12E11',
    'B': 'AE890406-F8E3-442D-BF98-44498DC1F517',
    'C': '743091FC-5899-477C-8C68-35A55343B70F',
    'D': '733DA849-6942-44C4-B170-F3B7A97F518A',
    'E': 'E6F973C7-8146-450F-AE4F-02D2C2D451D1',
    'F': '7A80526B-387F-4743-87AF-DB2666CE6639',
    'G': '80860D8F-1152-43BE-ABE3-FCE16987F413',
    'H': '3F67CD55-86B0-4C5F-9502-83F04CF3EE5A',
    'I': '4B55A896-FDA8-484C-81C5-882E140C290E',
    'J': '31F0C7AE-8528-463E-81E0-EF4B4F9A65C7',
    'K': '40A94F21-D8A3-408F-AA30-10BE6F7BCE49',
    'L': 'B43C3E32-2BDC-47C3-90A3-B7004920E0CC',
    'M': 'E8E54836-8579-49CC-B66A-57D7AC7D67C4',
    'N': '4342E427-808E-4BE7-AF73-8E2540FA84C9',
    'O': 'BDD11FB6-BF3F-42C2-B7DB-B81D1CE2AE5E',
    'P': '8C8A120C-755E-4650-883B-1EB8D033513C',
    'Q': 'E07BC23B-5247-4494-9C95-9E7DB46A84E2',
    'R': '90D4F55A-B000-46BB-B90B-99D205911188'
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

# credenciais do usuário
username = str(input('Usuário: _ '))
password = getpass.getpass('Senha: _ ')

# inicializa driver
driver = webdriver.Chrome(executable_path=os.getcwd() + r'/drivers/chromedriver')

# verifica login
if login(username, password):

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
                driver.get('https://www.notasonline.com/pages/user_occurrence.asp')
                sleep(1)
                logger.info(f'Inserindo registro {line_count} ...')

                # insere data da ocorrência
                try:
                    insert_data = driver.find_element_by_id('txtOccurrence_date')
                    insert_data.clear()
                    insert_data.send_keys(data)
                    logger.info(f'Inseriu data {data}.')
                except:
                    logger.error(f'Não foi possível inserir a data {data}. Algo deu errado!')
                    success = False
                sleep(1)

                # insere turma
                try:
                    insert_turma = Select(driver.find_element_by_id('selDivisions'))
                    insert_turma.select_by_visible_text(turmas[turma])
                    logger.info(f'Inseriu turma {turmas[turma]}.')
                except:
                    logger.error(f'Não foi possível inserir a turma {turmas[turma]}. Verifique o registro!')
                    success = False
                sleep(1)

                # insere disciplina
                try:
                    insert_disciplina = Select(driver.find_element_by_id('selSubjects_Teachers'))
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
                    insert_estudante = Select(driver.find_element_by_id('selStudents'))
                    insert_estudante.select_by_visible_text(estudante)
                    logger.info(f'Inseriu estudante {str(num+1)} {estudante}.')
                except:
                    logger.error(f'''Não foi possível inserir estudante {estudante}.
                          Algo deu errado!''')
                    success = False
                sleep(1)

                # insere ocorrência
                try:
                    insert_ocorrencia = Select(driver.find_element_by_id('selOccurrences_codes'))
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
                        insert_descricao = driver.find_element_by_id('txtOccurrence')
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
                        ok_button = driver.find_element_by_xpath('//*[@id="OKbutton"]/a')
                        ok_button.click()
                        logger.info('Ocorrência adicionada!')
                    except:
                        logger.warning('Houve algum erro ao enviar o formulário ...')
                else:
                    logger.warning('''Não foi possível enviar o formulário por falha em uma 
                          ou mais requisições. Verifique o registro para maiores detalhes.''')
                sleep(1)
                
            line_count += 1

    logger.info(f'PROCESSO FINALIZADO!\n' +  '='*40)
