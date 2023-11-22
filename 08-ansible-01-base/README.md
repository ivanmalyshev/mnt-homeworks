# Домашнее задание к занятию 1 «Введение в Ansible»

## Подготовка к выполнению

1. Установите Ansible версии 2.10 или выше.
2. Создайте свой публичный репозиторий на GitHub с произвольным именем.
3. Скачайте [Playbook](./playbook/) из репозитория с домашним заданием и перенесите его в свой репозиторий.

## Основная часть

1. Попробуйте запустить playbook на окружении из `test.yml`, зафиксируйте значение, которое имеет факт `some_fact` для указанного хоста при выполнении playbook.
2. Найдите файл с переменными (group_vars), в котором задаётся найденное в первом пункте значение, и поменяйте его на `all default fact`.
3. Воспользуйтесь подготовленным (используется `docker`) или создайте собственное окружение для проведения дальнейших испытаний.
4. Проведите запуск playbook на окружении из `prod.yml`. Зафиксируйте полученные значения `some_fact` для каждого из `managed host`.
5. Добавьте факты в `group_vars` каждой из групп хостов так, чтобы для `some_fact` получились значения: для `deb` — `deb default fact`, для `el` — `el default fact`.
6.  Повторите запуск playbook на окружении `prod.yml`. Убедитесь, что выдаются корректные значения для всех хостов.
7. При помощи `ansible-vault` зашифруйте факты в `group_vars/deb` и `group_vars/el` с паролем `netology`.
8. Запустите playbook на окружении `prod.yml`. При запуске `ansible` должен запросить у вас пароль. Убедитесь в работоспособности.
9. Посмотрите при помощи `ansible-doc` список плагинов для подключения. Выберите подходящий для работы на `control node`.
10. В `prod.yml` добавьте новую группу хостов с именем  `local`, в ней разместите localhost с необходимым типом подключения.
11. Запустите playbook на окружении `prod.yml`. При запуске `ansible` должен запросить у вас пароль. Убедитесь, что факты `some_fact` для каждого из хостов определены из верных `group_vars`.
12. Заполните `README.md` ответами на вопросы. Сделайте `git push` в ветку `master`. В ответе отправьте ссылку на ваш открытый репозиторий с изменённым `playbook` и заполненным `README.md`.
13. Предоставьте скриншоты результатов запуска команд.

---

## Ответ

1. Запуск плейбука
```bash

ansible-playbook playbook/site.yml -i playbook/inventory/test.yml 

PLAY [Print os facts] ************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************
ok: [localhost]

TASK [Print OS] ******************************************************************************************************************************************************************************
ok: [localhost] => {
    "msg": "Ubuntu"
}

TASK [Print fact] ****************************************************************************************************************************************************************************
ok: [localhost] => {
    "msg": 12
}

PLAY RECAP ***********************************************************************************************************************************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 
```

2. Замена значений
```bash
ansible-playbook playbook/site.yml -i playbook/inventory/test.yml 

PLAY [Print os facts] ************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************
ok: [localhost]

TASK [Print OS] ******************************************************************************************************************************************************************************
ok: [localhost] => {
    "msg": "Ubuntu"
}

TASK [Print fact] ****************************************************************************************************************************************************************************
ok: [localhost] => {
    "msg": "all default fact"
}

PLAY RECAP ***********************************************************************************************************************************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 
```
3. Для решения задания поднимем 2 докер контейнера
```bash
docker run -d --name=centos7 centos/python-36-centos7:latest sleep 600
Unable to find image 'centos/python-36-centos7:latest' locally
latest: Pulling from centos/python-36-centos7
75f829a71a1c: Pull complete 
e2c4942f4189: Pull complete 
f1498894b11c: Pull complete 
da56c9694723: Pull complete 
07fa76fc639e: Pull complete 
abab42dfb7f7: Pull complete 
dd73d54fbd62: Pull complete 
25966a5cbd52: Pull complete 
b947aec7d116: Pull complete 
Digest: sha256:ac50754646f0d37616515fb30467d8743fb12954260ec36c9ecb5a94499447e0
Status: Downloaded newer image for centos/python-36-centos7:latest
d8e1528c9cab09ce75a9b09f68508515e890fc276217a0fb95469a480790a78d

docker run -d --name=ubuntu python:3.9.18-bullseye sleep 600
Unable to find image 'python:3.9.18-bullseye' locally
3.9.18-bullseye: Pulling from library/python
d1da99c2f148: Pull complete 
577ff23cfe55: Pull complete 
c7b1e60e9d5a: Pull complete 
beefab36cbfe: Pull complete 
de3224efe726: Pull complete 
75fc8b83272d: Pull complete 
c353937fd1d8: Pull complete 
b218b8cd1189: Pull complete 
Digest: sha256:73415eae5a61f76b080bf18b90fa5ae43e69eaedbddc969dad0a3768a19c19b4
Status: Downloaded newer image for python:3.9.18-bullseye
88900bfd4deb5e5dd8868e6fbf5b1e43b17779a3435d09b4d0d2ca1d2ca1e093

```

