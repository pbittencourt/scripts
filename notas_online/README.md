# Notas Online

Automatizando inserção de registros no sistema [Notas Online](https://www.notasonline.com/).

## Visão geral

A instituição de ensino na qual leciono, minimamente antenada com o fato de já vivermos sob a égide do século XXI, utiliza diários de classe digitais, em detrimento dos anacrônicos e ultrapassados diários de classe de papel. Diariamente, portanto, lançamos registros diversos, tais como conteúdos, ausências e ocorrências. Durante o período de isolamento social imposto pela COVID19, no qual ministramos aulas remotamente, tal lançamento de ocorrências se tornou mais frequente, tendo em vista a necessidade de informar as famílias o que ocorre durante as aulas síncronas.

Este processo, entretanto, é repetitivo e entediante. Muitas vezes precisamos lançar registros semelhantes, com pequenas diferenças entre si, para muitos estudantes. A cada novo registro, é necessário avançar por uma série de passos, preenchendo um mesmo formulário diversas vezes, o que pode incorrer em erro. Ademais, a interface do sistema parece não ter sofrido qualquer alteração desde meados de 2001, quando sites eram desenvolvidos em tabelas e exigiam uma resolução mínima de 800x600 —  mas recomendava-se algo superior a 1024x768.

Foi pensando nesses problemas que desenvolvi alguns scripts, contidos aqui em **notas_online**, brevemente descritos a seguir.

## Requerimentos

Esses scripts utilizam os módulos **BeautifulSoup** e **Selenium**, que podem ser instalados via *pip*:

`pip install -m selenium`
`pip install -m bs4`

Para maiores detalhes e problemas relacionados à instalação, recomendo uma [leitura na documentação](https://selenium-python.readthedocs.io/installation.html) de [ambos os módulos](https://www.crummy.com/software/BeautifulSoup/bs4/doc.ptbr/). Também será necessário baixar o [driver correspondente a seu navegador](https://selenium-python.readthedocs.io/installation.html#drivers) para a utilização do *Selenium*. No diretório `drivers/` deste repositório, há drivers para **Google Chrome**, versões *linux* (ChromeDriver 79.0.3945.16) e *windows* (ChromeDriver 85.0.4183.87). Por definições do sistema Notas Online, alguns navegadores —  estou falando de você, Firefox! —  não são aceitos, então recomendo aceitar o Google Chrome.

## Instalação

Clone este o repositório:

`git clone https://github.com/pbittencourt/workflow.git`

Na primeira utilização, será necessário executar o script `install.py`. Em um terminal, basta executar:

`python3 /caminho/para/notas_online/install.py`

Após efetuar o login no sistema Notas Online, ele acessará suas páginas de ocorrências e diários de classe, efetuando uma raspagem de dados e armazenando variáveis úteis no arquivo `config.py`. Feito isto, você já estará apto a utilizar os scripts `ocorrencias.py` e `presenca.py`.

## Utilização

### Lançamento de ocorrências

Para lançar ocorrências dos estudantes (ausência, atividade não realizada, comportamento inadequado, etc.), o primeiro passo é preencher o documento `ocorrencias.csv` com as seguintes informações:

- **data**: a data da ocorrência, no formato dd/mm/yyyy.
- **turma**: a turma do estudante, dentre as opções programadas, referentes às turmas nas quais leciono:
    - 6A, 6B, 7A, 8A, 9A, 1A, 2A, 3A.
- **disciplina**: o *código da disciplina*, dentre as opções programadas, referentes às quais ministro:
    - DG (Desenho Geométrico), FIS (Física) e GMT (Geometria).
- **estudante**: o *número de chamada* do estudante.
- **ocorrencia**: o *código* da ocorrência; uma lista com códigos e ocorrências pode ser verificada em `lista_ocorrencias.txt`.
- **descricao**: uma descrição detalhada da ocorrência, se for o caso. Por exemplo, caso um estudante tenha deixado de entregar uma atividade, pode-se especificar aqui o que deixou de ser feito, qual era o prazo de entrega, quando foi solicitado e quais são as orientações para a família a partir disto.

Preenchido o documento, basta executar:

`python3 /caminho/para/notas_online/ocorrencias.py`

Após o fornecimento de suas credenciais, uma janela do navegador será aberta e os registros serão inseridos, **automagicamente**, no sistema! Aproveite este momento para passar um café (:

### Presenças e ausências

Para preencher o diário do dia, marcando presenças dos estudantes e, consequentemente, eventuais ausências, inicia-se preenchendo o documento `presenca.csv` com as seguintes informações:

- **mes**: o *número do mês*, sem zero à esquerda, referente à data na qual foi ministrada a aula —  8 para agosto e 11 para novembro, por exemplo.
- **turma**: a turma na qual foi ministrada a aula, dentre as opções programadas, referentes às turmas nas quais leciono:
    - 6A, 6B, 7A, 8A, 9A, 1A, 2A, 3A.
- **disciplina**: o *código da disciplina*, dentre as opções programadas, referentes às quais ministro:
    - DG (Desenho Geométrico), FIS (Física) e GMT (Geometria).
- **dia**: o dia em que a aula ocorreu, sem zero à esquerda.
- **ausencias**: os *números de chamada* dos alunos ausentes na aula, quando houver, separados por `|`.

Com o documento preenchido, pode-se executar:

`python3 /caminho/para/notas_online/presenca.py`

Mais uma vez, suas credenciais de usuário serão solicitadas e, após o preenchimento, uma janela do navegador será aberta. O *selenium* se encarrega de acessar páginas dos diários de classe, inserir datas, selecionar presenças para os estudantes, remover seleção para os ausentes e, nestes casos, também **lança ocorrência** para a família, indicando que tal estudante não assistiu à aula síncrona daquele dia! É tanta *automagia* que nem precisa de varinha!

![please](https://media.giphy.com/media/3o6Zt5tRWAEABTT9nO/giphy.gif)

## Alguns problemas

Eventualmente surgirão, uns mais conhecidos, outros nem tantos. Escrevi o script pensando somente no meu ambiente de trabalho, expandindo depois para outros colegas específicos utilizarem-no também. Mas podemos alterar algumas linhas de código, **na unha**, se for o caso.

### A questão do driver

Como mencionado na [seção de requerimentos](#requerimentos), estou utilizando drivers para linux e windows, nas versões ali explicitadas. Caso você utilize outras versões, precisará baixar novos drivers e salvá-los no diretório `drivers/`, que também se encontra neste repositório. Mantendo a opção de utilizar o Google Chrome, apenas certifique-se de que o nome do arquivo seja igual àquele que se encontra no diretório, ou seja, `chromedriver` para ambiente linux e `chromedriver.exe` para ambiente windows.

Entretanto, você pode optar por utilizar o navegador Safari, por exemplo —  até onde vai minha memória, ele é suportado pelo sistema Notas Online. Para isto, pode-se utilizar de uma *artimanha*, salvando o driver **também** como `chromedriver` (ou `chromedriver.exe`) na pasta `drivers/`. Não é uma solução *elegante* mas **funciona**.

Se não estiver satisfeito com tal truque sórdido, ou desejar manter os drivers originais ali sem renomeá-los, pode também fazer uma pequena modificação no código de `config.py`. Basta localizar este trecho
``` 
# inicializa o driver
# o executável depende do SO do usuário
drivers_dir = os.path.join(parent_dir, 'drivers')
user_os = platform.system()
if user_os == 'Linux':
    driver_exe = 'chromedriver'
elif user_os == 'Windows':
    driver_exe = 'chromedriver.exe'
```
substituindo os nomes `'chromedriver'` e `'chromedriver.exe'` para os nomes dos arquivos como você os salvou no diretório de drivers.

## Autor

[Pedro P. Bittencourt](pedrobittencourt.com.br), professor da educação básica e aspirante a programador.
