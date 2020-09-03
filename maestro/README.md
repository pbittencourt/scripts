# Maestro: aula digital

Criação automatizada de aulas digitais na plataforma **Maestro** da [Somos Educação](https://www.somoseducacao.com.br/).

## Visão geral

Durante o período de isolamento social imposto pela COVID19, estamos ministrando aulas remotamente, dentro do modelo de *Ensino Remoto Emergencial*. A instituição de ensino na qual leciono utiliza material didático do [Sistema Anglo de Ensino](https://portal.sistemaanglo.com.br). Tal sistema possui diversos recursos digitais, sendo a plataforma **Maestro** um deles. Ao final do mês de março, uma grande reestruturação passou a permitir a criação de *videoconferências* diretamente pelo Maestro, nomeadas de **aulas digitais** utilizando os serviços do [Google Meet](https://meet.google.com).

A criação de aulas digitais é bastante simples, bastando selecionar algumas informações correspondentes à turma na qual a aula será ministrada. Apesar disto — e fica aqui minha nota de agradecimento à equipe de desenvolvimento, que vem trabalhando incansavelmente! — este processo é *maçante*; as aulas ocorrem semanalmente nos mesmos dias e nos mesmos horários, mudando apenas as datas.

Foi pensando nisto que surgiu este pequeno script `auladigital.py`.

## Utilização

O primeiro passo é preencher o arquivo `auladigital.csv`, que contém as informações relevantes para a criação da videoconferência:

- Turma
- Disciplina
- Título da aula
- Dia
- Horário

Com o arquivo csv preenchido, basta executar `auladigital.py`. O script, escrito em *python* e utilizando o módulo *selenium*, abrirá uma janela do navegador, navegará pelas páginas necessárias e preencherá, **automagicamente**, o formulário de criação de uma aula digital, para cada linha contida no registro.

Enquanto o computador trabalha, o professor pode desfrutar de uma xícara de chá.

## Autor

[Pedro P. Bittencourt](pedrobittencourt.com.br), professor da educação básica e aspirante a programador.
