#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep
from csv import reader

# config
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

# abre página
browser = webdriver.Chrome(executable_path=r'/home/monolito/selenium_drivers/chromedriver')
browser.get('https://www.notasonline.com/pages/nol_logon.asp')
print('Acesso à página efetuado.')
sleep(2)

# login no sistema
user = {
    'name': 'pedro.bittencourt',
    'pass': 'qwpo1209'
}

browser.find_element_by_id('txtLogin').send_keys(user['name'])
sleep(1)
browser.find_element_by_id('txtPassword').send_keys(user['pass'])
sleep(2)
browser.find_element_by_id('frmForm').submit()
print('Logou com sucesso!')

# le csv com as ocorrências
with open('/home/monolito/scripts/ocorrencias.csv') as file:
    handle = reader(file)
    line_count = 0
    for row in handle:
        if line_count > 0:
            data, turma, disciplina, estudante, ocorrencia = row
            print(data, turma, disciplina, estudante, ocorrencia, sep=', ', end='\n')

            # acessa a página de notificações
            browser.get('https://www.notasonline.com/pages/user_occurrence.asp')
            sleep(2)
            print('Página de ocorrência selecionada.')

            # insere data da ocorrência
            insert_data = browser.find_element_by_id('txtOccurrence_date')
            insert_data.clear()
            insert_data.send_keys(data)
            print('Inseriu data.')
            sleep(1)

            # seleciona a turma
            insert_turma = Select(browser.find_element_by_id('selDivisions'))
            insert_turma.select_by_visible_text(turmas[turma])
            print('Selecionou turma.')
            sleep(1)

            # seleciona a disciplina
            insert_disciplina = Select(browser.find_element_by_id('selSubjects_Teachers'))
            insert_disciplina.select_by_visible_text(disciplinas[disciplina])
            print('Selecionou disciplina.')
            sleep(1)

            # seleciona o estudante
            insert_estudante = Select(browser.find_element_by_id('selStudents'))
            insert_estudante.select_by_visible_text(estudante)
            print('Selecionou estudante.')
            sleep(1)

            # seleciona a ocorrência
            insert_ocorrencia = Select(browser.find_element_by_id('selOccurrences_codes'))
            insert_ocorrencia.select_by_value(ocorrencias[ocorrencia])
            print('Selecionou ocorrência.')
            sleep(1)

            ok_button = browser.find_element_by_xpath('//*[@id="OKbutton"]/a')
            ok_button.click()
            sleep(2)
            print('Ocorrência adicionada!')
            print('======================')
            
        line_count += 1

print('PROCESSO FINALIZADO')
