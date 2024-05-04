1) Развернул кластер с помощью docker compose на локальной машине
2) Связал ноды в кластер, сделал ребалансировку, добавил тестовые данные 
3) Проверил выполнение запросов к БД со страницы https://docs.couchbase.com/cloud/get-started/run-first-queries.html
4) Добавил индекс к этому запросу, оценил изменение времени выполнения с 300 до 30 ms (CREATE INDEX adv_destinationairport_type ON `travel-sample`(`destinationairport`) WHERE `type` = 'route')
5) Уронил 1 инстанс, запросы к БД из UI c других инстансов на какое-то время перестали выполняться, пока база не преобрела статус failover
<img width="1091" alt="image" src="https://github.com/Rutkovski/NoSql/assets/64417045/009b5a11-b29d-4809-9e49-749fe7049891">
<img width="1336" alt="image" src="https://github.com/Rutkovski/NoSql/assets/64417045/d6e6ea5e-64d2-4b7f-89eb-1f6af6d39f27">
<img width="1336" alt="image" src="https://github.com/Rutkovski/NoSql/assets/64417045/1cf00c34-f4f4-4644-a668-b744cc3ee83b">
6) Убрал ноду из кластера, перебалансировал, удалил ее данные дисков
7) Проверил скорость выполнения запроса на чтение из БД, не изменилась значительно
8) Поднял ноду заново, добавил в кластер, перебалансировал.


Сложности в процессе с которыми столкнулся: на ВМ не было достаточно ресурсов, поэтому пришлось перенести все на локальный ПК с докером.
