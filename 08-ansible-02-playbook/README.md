# Домашнее задание к занятию 2 «Работа с Playbook»

## Подготовка к выполнению

1. * Необязательно. Изучите, что такое [ClickHouse](https://www.youtube.com/watch?v=fjTNS2zkeBs) и [Vector](https://www.youtube.com/watch?v=CgEhyffisLY).
2. Создайте свой публичный репозиторий на GitHub с произвольным именем или используйте старый.
3. Скачайте [Playbook](./playbook/) из репозитория с домашним заданием и перенесите его в свой репозиторий.
4. Подготовьте хосты в соответствии с группами из предподготовленного playbook.

## Основная часть

1. Подготовьте свой inventory-файл `prod.yml`.
2. Допишите playbook: нужно сделать ещё один play, который устанавливает и настраивает [vector](https://vector.dev). Конфигурация vector должна деплоиться через template файл jinja2. От вас не требуется использовать все возможности шаблонизатора, просто вставьте стандартный конфиг в template файл. Информация по шаблонам по [ссылке](https://www.dmosk.ru/instruktions.php?object=ansible-nginx-install).
3. При создании tasks рекомендую использовать модули: `get_url`, `template`, `unarchive`, `file`.
4. Tasks должны: скачать дистрибутив нужной версии, выполнить распаковку в выбранную директорию, установить vector.
5. Запустите `ansible-lint site.yml` и исправьте ошибки, если они есть.
6. Попробуйте запустить playbook на этом окружении с флагом `--check`.
7. Запустите playbook на `prod.yml` окружении с флагом `--diff`. Убедитесь, что изменения на системе произведены.
8. Повторно запустите playbook с флагом `--diff` и убедитесь, что playbook идемпотентен.
9. Подготовьте README.md-файл по своему playbook. В нём должно быть описано: что делает playbook, какие у него есть параметры и теги. Пример качественной документации ansible playbook по [ссылке](https://github.com/opensearch-project/ansible-playbook).
10. Готовый playbook выложите в свой репозиторий, поставьте тег `08-ansible-02-playbook` на фиксирующий коммит, в ответ предоставьте ссылку на него.

---

### Как оформить решение задания

Выполненное домашнее задание пришлите в виде ссылки на .md-файл в вашем репозитории.

---

## Ответ
1. Настроен отдельный хост в файле инвентори
`prod.yml`
```yaml
clickhouse:
  hosts:
    clickhouse-01:
      ansible_host: 178.154.202.169
      ansible_user: ansible
```

проверка через ad-hoc 
```bash
ansible all -i playbook/inventory/prod.yml -m ping
clickhouse-01 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
```

2. добавлены файлы с темплейтами в `playbook/templates`

5. ansible-lint - убрал лишние пустые строки в конце плейбука

```bash
mid@mid-desktop:~/Nextcloud/netology/ans_cicd_mon/mnt-homeworks/08-ansible-02-playbook$ ansible-lint playbook/site.yml
[201] Trailing whitespace
playbook/site.yml:81
        

[201] Trailing whitespace
playbook/site.yml:82
        

mid@mid-desktop:~/Nextcloud/netology/ans_cicd_mon/mnt-homeworks/08-ansible-02-playbook$ ansible-lint playbook/site.yml
mid@mid-desktop:~/Nextcloud/netology/ans_cicd_mon/mnt-homeworks/08-ansible-02-playbook$
```

6-8. Вывод работы плейбука
```bash
ansible-playbook -i playbook/inventory/prod.yml playbook/site.yml --become 

PLAY [Install Clickhouse] **********************************************************************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************************************************************************
ok: [clickhouse-01]

TASK [Get clickhouse distrib] ******************************************************************************************************************************************************
ok: [clickhouse-01] => (item=clickhouse-client)
ok: [clickhouse-01] => (item=clickhouse-server)
ok: [clickhouse-01] => (item=clickhouse-common-static)

TASK [Install clickhouse packages] *************************************************************************************************************************************************
ok: [clickhouse-01]

TASK [Flush handlers] **************************************************************************************************************************************************************

TASK [Create database] *************************************************************************************************************************************************************
ok: [clickhouse-01]

PLAY [Install Vector] **************************************************************************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************************************************************************
ok: [clickhouse-01]

TASK [Vector | Download packages] **************************************************************************************************************************************************
ok: [clickhouse-01]

TASK [Vector | Install packages] ***************************************************************************************************************************************************
ok: [clickhouse-01]

TASK [Vector | Apply template] *****************************************************************************************************************************************************
changed: [clickhouse-01]

TASK [Vector | change systemd unit] ************************************************************************************************************************************************
ok: [clickhouse-01]

PLAY RECAP *************************************************************************************************************************************************************************
clickhouse-01              : ok=9    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

Выводы конф-файлов из машины

Сервисы в работе
```bash
[root@clickhouse log]# service vector status
Redirecting to /bin/systemctl status vector.service
● vector.service - Vector
   Loaded: loaded (/usr/lib/systemd/system/vector.service; disabled; vendor preset: disabled)
  Drop-In: /run/systemd/system/vector.service.d
           └─zzz-lxc-service.conf
   Active: active (running) since Mon 2023-11-27 14:18:18 UTC; 3min 46s ago
     Docs: https://vector.dev
 Main PID: 7731 (vector)
    Tasks: 5 (limit: 26213)
   Memory: 12.5M
   CGroup: /system.slice/vector.service
           └─7731 /usr/bin/vector --config /etc/vector/vector.yml

[root@clickhouse log]# service clickhouse-server status
/var/run/clickhouse-server/clickhouse-server.pid file exists and contains pid = 2758.
The process with pid = 2758 is running.
```
```bash
[root@clickhouse log]# cat /etc/vector/vector.yml 
sinks:
    to_clickhouse:
        compression: gzip
        database: logs
        endpoint: http://127.0.0.1:8123
        healthcheck: true
        inputs:
        - demo_logs
        skip_unknown_fields: true
        table: vector_table
        type: clickhouse
sources:
    demo_logs:
        format: syslog
        type: demo_logs

```
`add tag 08-ansible-02-playbook `

Раскатывал и в я.облако и локально на вм в проксмксе - повторяется и там и там. 

