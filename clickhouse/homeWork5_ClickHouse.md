
### Условия ДЗ ###
Необходимо, используя туториал https://clickhouse.tech/docs/ru/getting-started/tutorial/ :
- развернуть инстанс;
- выполнить импорт тестовой БД;
- выполнить несколько запросов и оценить скорость выполнения.

Дз сдается в виде миниотчета.
* развернуть дополнительно одну из тестовых БД https://clickhouse.com/docs/en/getting-started/example-datasets , протестировать скорость запросов
 ** развернуть Кликхаус в кластерном исполнении, создать распределенную таблицу, заполнить данными и протестировать скорость


### **Задание 1** ###


_compose_

```
version: '3.9'
services:
  clickhouse:
    image: clickhouse/clickhouse-server
    container_name: clickhouse
    volumes:
        - ${PWD}/ch_data:/var/lib/clickhouse/
        - ${PWD}/ch_logs:/var/log/clickhouse-server/
    ports:
        - '8123:8123'
        - '9000:9000'
```

_docker pull clickhouse/clickhouse-server
docker compose -f  "docker-compose.yml" up -d --build_

Подключился проверить что работает
_docker exec -it clickhouse clickhouse-client_

Скачал клиент и запустил 
_curl https://clickhouse.com/ | sh
./clickhouse client_


Сложность для macOS с импортированием данных 
	- или скачиввать для мака немного изменив команду 
	- Или внутри контейнера (установив нужные пакеты)

_curl https://datasets.clickhouse.com/visits/tsv/visits_v1.tsv.xz | xzcat > visits_v1.tsv
clickhouse-client --query "CREATE DATABASE IF NOT EXISTS tutorial"_

Дальше создание таблиц (большой запрос из доки, можно найти по ссылке.)

Проимпортировал БД

_➜  ch ./clickhouse client --query "INSERT INTO tutorial.hits_v1 FORMAT TSV" --max_insert_block_size=100000 < hits_v1.tsv
➜  ch ./clickhouse client --query "INSERT INTO tutorial.visits_v1 FORMAT TSV" --max_insert_block_size=100000 < visits_v1.tsv_

Попробовал выполнить селект всей таблицы
_select * from hits_v1_

8873898 rows in set. Elapsed: 13.113 sec. Processed 8.87 million rows, 6.73 GB (676.73 thousand rows/s., 512.87 MB/s.)
Peak memory usage: 354.23 MiB.

_SELECT
    StartURL AS URL,
    AVG(Duration) AS AvgDuration
FROM tutorial.visits_v1
WHERE StartDate BETWEEN '2014-03-23' AND '2014-03-30'
GROUP BY URL
ORDER BY AvgDuration DESC
LIMIT 10_

10 rows in set. Elapsed: 0.157 sec. Processed 1.47 million rows, 114.62 MB (9.40 million rows/s., 731.39 MB/s.)
Peak memory usage: 50.75 MiB.

_SELECT
    sum(Sign) AS visits,
    sumIf(Sign, has(Goals.ID, 1105530)) AS goal_visits,
    (100. * goal_visits) / visits AS goal_percent
FROM tutorial.visits_v1
WHERE (CounterID = 912887) AND (toYYYYMM(StartDate) = 201403)_

1 row in set. Elapsed: 0.049 sec. Processed 46.57 thousand rows, 1.25 MB (960.05 thousand rows/s., 25.71 MB/s.)
Peak memory usage: 122.82 KiB.

### **Задание с одной звездочкой** ###
https://clickhouse.com/docs/en/getting-started/example-datasets/uk-price-paid
Залито как в описании по ссылке (создание и импорт - длинные запросы, не дублирую здесь)
Сложность - качалось и заливалось час, на очень быстром интернете
Поделал запросы в духе _select * from uk_price_paid_ Оценил время выполнения

38770503 rows in set. Elapsed: 2.063 sec. Processed 38.77 million rows, 1.71 GB (18.79 million rows/s., 829.87 MB/s.)
Peak memory usage: 47.38 MiB.

### **Задание с двумя звездочками** ###

```
version: '3.9'
services:
  clickhouse:
    image: clickhouse/clickhouse-server
    container_name: clickhouse1
    volumes:
        - ${PWD}/ch_data:/var/lib/clickhouse/
        - ${PWD}/ch_logs:/var/log/clickhouse-server/
        - ${PWD}/cluster_conf/config.xml:/etc/clickhouse-server/config.xml
    ports:
        - '8124:8123'
        - '9001:9000'
  clickhouse2:
    image: clickhouse/clickhouse-server
    container_name: clickhouse2
    volumes:
        - ${PWD}/cluster_conf/config.xml:/etc/clickhouse-server/config.xml
  clickhouse3:
    image: clickhouse/clickhouse-server
    container_name: clickhouse3
    volumes:
        - ${PWD}/cluster_conf/config.xml:/etc/clickhouse-server/config.xml
```

_Файл config.xml_

```
<remote_servers>
        <!-- Test only shard config for testing distributed storage -->
        <perftest_3shards_1replicas>
            <shard>
                <replica>
                    <host>clickhouse1</host>
                    <port>9000</port>
                </replica>
            </shard>
            <shard>
                <replica>
                    <host>clickhouse2</host>
                    <port>9000</port>
                </replica>
            </shard>
            <shard>
                <replica>
                    <host>clickhouse3</host>
                    <port>9000</port>
                </replica>
            </shard>
        </perftest_3shards_1replicas>
    </remote_servers>
```

Развернул с 3 шардами и 1 репликацией для каждой как описано в документации.
_https://clickhouse.com/docs/ru/getting-started/tutorial
_
создал новую локальную таблицу на каждом хосте
_CREATE TABLE tutorial.hits_local (...) ENGINE = MergeTree() ..._

создал распределенную таблицу на каждом хосте
_CREATE TABLE tutorial.hits_all AS tutorial.hits_local
ENGINE = Distributed(perftest_3shards_1replicas, tutorial, hits_local, rand());_

выполнил инсерт из табл. из пункта 1 в нужную распределенную таблицу
_INSERT INTO tutorial.hits_all SELECT * FROM tutorial.hits_v1;_

Файл конфигов и compose прилагаю.

Сравнил время выполнения с выполением из п.1 (по _select * from hits_all_)
Не ощутил ожидаемого прироста в 3 раза (вероятно т.к. я запускаю их 3 в докере на 1 моем ПК, общая вычислительная мощность не изменилась)
