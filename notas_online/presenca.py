#!/usr/bin/env python3
"""
AUTOMATIZANDO PRESENÇAS NO NOTAS ONLINE
Acessa notasonline via selenium e insere
registros contidos em presenca.csv

Autor: Pedro P. Bittencourt
Email: contato@pedrobittencourt.com.br
Site: pedrobittencourt.com.br
"""


from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from csv import reader
from time import sleep
from config import *
import os


# inicializa programa
p = Main()

# verifica login
if p.login():

    # le csv com registros de aulas
    with open(os.path.join(file_dir, 'presenca.csv')) as handle:
        registro = reader(handle)
        line_count = 0
        for row in registro:
            if line_count > 0:
                mes, turma, disciplina, dia, ausencias = row
                p.logger.info(f'Preenchendo diário {line_count} ...')

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
                    p.driver.get(urlpresenca)
                    p.logger.info(f'Acessou diário da turma {diario}, mês {mes}.')
                except:
                    p.errorquit(f'Não foi possível acessar diário da turma {diario}, mês {mes}.')
                sleep(1)

                # verifica qual é a primeira coluna vazia no diário,
                # a partir da qual preencheremos com o registro do dia
                col = 2  # a primeira coluna contém os nomes dos alunos
                while True:
                    xpath = f'/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td[{col}]'
                    novo_dia = p.driver.find_element_by_xpath(xpath)
                    novo_dia_texto = novo_dia.text.replace('__', '').strip()
                    if len(novo_dia_texto) == 0:
                        break

                    col += 1
                    
                p.logger.info(f'Uma nova data será inserida na coluna {col-1}.')

                # é preciso clicar na célula correspondente ao dia para
                # ativar um prompt javascript e preencher com o dia
                try:
                    novo_dia.click()
                    alert = Alert(p.driver)
                    alert.send_keys(dia)
                    alert.accept()
                    p.logger.info(f'Inserido dia {dia} no diário.')
                except:
                    p.errorquit(f'Não foi possível inserir dia {dia} no diário.')
                sleep(1)

                # clica no checkbox correspondente ao dia para
                # marcar presença a todos os alunos, por padrão
                try:
                    box_dia = p.driver.find_element_by_id('day_' + str(col-1))
                    box_dia.click()
                    p.logger.info('Marcando presença para os estudantes.')
                except:
                    p.errorquit('Não foi possível marcar presença para os estudantes.')
                sleep(1)

                # verifica as ausências do dia
                ausente = ausencias.split('|')
                if (ausente[0] != ''):
                    p.logger.info(f'Temos {len(ausente)} ausência(s) nesta data:')
                    for aluno in ausente:
                        row = int(aluno) + 2
                        try:
                            xpath = f'/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{row}]/td[{col}]/input'
                            ausente_box = p.driver.find_element_by_xpath(xpath)
                            ausente_box.click()
                            p.logger.info(f'Inserida ausência para estudante num {aluno}.')
                        except:
                            p.errorquit(f'Não foi possível inserir ausência para estudante num {aluno}.')
                sleep(1)

                # finaliza o preenchimento
                try:
                    gravar = p.driver.find_element_by_id('btSave')
                    #gravar.click()
                    p.logger.info('Preenchimento do diário efetuado com sucesso!')
                except:
                    p.errorquit('Não foi possível finalizar o preenchimento do diário.')
                sleep(1)

                ###################################
                # ENVIANDO NOTIFICAÇÕES DE AUSÊNCIA
                ###################################

                if (ausente[0] != ''):
                    for i in range(0, len(ausente)):
                        # acessa página de notificações
                        try:
                            p.driver.get('https://www.notasonline.com/pages/user_occurrence.asp')
                            p.logger.info(f'Inserindo {i+1}a ausência de {len(ausente)} no diário {diario} ...')
                        except:
                            p.errorquit('Não foi possível inserir {i+1}a ausência do diário de {diario}!')
                        sleep(1)
                        
                        # insere data da ocorrência
                        data = dia.zfill(2) + '/' + mes.zfill(2) + '/2020'
                        try:
                            insert_data = p.driver.find_element_by_id('txtOccurrence_date')
                            insert_data.clear()
                            insert_data.send_keys(data)
                            p.logger.info(f'Inseriu data {data}.')
                        except:
                            p.errorquit(f'Não foi possível inserir a data {data}.')
                        sleep(1)

                        # insere turma
                        try:
                            insert_turma = Select(p.driver.find_element_by_id('selDivisions'))
                            insert_turma.select_by_visible_text(turmas[turma])
                            p.logger.info(f'Inseriu turma {turmas[turma]}.')
                        except:
                            p.errorquit(f'Não foi possível inserir a turma {turmas[turma]}.')
                        sleep(1)

                        # insere disciplina
                        try:
                            insert_disciplina = Select(p.driver.find_element_by_id('selSubjects_Teachers'))
                            insert_disciplina.select_by_visible_text(disciplinas[disciplina])
                            p.logger.info(f'Inseriu disciplina {disciplinas[disciplina]}.')
                        except:
                            p.errorquit(f'Não foi possível inserir a disciplina {disciplinas[disciplina]}.')
                        sleep(1)

                        # recebe nome do estudante a partir do número
                        with open(os.path.join(file_dir, turma)) as turma_arquivo:
                            file = turma_arquivo.read()
                            lista = file.split(',')
                            estudante = lista[int(ausente[i]) - 1]

                        # insere estudante
                        try:
                            insert_estudante = Select(p.driver.find_element_by_id('selStudents'))
                            insert_estudante.select_by_visible_text(estudante)
                            p.logger.info(f'Inseriu estudante {ausente[i]} {estudante}.')
                        except:
                            p.errorquit(f'Não foi possível inserir estudante {estudante}.')
                        sleep(1)

                        # insere ocorrência
                        try:
                            insert_ocorrencia = Select(p.driver.find_element_by_id('selOccurrences_codes'))
                            insert_ocorrencia.select_by_value('8C8A120C-755E-4650-883B-1EB8D033513C')
                            p.logger.info(f'Inseriu ocorrência: ausente na aula síncrona (P).')
                        except:
                            p.errorquit(f'Não foi possível inserir ocorrência: {ocorrencias[ocorrencia]}.')
                        sleep(1)

                        # envia formulário
                        try:
                            ok_button = p.driver.find_element_by_xpath('//*[@id="OKbutton"]/a')
                            #ok_button.click()
                            p.logger.info('Ausência adicionada!')
                        except:
                            p.logger.warning('Houve algum erro ao enviar o formulário ...')
                            sleep(1)

            line_count += 1

    p.logger.info(f'PROCESSO FINALIZADO!\n' +  '='*40)

else:
    p.logger.error('Não foi possível efetuar o login. Você inseriu as credenciais corretas?')

# encerra o driver
p.driver.quit()