и плагин для докер-контейнера из коллекции ансибла 
`ansible-galaxy collection install community.docker`

Проверяем - все работает, контейнеры живут и можно к ним подключатся с ансибла по имени
```bash
 docker ps
CONTAINER ID   IMAGE                             COMMAND                  CREATED          STATUS          PORTS      NAMES
d8e1528c9cab   centos/python-36-centos7:latest   "container-entrypoin…"   29 seconds ago   Up 28 seconds   8080/tcp   centos7
88900bfd4deb   python:3.9.18-bullseye            "sleep 600"              3 minutes ago    Up 2 minutes               ubuntu
```

4. Запуск плейбука для докер-контейнеров
```bash
ansible-playbook playbook/site.yml -i playbook/inventory/prod.yml 

PLAY [Print os facts] ************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] ******************************************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Debian"
}

TASK [Print fact] ****************************************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "el"
}
ok: [ubuntu] => {
    "msg": "deb"
}

PLAY RECAP ***********************************************************************************************************************************************************************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 
```

5. Добавил some_facts
```bash
TASK [Print OS] ******************************************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Debian"
}

TASK [Print fact] ****************************************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "el default"
}
ok: [ubuntu] => {
    "msg": "deb default"
}
```

7. Шифрование

```bash
ansible-vault create playbook/group_vars/deb/examp.yml 
New Vault password: 
Confirm New Vault password: 

ansible-vault encrypt playbook/group_vars/el/examp.yml 
New Vault password: 
Confirm New Vault password: 
Encryption successful
```

8. Проверка плейбука после шифрования

```bash
ansible-playbook playbook/site.yml -i playbook/inventory/prod.yml --ask-vault-pass
Vault password: 

PLAY [Print os facts] ************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] ******************************************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Debian"
```

9. Судя по всему модуль `local` нам и требуется
```bash
ansible-doc -t connection -l
community.docker.docker     Run tasks in docker containers                                                                                                                               
community.docker.docker_api Run tasks in docker containers                                                                                                                               
community.docker.nsenter    execute on host running controller container                                                                                                                 
local                       execute on controller                                                                                                                                        
paramiko_ssh                Run tasks via python ssh (paramiko)                                                                                                                          
psrp                        Run tasks over Microsoft PowerShell Remoting Protocol                                                                                                        
ssh                         connect via SSH client binary                                                                                                                              
winrm                       Run tasks over Microsoft's WinRM                     
```
10. Добавил в плейбук вызов localhost
```yaml
  local:
    hosts:
       local:
         ansible_connection: local
```
11. Запуск плейбука

```bash
TASK [Print fact] ****************************************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "el default"
}
ok: [ubuntu] => {
    "msg": "deb default"
}
ok: [local] => {
    "msg": "all default fact"
}
```

## Необязательная часть

1. При помощи `ansible-vault` расшифруйте все зашифрованные файлы с переменными.
2. Зашифруйте отдельное значение `PaSSw0rd` для переменной `some_fact` паролем `netology`. Добавьте полученное значение в `group_vars/all/exmp.yml`.
3. Запустите `playbook`, убедитесь, что для нужных хостов применился новый `fact`.
4. Добавьте новую группу хостов `fedora`, самостоятельно придумайте для неё переменную. В качестве образа можно использовать [этот вариант](https://hub.docker.com/r/pycontribs/fedora).
5. Напишите скрипт на bash: автоматизируйте поднятие необходимых контейнеров, запуск ansible-playbook и остановку контейнеров.
6. Все изменения должны быть зафиксированы и отправлены в ваш личный репозиторий.

---

### Как оформить решение задания

Выполненное домашнее задание пришлите в виде ссылки на .md-файл в вашем репозитории.

---
