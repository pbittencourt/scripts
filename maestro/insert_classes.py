#!/usr/bin/env python3

from selenium import webdriver
from time import sleep
from csv import reader

# abre página
browser = webdriver.Firefox(executable_path=r'/home/monolito/selenium_drivers/geckodriver')
browser.get('https://maestro.plurall.net/?state=6200112592659666#/access_token=4a5fa69cfc0cd25b30322c40dbe4b3ac&expires_in=86400&token_type=bearer&scope=&refresh_token=c37b594e96e3a7f5cb3cae575c7a083b1bafb7b8')

# seleciona perfil de professor
try:
    browser.find_element_by_xpath("//*[@aria-label = 'Professor']").click()
    sleep(10)
except:
    # entrou direto na conta de professor
    print('foi direto ou deu erro ...')
    pass

# clica em aula digital
browser.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/md-sidenav/md-toolbar/md-list/md-list-item[4]").click()
sleep(10)

# le csv contendo aulas para criar
with open('/home/monolito/scripts/insert_classes.csv') as file:
    handle = reader(file)
    line_count = 0
    for row in handle:
        if line_count > 0:
            serie, turma, titulo, dia, horario = row
            print(serie, turma, titulo, dia, horario, sep=', ', end='\n')

            # abre menu de séries
            browser.find_element_by_xpath("/html/body/div[3]/div[2]/md-content/div/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/md-menu-bar/md-menu/button").click()
            sleep(2)

            # seleciona a série desejada
            browser.find_element_by_xpath("//*[@aria-label = '" + serie + "']").click()
            sleep(5)

            # abre menu de turmas/disciplinas
            browser.find_element_by_xpath("/html/body/div[3]/div[2]/md-content/div/div/div[1]/div[1]/div[2]/div[2]/div/div[2]/md-menu-bar/md-menu/button").click()
            sleep(2)

            # seleciona a turma/disciplina desejada
            browser.find_element_by_xpath("//*[@aria-label = '" + turma + "']").click()
            sleep(5)

            # clica em criar nova aula
            browser.find_element_by_xpath("/html/body/div[3]/div[2]/md-content/div/div/div[1]/div[1]/div[2]/div[3]/button").click()
            sleep(5)

            # título da aula: limpa e seta valor
            aula_titulo = browser.find_element_by_xpath("//*[@ng-model='lesson.settings.title']")
            aula_titulo.clear()
            aula_titulo.send_keys(titulo)
            sleep(1)

            # dia da aula: limpa e seta valor
            aula_dia = browser.find_element_by_xpath("//*[@ng-model='ctrl.defaultDate']")
            aula_dia.clear()
            aula_dia.send_keys(dia)
            sleep(1)

            # horário da aula: limpa e seta valor
            aula_horario = browser.find_element_by_xpath("//*[@ng-model='ctrl.ngModel']")
            aula_horario.clear()
            aula_horario.send_keys(horario)
            sleep(1)

            # salva a aula
            browser.find_element_by_xpath("//*[@ng-click='save()']").click()
            print('Feito!!', end='\n\n')
            sleep(20)
            
        line_count += 1
