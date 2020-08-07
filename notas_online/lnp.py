from datetime import datetime
import logging

# set up logging to file
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='/home/monolito/scripts/notas_online/ocorrencias.log',
                    filemode='a')

# create logger object
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)

# set a format which is simpler for console use
formatter = logging.Formatter('%(levelname)-8s %(message)s')

# tell the handler to use this format
console.setFormatter(formatter)

# add handler to logger
logger.addHandler(console)

# 'application' code
now = datetime.now().strftime('%d-%b-%Y (%H:%M:%S)')
logger.info(f'Acesso à página efetuado em {now}.')

