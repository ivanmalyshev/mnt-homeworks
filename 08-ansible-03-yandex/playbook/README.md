Документация к плейбуку `site.yml`

Содержит 3 блока задач.

---

name: Installation NGINX

name: Install Lighthouse

Первый блок устанавливает `nginx` и скачивает статику для `Lighthouse`.  
Все используемые переменные в `group_vars/lighthouse/lighthouse.yml`:

1. `nginx_user_name: root` для конфига в nginx.j2 
2. `lighthouse_repo` репозиторий git с lighthouse
3. `lighthouse_location_dir` директория для установки статики lighthouse 

### Tasks

`Install nginx` - устанавливает nginx с репозиториев через модуль `ansible.builtin.yum:`,

`Creating config` копирует дефолтный конфиг nginx.conf из шаблона nginx.j2 через модуль `ansible.builtin.template`, перезапускает nginx через `ansible.builtin.service`

`Lighthouse ----- Installing Git` - устанавливает git для скачивания Lighthouse (`ansible.builtin.yum:`), 

`Lighthouse ----- Downloading Lighthouse` загружает Lighthouse с репозитория (`ansible.builtin.git`),

`Lighthouse ----- Creating lighthouse vector config` копирует конфиг lighthouse (`ansible.builtin.template`), перезапускает nginx через notify.

---

name: Install Clickhouse

Второй блок устанавливает `Clickhouse`
Все используемые переменные в `group_vars/сlickhouse/сlickhouse.yml`:

1. `clickhouse_version` версия clickhouse для установки
2. `clickhouse_packages` список устанавливаемых пакетов

### Tasks

`Get clickhouse distrib` - скачивает необходимые пакеты через `ansible.builtin.get_url` переименовывает в соотвествии с переменными `{{ item }}-{{ clickhouse_version }}`

`Install clickhouse packages` - производит установку необходимых пакетов (`ansible.builtin.yum`), стартует сервисы через хендлер `Start clickhouse service`

`Pause playbook for start clickhouse` - пауза выполнения плейбука, для ожидания старта сервиса Clickhouse (`ansible.builtin.pause`)

`Create database` - создание БД (`ansible.builtin.command`)

---

### name: Install Vector

Третий блок устанавливает `Vector`
Все используемые переменные в `group_vars/vector/vector.yml`:
1. `vector_url` ссылка для загрузки Vector, включает в себя версию, вызываемую в `vector_version`
2. `vector_config_dir` директория конфига Vector
3. `vector ip` ip-адрес машины, используется в конфиге для endpoint'a
4. `vector_config` - конфиг вектора в yaml-формате

### Tasks

`Vector | Download packages` загрузка необходимого пакета через `ansible.builtin.get_url`

`Vector | Install packages` установка через `ansible.builtin.yum`

`Vector | Apply template` копирование шаблона через `ansible.builtin.template`

`Vector | change systemd unit` копирование шаблона сервиса через `ansible.builtin.template`

Перезапуск сервиса Vector через notify `Start Vector service`



