#!/usr/bin/python3

'''
Um deployer simples
Le o historico de commits a partir do pipe com o git log:

- git log --pretty="%H>%s" | python deploy_hook.py

O arquivo .deployhookhistory persiste o ultimo commit aplicado
O arquivo .deployhook.log persiste os logs do deployer

Para executar um comando use o !<commando no comentario>.
- Ex: git commit -m 'Atualiza dependendias !requirements'

Commandos:
    !requirements = atualiza dependencias
    !migrate = aplica migracoes
    !collectstatic = colleta arquivos estaticos
    !reset-app = reinicia o container principal
    !reset-db = reinicia o container com o banco -> nao implementado
    !reset-all = reinicia todos os servicos -> nao implementado

Eh possivel combinar comandos.
- Ex: git commit -m 'Novo app Teste !requirements !migrate !reset-app !collectstatic
'''

import os
import sys
import subprocess
import traceback

from datetime import datetime
from pathlib import Path
from optparse import OptionParser

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CONTAINER = "tracescopio-app"
MAX_SIZE_BUFFER = 1024
COMMIT_COMMENT_SEPARATOR = '>'
FILE_LAST_COMMIT_APPLIED = os.path.join(BASE_DIR, '.deployhook.history')
DEPLOYER_LOG = os.path.join(BASE_DIR,'.deployhook.log' )
AGORA = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
LOG_ENTRY = AGORA + ' - {entry}\n'
COMMIT_ENTRY = '{commit}/{agora}\n'

parser = OptionParser()
parser.add_option(
    "-c",
    "--container",
    dest="container",
    help="Define o container para receber os comandos",
)
parser.add_option("-p", "--pipe", help="Pipe com saida do GIT", default=True)

(options, args) = parser.parse_args()

def reset_app():
    cmd = "docker restart {}".format(DEFAULT_CONTAINER)
    subprocess.call(cmd, shell=True)    

if __name__ == "__main__":
    history_file = ''
    last_commit = ''
    log = ''
    reset = False
    try:
        history_file = open(FILE_LAST_COMMIT_APPLIED, 'r+')
        with history_file as hf:
            last_commit = hf.readline()
            last_commit = last_commit.split('/')[0] if last_commit else ''
        
        log = open(DEPLOYER_LOG, 'a+')
    except FileNotFoundError:
        last_commit = ''
        history_file = open(FILE_LAST_COMMIT_APPLIED, 'w').close()
        log = open(DEPLOYER_LOG, 'w').close()
        log = open(DEPLOYER_LOG, 'a+')

    log_entry = ""
    container = options.container or DEFAULT_CONTAINER
    pipe = options.pipe

    if pipe:
        for i in range(0, MAX_SIZE_BUFFER):
            log_entry += sys.stdin.read()
    
    commits = log_entry.split('\n')
    commits_to_apply = []
    commits_applied = []
    for c in commits:
        if last_commit and last_commit in c:
            break
        commits_to_apply.append(c)    
    
    with log as _log:
        for index, commit in enumerate(commits_to_apply):
            cmd = __cmd = _hash = comment = ''
            try:
                if commit:
                    _hash, comment = commit.split(COMMIT_COMMENT_SEPARATOR)
                    if not comment or not _hash:
                        _log.write(LOG_ENTRY.format(entry='Commit sem comentario? ' + _hash))
                        continue
                    
                    if '!requirements' in comment:                        
                        _log.write(LOG_ENTRY.format(entry='Aplicando dependencias ' + _hash))                        
                        cmd = "pip install -r requirements.txt"
                        __cmd = 'docker exec {} {}'.format(container, cmd)
                        subprocess.call(__cmd, shell=True)
                        reset = True

                    if '!migrate' in comment:
                        _log.write(LOG_ENTRY.format(entry='Aplicando migrations ' + _hash))
                        cmd = "python manage.py migrate_schemas"
                        __cmd = 'docker exec {} {}'.format(container, cmd)
                        subprocess.call(__cmd, shell=True)
                        reset = True
                    
                    if '!collectstatic' in comment:
                        _log.write(LOG_ENTRY.format(entry='Coletando estaticos ' + _hash))
                        cmd = "python manage.py collectstatic --noinput"
                        __cmd = 'docker exec {} {}'.format(container, cmd)
                        subprocess.call(__cmd, shell=True)
                        reset = True

                    if '!reset-app' in comment:
                        _log.write(LOG_ENTRY.format(entry='Reiniciando o container (app) ' + _hash))
                        cmd = "docker restart {}".format(DEFAULT_CONTAINER)
                        subprocess.call(__cmd, shell=True)
                        reset = False
                    
                    if reset:
                        reset_app()
                    
                    # para historico de commits
                    agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    _value = COMMIT_ENTRY.format(commit=_hash, agora=agora)
                    commits_applied.append(_value)
            
            except Exception as error:
                # commit sem comentario?
                _trace = traceback.format_exc()
                with log as _log:
                    _log.write(LOG_ENTRY.format(entry='ERROR: '+ str(index) + str(error) + ':\n' + _trace))
                continue
    
    
    if commits_applied:
        with open(FILE_LAST_COMMIT_APPLIED, 'w+') as hf:
            for _c in commits_applied:
                hf.write(_c)
    
    sys.exit(0)

