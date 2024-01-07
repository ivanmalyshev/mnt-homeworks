# Домашнее задание к занятию 5 «Тестирование roles»

## Подготовка к выполнению

1. Установите molecule: `pip3 install "molecule==3.5.2"` и драйвера `pip3 install molecule_docker molecule_podman`.
2. Выполните `docker pull aragast/netology:latest` —  это образ с podman, tox и несколькими пайтонами (3.7 и 3.9) внутри.

## Основная часть

Ваша цель — настроить тестирование ваших ролей.

Задача — сделать сценарии тестирования для vector.

Ожидаемый результат — все сценарии успешно проходят тестирование ролей.

### Molecule

1. Запустите  `molecule test -s centos_7` внутри корневой директории clickhouse-role, посмотрите на вывод команды. Данная команда может отработать с ошибками, это нормально. Наша цель - посмотреть как другие в реальном мире используют молекулу.
2. Перейдите в каталог с ролью vector-role и создайте сценарий тестирования по умолчанию при помощи `molecule init scenario --driver-name docker`.
3. Добавьте несколько разных дистрибутивов (centos:8, ubuntu:latest) для инстансов и протестируйте роль, исправьте найденные ошибки, если они есть.
4. Добавьте несколько assert в verify.yml-файл для  проверки работоспособности vector-role (проверка, что конфиг валидный, проверка успешности запуска и др.).
5. Запустите тестирование роли повторно и проверьте, что оно прошло успешно.
5. Добавьте новый тег на коммит с рабочим сценарием в соответствии с семантическим версионированием.

### Tox

1. Добавьте в директорию с vector-role файлы из [директории](./example).
2. Запустите `docker run --privileged=True -v <path_to_repo>:/opt/vector-role -w /opt/vector-role -it aragast/netology:latest /bin/bash`, где path_to_repo — путь до корня репозитория с vector-role на вашей файловой системе.
3. Внутри контейнера выполните команду `tox`, посмотрите на вывод.
5. Создайте облегчённый сценарий для `molecule` с драйвером `molecule_podman`. Проверьте его на исполнимость.
6. Пропишите правильную команду в `tox.ini`, чтобы запускался облегчённый сценарий.
8. Запустите команду `tox`. Убедитесь, что всё отработало успешно.
9. Добавьте новый тег на коммит с рабочим сценарием в соответствии с семантическим версионированием.

После выполнения у вас должно получится два сценария molecule и один tox.ini файл в репозитории. Не забудьте указать в ответе теги решений Tox и Molecule заданий. В качестве решения пришлите ссылку на  ваш репозиторий и скриншоты этапов выполнения задания.

## Необязательная часть

1. Проделайте схожие манипуляции для создания роли LightHouse.
2. Создайте сценарий внутри любой из своих ролей, который умеет поднимать весь стек при помощи всех ролей.
3. Убедитесь в работоспособности своего стека. Создайте отдельный verify.yml, который будет проверять работоспособность интеграции всех инструментов между ними.
4. Выложите свои roles в репозитории.

В качестве решения пришлите ссылки и скриншоты этапов выполнения задания.

---

### Как оформить решение задания

Выполненное домашнее задание пришлите в виде ссылки на .md-файл в вашем репозитории.


---

### Molecule

## 1. Команда не сработает, т.к. по дефолту нет параметров для centos 7.
```bash
mid@mid-desktop:~/Nextcloud/netology/ans_cicd_mon/mnt-homeworks/08-ansible-05-testing$ cd clickhouse/
mid@mid-desktop:~/Nextcloud/netology/ans_cicd_mon/mnt-homeworks/08-ansible-05-testing/clickhouse$ molecule test -s centos_7
CRITICAL 'molecule/centos_7/molecule.yml' glob failed.  Exiting.
mid@mid-desktop:~/Nextcloud/netology/ans_cicd_mon/mnt-homeworks/08-ansible-05-testing/clickhouse$ ^C
mid@mid-desktop:~/Nextcloud/netology/ans_cicd_mon/mnt-homeworks/08-ansible-05-testing/clickhouse$
```

## 2-3. molecule_step3

```bash
Please edit meta/main.yml and assure we can correctly determine full role name:

galaxy_info:
role_name: my_name  # if absent directory name hosting role is used instead
namespace: my_galaxy_namespace  # if absent, author is used instead

Namespace: https://galaxy.ansible.com/docs/contributing/namespaces.html#galaxy-namespace-limitations
Role: https://galaxy.ansible.com/docs/contributing/creating_role.html#role-names

As an alternative, you can add 'role-name' to either skip_list or warn_list.
```

