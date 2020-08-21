#!/usr/bin/env python3
"""
AUTOMATIZANDO PRESENÇAS NO NOTAS ONLINE
Acessa notasonline via selenium e insere
registros contidos em presenca.csv

Autor: Pedro P. Bittencourt
Email: contato@pedrobittencourt.com.br
Site: pedrobittencourt.com.br
"""


from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from csv import reader
from time import sleep
import logging
import getpass


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
    driver.find_element_by_id('txtPassword').send_keys(password)
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
diarios = {
    '6ADG': '591D1214-CEC7-4511-B99D-38B64C224704',
    '6BDG': '2C350D3D-560B-4FE3-A6B8-9C3B4C1D7BB2',
    '7ADG': '860B570A-9F38-4384-93BA-8905AE76B98C',
    '8ADG': '570678BF-C4FD-4E26-BB11-9C19AA9BB457',
    '9ADG': 'C35A5E17-0299-4E6F-86A5-3BFCEAE34E87',
    '8AFIS': '6CDA5EAA-BB3C-4029-8F27-674B385E4689',
    '9AFIS': 'D61E769F-C1BF-4720-9F0F-28DB24889C73',
    '1AFIS': '993A3639-2A70-4748-8BB9-CF4BF24131FE',
    '1AGMT': '80A71A6F-1ED2-4267-8E93-FD74B5B77EA4',
    '2AFIS': '88A1A059-12DE-4676-9A28-E07EB47DE913',
    '2AGMT': 'E12A8904-21D6-4E1B-A1DA-99A66EAF400F',
    '3AFIS': '930B8C3A-450A-405D-A1ED-725FD1FC19E8',
    '3AGMT': 'E08722EA-267E-42DE-875E-35944FA616D9',
}

##############################
# SETUP LOGGING
##############################

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s %(levelname)s %(message)s',
                   datefmt='%d-%b-%Y %H:%M:%S',
                   filename='presenca.log',
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
driver = webdriver.Chrome(executable_path=r'/home/monolito/selenium_drivers/chromedriver')

