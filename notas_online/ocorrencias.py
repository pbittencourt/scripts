#!/usr/bin/env python3
"""
AUTOMATIZANDO OCORRÊNCIAS NO NOTAS ONLINE
Acessa notasonline via selenium e insere
registros contidos em ocorrencias.csv

Autor: Pedro P. Bittencourt
Email: contato@pedrobittencourt.com.br
Site: pedrobittencourt.com.br
Github: https://github.com/pbittencourt/workflow
"""

from selenium.webdriver.support.ui import Select
from csv import reader
from time import sleep
from config import *
import os

# inicializa programa
p = Main('ocorrências')

# verifica login
if p.login():
    p.logger.info(f'ACESSO À PÁGINA EFETUADO POR {p.username}!')

    # le csv com as ocorrências
    with open(os.path.join(file_dir, 'ocorrencias.csv')) as handle:
        registro = reader(handle)
        line_count = 0
        for row in registro:
            if line_count > 0:
                data, turma, disciplina, num, ocorrencia, descricao = row
                num = int(num) - 1

                # acessa a página de notificações
                p.driver.get('https://www.notasonline.com/pages/user_occurrence.asp')
                sleep(1)
                p.logger.info(f'Inserindo registro {line_count} ...')

                # insere data da ocorrência
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
                    p.errorquit(f'Não foi possível inserir a disciplina                       {disciplinas[disciplina]}.')
                sleep(1)

                # recebe nome do estudante a partir do número
                with open(os.path.join(file_dir, turma)) as turma_arquivo:
                    filename = turma_arquivo.read()
                    lista = filename.split(',')
                    estudante = lista[num]

                # insere estudante
                try:
                    insert_estudante = Select(p.driver.find_element_by_id('selStudents'))
                    insert_estudante.select_by_visible_text(estudante)
                    p.logger.info(f'Inseriu estudante {str(num+1)} {estudante}.')
                except:
                    p.errorquit(f'Não foi possível inserir estudante {estudante}.')
                sleep(1)

                # insere ocorrência
                try:
                    insert_ocorrencia = Select(p.driver.find_element_by_id('selOccurrences_codes'))
                    insert_ocorrencia.select_by_value(ocorrencias[ocorrencia][0])
                    p.logger.info(f'Inseriu ocorrência: {ocorrencias[ocorrencia][1]}.')
                except:
                    p.errorquit(f'Não foi possível inserir ocorrência: {ocorrencias[ocorrencia][1]}.')
                sleep(1)

                # insere descrição da ocorrência, se houver
                if (len(descricao) > 0):
                    try:
                        insert_descricao = p.driver.find_element_by_id('txtOccurrence')
                        insert_descricao.clear()
                        insert_descricao.send_keys(descricao)
                        p.logger.info(f'Inseriu descrição: {descricao}.')
                    except:
                        p.errorquit(f'Não foi possível inserir descrição: {descricao}.')
                sleep(1)

                # envia formulário
                try:
                    ok_button = p.driver.find_element_by_xpath('//*[@id="OKbutton"]/a')
                    ok_button.click()
                    p.logger.info('Ocorrência adicionada!')
                except:
                    p.logger.warning('Houve algum erro ao enviar o formulário ...')
                sleep(1)
                
            line_count += 1

    p.logger.info(f'PROCESSO FINALIZADO!\n' +  '='*40)

else:
    p.logger.error('Não foi possível efetuar o login. Você inseriu as credenciais corretas?\n' + '='*40)

# encerra o driver
p.driver.quit()