В начале `molecule test` не запускался из-за неправильных meta-данных. Не был указан role-name. Исправил - тест пошел

Повторный запуск
```bash
PLAY [Verify] ******************************************************************

TASK [Validation Vector configuration] *****************************************
fatal: [centos8]: FAILED! => {"ansible_facts": {"discovered_interpreter_python": "/usr/libexec/platform-python"}, "changed": false, "cmd": "vector validate --no-environment --config-toml /etc/vector/vector.toml", "msg": "[Errno 2] No such file or directory: b'vector': b'vector'", "rc": 2, "stderr": "", "stderr_lines": [], "stdout": "", "stdout_lines": []}
fatal: [ubuntu]: FAILED! => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3"}, "changed": false, "cmd": "vector validate --no-environment --config-toml /etc/vector/vector.toml", "msg": "[Errno 2] No such file or directory: b'vector': b'vector'", "rc": 2, "stderr": "", "stderr_lines": [], "stdout": "", "stdout_lines": []}


```

Так и не удалось победить - не работает :)

[vector-role release v0.0.2](https://github.com/ivanmalyshev/vector-role/releases/tag/0.0.2)

## Tox

```bash
docker run --privileged=True -v ./:/opt/vector-role -w /opt/vector-role -it aragast/netology:latest /bin/bash
[root@d2e2c1ec3047 vector-role]# tox
py39-ansible30 create: /opt/vector-role/.tox/py39-ansible30
py39-ansible30 installdeps: -rtox-requirements.txt, ansible<3.1
py39-ansible30 installed: ansible==3.0.0,ansible-base==2.10.17,ansible-compat==4.1.10,ansible-core==2.15.8,ansible-lint==5.1.3,arrow==1.3.0,attrs==23.2.0,bcrypt==4.1.2,binaryornot==0.4.4,bracex==2.4,Cerberus==1.3.5,certifi==2023.11.17,cffi==1.16.0,chardet==5.2.0,charset-normalizer==3.3.2,click==8.1.7,click-help-colors==0.9.4,cookiecutter==2.5.0,cryptography==41.0.7,distro==1.9.0,enrich==1.2.7,idna==3.6,importlib-resources==5.0.7,Jinja2==3.1.2,jmespath==1.0.1,jsonschema==4.20.0,jsonschema-specifications==2023.12.1,lxml==5.0.1,markdown-it-py==3.0.0,MarkupSafe==2.1.3,mdurl==0.1.2,molecule==3.5.2,molecule-podman==2.0.0,packaging==23.2,paramiko==2.12.0,pathspec==0.12.1,pluggy==1.3.0,pycparser==2.21,Pygments==2.17.2,PyNaCl==1.5.0,python-dateutil==2.8.2,python-slugify==8.0.1,PyYAML==5.4.1,referencing==0.32.1,requests==2.31.0,resolvelib==1.0.1,rich==13.7.0,rpds-py==0.16.2,ruamel.yaml==0.18.5,ruamel.yaml.clib==0.2.8,selinux==0.3.0,six==1.16.0,subprocess-tee==0.4.1,tenacity==8.2.3,text-unidecode==1.3,types-python-dateutil==2.8.19.20240106,typing_extensions==4.9.0,urllib3==2.1.0,wcmatch==8.5,yamllint==1.26.3
py39-ansible30 run-test-pre: PYTHONHASHSEED='3556110078'
py39-ansible30 run-test: commands[0] | molecule test -s compatibility --destroy always
CRITICAL 'molecule/compatibility/molecule.yml' glob failed.  Exiting.
ERROR: InvocationError for command /opt/vector-role/.tox/py39-ansible30/bin/molecule test -s compatibility --destroy always (exited with code 1)
_____________________________________________________________________________________ summary ______________________________________________________________________________________
ERROR:   py37-ansible210: commands failed
ERROR:   py37-ansible30: commands failed
ERROR:   py39-ansible210: commands failed
ERROR:   py39-ansible30: commands failed
```

команда в tox.ini
```bash
commands =
    {posargs:molecule test -s tox --destroy always}
```

[Вывод команды tox](tox_output)


[ссылка на модуль с tox тестами](https://github.com/ivanmalyshev/vector-role/releases/tag/0.0.3)
