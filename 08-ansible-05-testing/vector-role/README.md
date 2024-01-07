Vector
=========

- Загрузка и установка агрегатора логов Vector
- Создание модуля systemd для управления службой Vector
- Настройка конфигурации Vector для сбора логов NGINX и последующей передачи Clickhouse

Requirements
------------

Поддерживаются только RPM-based дистрибутивы

Для работы необходимы ```Clickhouse``` и ```nginx```

Role Variables
--------------

```vector_version```- доступная версия vector

```vector_conf_dir``` - каталог хранения конфигурации vector

Dependencies
------------
Параметры конфигурации для сбора логов указаны в файле
```/templates/vector.conf.j2```:

```endpoint = "http://127.0.0.1:8123"``` - 
выгрузка осуществляется в Clickhouse установленный на том же сервере

```database = "nginxdb"``` - имя БД Clickhouse по-умолчанию для выгрузки логов

```table = "log"``` - таблица в БД ```nginxdb``` для хранения логов

Example Playbook
----------------

```
    - hosts: vector
      roles:
         - vector-role
```
License
-------

BSD

Author Information
------------------
