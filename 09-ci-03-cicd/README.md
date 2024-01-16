# Домашнее задание к занятию 9 «Процессы CI/CD»

## Подготовка к выполнению

1. Создайте два VM в Yandex Cloud с параметрами: 2CPU 4RAM Centos7 (остальное по минимальным требованиям).
2. Пропишите в [inventory](./infrastructure/inventory/cicd/hosts.yml) [playbook](./infrastructure/site.yml) созданные хосты.
3. Добавьте в [files](./infrastructure/files/) файл со своим публичным ключом (id_rsa.pub). Если ключ называется иначе — найдите таску в плейбуке, которая использует id_rsa.pub имя, и исправьте на своё.
4. Запустите playbook, ожидайте успешного завершения.
5. Проверьте готовность SonarQube через [браузер](http://localhost:9000).
6. Зайдите под admin\admin, поменяйте пароль на свой.
7.  Проверьте готовность Nexus через [бразуер](http://localhost:8081).
8. Подключитесь под admin\admin123, поменяйте пароль, сохраните анонимный доступ.

## Знакомоство с SonarQube

### Основная часть

1. Создайте новый проект, название произвольное.
2. Скачайте пакет sonar-scanner, который вам предлагает скачать SonarQube.
3. Сделайте так, чтобы binary был доступен через вызов в shell (или поменяйте переменную PATH, или любой другой, удобный вам способ).
4. Проверьте `sonar-scanner --version`.
5. Запустите анализатор против кода из директории [example](./example) с дополнительным ключом `-Dsonar.coverage.exclusions=fail.py`.
6. Посмотрите результат в интерфейсе.
7. Исправьте ошибки, которые он выявил, включая warnings.
8. Запустите анализатор повторно — проверьте, что QG пройдены успешно.
9. Сделайте скриншот успешного прохождения анализа, приложите к решению ДЗ.

## Знакомство с Nexus

### Основная часть

1. В репозиторий `maven-public` загрузите артефакт с GAV-параметрами:

 *    groupId: netology;
 *    artifactId: java;
 *    version: 8_282;
 *    classifier: distrib;
 *    type: tar.gz.

2. В него же загрузите такой же артефакт, но с version: 8_102.
3. Проверьте, что все файлы загрузились успешно.
4. В ответе пришлите файл `maven-metadata.xml` для этого артефекта.

### Знакомство с Maven

### Подготовка к выполнению

1. Скачайте дистрибутив с [maven](https://maven.apache.org/download.cgi).
2. Разархивируйте, сделайте так, чтобы binary был доступен через вызов в shell (или поменяйте переменную PATH, или любой другой, удобный вам способ).
3. Удалите из `apache-maven-<version>/conf/settings.xml` упоминание о правиле, отвергающем HTTP- соединение — раздел mirrors —> id: my-repository-http-unblocker.
4. Проверьте `mvn --version`.
5. Заберите директорию [mvn](./mvn) с pom.

### Основная часть

1. Поменяйте в `pom.xml` блок с зависимостями под ваш артефакт из первого пункта задания для Nexus (java с версией 8_282).
2. Запустите команду `mvn package` в директории с `pom.xml`, ожидайте успешного окончания.
3. Проверьте директорию `~/.m2/repository/`, найдите ваш артефакт.
4. В ответе пришлите исправленный файл `pom.xml`.

---

### Как оформить решение задания

Выполненное домашнее задание пришлите в виде ссылки на .md-файл в вашем репозитории.

---



#### Выполнение работы

Не работает плейбук - не ставится postgres на centos7

Валится на установке самого пакета.

![question1](https://github.com/ivanmalyshev/mnt-homeworks/blob/MNT-video/09-ci-03-cicd/question1.png)
![question2](https://github.com/ivanmalyshev/mnt-homeworks/blob/MNT-video/09-ci-03-cicd/question2.png)


Репозиторий PostgreSQL не содержит информацию 11 версии.
![question2](https://github.com/ivanmalyshev/mnt-homeworks/blob/MNT-video/09-ci-03-cicd/question3.png)

так и не смог победить, как не старался - не ставится. Какие могут быть рекомендации к исправлению?


UPD:
решил путем установки postgres12 - возможно стоит поправить ТЗ?


```bash
TASK [Wait for Nexus port if started] ********************************************************************************************************************************************************
ok: [nexus-01]

PLAY RECAP ***********************************************************************************************************************************************************************************
nexus-01                   : ok=17   changed=15   unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
sonar-01                   : ok=34   changed=16   unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
```


## Знакомоство с SonarQube

![sonar-bug](https://github.com/ivanmalyshev/mnt-homeworks/blob/postgres12/09-ci-03-cicd/sonar/sonar-bug.png)

![sonar-fixbug](https://github.com/ivanmalyshev/mnt-homeworks/blob/postgres12/09-ci-03-cicd/sonar/sonar-fixbug.png)

![sonar-fixbug](https://github.com/ivanmalyshev/mnt-homeworks/blob/postgres12/09-ci-03-cicd/sonar/warnings.png)

Для фикса варнингов использовал
```bash
sonar-scanner  \
-Dsonar.projectKey=mid-netology \
-Dsonar.sources=. \
-Dsonar.host.url=http://158.160.106.92:9000  \
-Dsonar.login=3bc6951cd4eb3a56d03b8d0c187e48ec7e575312 \
-Dsonar.coverage.exclusions=fail.py \
-Dsonar.python.version=2.7,3.7 \
-Dsonar.scm.disabled=true
```
Dsonar.python.version=2.7,3.7 - устанавливает точную версию интерпритатора

Dsonar.scm.disabled=true - Отключение плагина SCM. Используется для сбора данных из системы контроля во время анализа кода


## Знакомство с Nexus

![meta](https://github.com/ivanmalyshev/mnt-homeworks/blob/postgres12/09-ci-03-cicd/mvn/nexus.png)

ссылка на файл metadata.xml
![meta](https://github.com/ivanmalyshev/mnt-homeworks/blob/postgres12/09-ci-03-cicd/mvn/maven-metadata.xml)



## Знакомство с Maven

![meta](https://github.com/ivanmalyshev/mnt-homeworks/blob/postgres12/09-ci-03-cicd/mvn/mvn-build.png)


Артефакт загружен
```bash
mid@mid-desktop:~/.m2/repository/netology/java/8_282$ ls
java-8_282-distrib.tar.gz  java-8_282-distrib.tar.gz.sha1  java-8_282.pom.lastUpdated  _remote.repositories
mid@mid-desktop:~/.m2/repository/netology/java/8_282$
```

ссылка на pom-файл
(https://github.com/ivanmalyshev/mnt-homeworks/blob/postgres12/09-ci-03-cicd/mvn/pom.xml)