# verifica login
if login(username, password):

    # le csv com registros de aulas
    with open('presenca.csv') as handle:
        file = reader(handle)
        line_count = 0
        for row in file:
            if line_count > 0:
                mes, turma, disciplina, dia, ausencias = row
                success = True

                logger.info(f'Preenchendo diário {line_count} ...')

                ####################
                # PREENCHENDO DIÁRIO
                ####################

                # variável diário: junção de turma com disciplina, 
                # no formato '6ADG' ou '3AFIS', por exemplo
                diario = turma + disciplina

                # monta a url
                urlpresenca = f'https://www.notasonline.com/pages/diario.asp?fkey_division_teacher_subject={diarios[diario]}&bimester={mes}&type=regular'

                # acessa diário da turma
                try:
                    driver.get(urlpresenca)
                    logger.info(f'Acessou diário da turma {diario}, mês {mes}.')
                except:
                    logger.error(f'Não foi possível acessar diário da turma {diario}, mês {mes}. Verifique o registro!')
                    success = False
                sleep(1)

                # verifica qual é a primeira coluna vazia no diário,
                # a partir da qual preencheremos com o registro do dia
                col = 2  # a primeira coluna contém os nomes dos alunos
                while True:
                    xpath = f'/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td[{col}]'
                    novo_dia = driver.find_element_by_xpath(xpath)
                    novo_dia_texto = novo_dia.text.replace('__', '').strip()
                    if len(novo_dia_texto) == 0:
                        break

                    col += 1
                    
                logger.info(f'Uma nova data será inserida na coluna {col-1}.')

                # é preciso clicar na célula correspondente ao dia para
                # ativar um prompt javascript e preencher com o dia
                try:
                    novo_dia.click()
                    alert = Alert(driver)
                    alert.send_keys(dia)
                    alert.accept()
                    logger.info(f'Inserido dia {dia} no diário.')
                except:
                    logger.error(f'Não foi possível inserir dia {dia} no diário. Verifique o registro!')
                    success = False
                sleep(1)

                # clica no checkbox correspondente ao dia para
                # marcar presença a todos os alunos, por padrão
                try:
                    box_dia = driver.find_element_by_id('day_' + str(col-1))
                    box_dia.click()
                    logger.info('Marcando presença para os estudantes.')
                except:
                    logger.info('Não foi possível dar presença para os estudantes. Verifique o registro!')
                    success = False
                sleep(1)

                # verifica as ausências do dia
                ausente = ausencias.split('|')
                if (ausente[0] != ''):
                    logger.info(f'Temos {len(ausente)} ausência(s) nesta data:')
                    for aluno in ausente:
                        row = int(aluno) + 2
                        try:
                            xpath = f'/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{row}]/td[{col}]/input'
                            ausente_box = driver.find_element_by_xpath(xpath)
                            ausente_box.click()
                            logger.info(f'Inserida ausência para estudante num {aluno}.')
                        except:
                            logger.error(f'Não foi possível inserir ausência para estudante num {aluno}. Verifique o registro!')
                            success = False
                sleep(1)

                # finaliza o preenchimento
                if success:
                    try:
                        gravar = driver.find_element_by_id('btSave')
                        #gravar.click()
                        logger.info('Preenchimento do diário efetuado com sucesso!')
                    except:
                        logger.error('Não foi possível finalizar o preenchimento do diário.')
                else:
                    logger.warning('''Não foi possível preencher o diário por falha em uma
                        ou mais requisições. Verifique o registro para maiores detalhes.''')
                sleep(1)

                ###################################
                # ENVIANDO NOTIFICAÇÕES DE AUSÊNCIA
                ###################################

                if (ausente[0] != ''):
                    for i in range(0, len(ausente)):
                        success = True
                        # acessa página de notificações
                        try:
                            driver.get('https://www.notasonline.com/pages/user_occurrence.asp')
                            logger.info(f'Inserindo {i+1}a ausência de {len(ausente)} no diário {diario} ...')
                        except:
                            logger.error('Não foi possível inserir {i+1}a ausência do diário de {diario}!')
                            success = False
                        sleep(1)
                        
                        # insere data da ocorrência
                        data = dia.zfill(2) + '/' + mes.zfill(2) + '/2020'
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
                            estudante = lista[int(ausente[i]) - 1]

                        # insere estudante
                        try:
                            insert_estudante = Select(driver.find_element_by_id('selStudents'))
                            insert_estudante.select_by_visible_text(estudante)
                            logger.info(f'Inseriu estudante {ausente[i]} {estudante}.')
                        except:
                            logger.error(f'''Não foi possível inserir estudante {estudante}.
                                  Algo deu errado!''')
                            success = False
                        sleep(1)

                        # insere ocorrência
                        try:
                            insert_ocorrencia = Select(driver.find_element_by_id('selOccurrences_codes'))
                            insert_ocorrencia.select_by_value('8C8A120C-755E-4650-883B-1EB8D033513C')
                            logger.info(f'Inseriu ocorrência: ausente na aula síncrona (P).')
                        except:
                            logger.error(f'''Não foi possível inserir ocorrência: {ocorrencias[ocorrencia]}.
                                  Algo deu errado!''')
                            success = False
                        sleep(1)

                        # envia formulário
                        if success:
                            try:
                                ok_button = driver.find_element_by_xpath('//*[@id="OKbutton"]/a')
                                #ok_button.click()
                                logger.info('Ausência adicionada!')
                            except:
                                logger.warning('Houve algum erro ao enviar o formulário ...')
                        else:
                            logger.warning('''Não foi possível enviar o formulário por falha em uma 
                                  ou mais requisições. Verifique o registro para maiores detalhes.''')
                        sleep(1)

            line_count += 1

    logger.info(f'PROCESSO FINALIZADO!\n' +  '='*40)
