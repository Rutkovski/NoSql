1) Развернул шардированный класстер на основе примера в лекции но видоизменив docker compose убрав порты у всех серверов кроме mongos, негоже им смотреть наружу, и не меняя дефолтных портов
2) Итого 3 конфиг сервера, 2 шарды по 3 сервера в каждой и 2 mongos
3) Сделал два сервера mongos для обеспечения надежности
4) Cложность: Столкнулся с тем что не могу достучаться до машин, долго искал инфу пока понял, что у конфиг серверов свой порт по дефолту и у шард свой
5) Поронял разные инстсы, если уронить 2 конфиг сервера или 2 сервера в шардае - то 1 серверу не хватает голоса чтобы стать primary и кластер рушится. Если по 1 машине ронять - все работает.
6) Ключ шардирования задал хэшированный _id
7) Развернул 1 инстанс в контейнере для авторизаци проверки и настройки ролей (как в лекции на 1 инстансе, т.к. для кластера шардированного применяется подход с файлами ключей и настройка, судя по всему, будет очень долгой)
8) Столкнулся со сложностью - если разворачивать в контейнерах, отсутствует файл /etc/mongo.config (поэтому задал требование аутентификации через compose файл)
   Насоздавал различных пользователей с различными ролями.


Пример docker-compose который использовал для развертывания шардированного кластера:

[Uploading---
version: "3.8"
services:
  m_configsvr1:
    image: mongo:7
    container_name: m_configsvr1
    command: --configsvr --replSet configReplSet --bind_ip_all  
    volumes:
      - ./m_configsvr1_db:/data/db
      - ./m_configsvr1_config:/etc/mongod.conf

  m_configsvr2:
    image: mongo:7
    container_name: m_configsvr2
    command: --configsvr --replSet configReplSet --bind_ip_all  
    volumes:
      - ./m_configsvr2_db:/data/db
      - ./m_configsvr2_config:/etc/mongod.conf

  m_configsvr3:
    image: mongo:7
    container_name: m_configsvr3
    command: --configsvr --replSet configReplSet --bind_ip_all  
    volumes:
      - ./m_configsvr3_db:/data/db
      - ./m_configsvr3_config:/etc/mongod.conf

  m_shard1rs1:
    image: mongo:7
    container_name: m_shard1rs1
    command: --shardsvr --replSet shard1 --bind_ip_all  
    volumes:
      - ./m_shard1rs1_db:/data/db
      - ./m_shard1rs1_config:/etc/mongod.conf

  m_shard1rs2:
    image: mongo:7
    container_name: m_shard1rs2
    command: --shardsvr --replSet shard1 --bind_ip_all  
    volumes:
      - ./m_shard1rs2_db:/data/db
      - ./m_shard1rs2_config:/etc/mongod.conf
  
  m_shard1rs3:
    image: mongo:7
    container_name: m_shard1rs3
    command: --shardsvr --replSet shard1 --bind_ip_all  
    volumes:
      - ./m_shard1rs3_db:/data/db
      - ./m_shard1rs3_config:/etc/mongod.conf

  m_shard2rs1:
    image: mongo:7
    container_name: m_shard2rs1
    command: --shardsvr --replSet shard2 --bind_ip_all  
    volumes:
      - ./m_shard2rs1_db:/data/db
      - ./m_shard2rs1_config:/etc/mongod.conf

  m_shard2rs2:
    image: mongo:7
    container_name: m_shard2rs2
    command: --shardsvr --replSet shard2 --bind_ip_all   
    volumes:
      - ./m_shard2rs2_db:/data/db
      - ./m_shard2rs2_config:/etc/mongod.conf

  m_shard2rs3:
    image: mongo:7
    container_name: m_shard2rs3
    command: --shardsvr --replSet shard2 --bind_ip_all  
    volumes:
      - ./m_shard2rs3_db:/data/db
      - ./m_shard2rs3_config:/etc/mongod.conf

  m_route1:
    image: mongo:7
    container_name: m_route1
    command: mongos --configdb configReplSet/m_configsvr1:27019,m_configsvr2:27019,m_configsvr3:27019 --bind_ip_all 
    volumes:
      - ./m_route1_db:/data/db
      - ./m_route2_config/mongod:/etc/mongod.conf
    ports:
      - 27017:27017

  m_route2:
    image: mongo:7
    container_name: m_route2
    command: mongos --configdb configReplSet/m_configsvr1:27019,m_configsvr2:27019,m_configsvr3:27019 --bind_ip_all
    volumes:
      - ./m_route2_db:/data/db
      - ./m_route2_config/mongod:/etc/mongod.conf
    ports:
      - 27018:27017

 docker-copmose.shard2.yml…]()

 Пример docker-compose который использвал для развертывания mongo с автордизацией:
[Uploading compose.yml…version: '3.9'

services:
  my-mongodb:
    image: mongo
    container_name: mongodb
    tty: true
    stdin_open: true
    ports:
      - 27017:27017
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=admin
    volumes:
      - ./mongo/data:/data/db
    # command: --port 27020 
    networks:
      - mongo_net
networks:
  mongo_net:
    driver: bridge]()

 
Примеров команд не сохранилось, т.к. 
1) Контейнер был перезапущен после отправки дз
2) Система была перезалита.

При этом использовал для развертывания кластера шардированного стандартные команды из приложения - практики - то, что и делали на уроке.
(заменив названия хостов на названия контейнеров из конфигов выше и поставь порты 27019 для конфиг серверов и 27018 для шард серверов (т к они идут по умолчанию)
Привожу здесь копипасту из практики, по факту хосты порты были изменены на свои.
rs.initiate({
  "_id": "config-replica-set",
  members : [
    {"_id": 0, "host": "mongo-configsvr-1:40001"},
    {"_id": 1, "host": "mongo-configsvr-2:40002"},
    {"_id": 2, "host": "mongo-configsvr-3:40003" }
] });


rs.initiate({
  "_id" : "shard-replica-set-1",
  members : [
    {"_id" : 0, host : "mongo-shard-1-rs-1:40011"},
    {"_id" : 1, host : "mongo-shard-1-rs-2:40012"},
    {"_id" : 2, host : "mongo-shard-1-rs-3:40013" }
] });

rs.initiate({
  "_id" : "shard-replica-set-2",
  members : [
    {"_id" : 0, host : "mongo-shard-2-rs-1:40021"},
    {"_id" : 1, host : "mongo-shard-2-rs-2:40022"},
    {"_id" : 2, host : "mongo-shard-2-rs-3:40023" }
] });


docker exec -it mongos-shard bash 
> sh.addShard("shard-replica-set-1/mongo-shard-1-rs-1:40011,mongo-shard-1-
rs-2:40012,mongo-shard-1-rs-3:40013")
> sh.addShard("shard-replica-set-2/mongo-shard-2-rs-1:40021,mongo-shard-2-
rs-2:40022,mongo-shard-2-rs-3:40023")
> sh.status()


Далее залил данные из коллекции с гитхаба ссылка на которую была в первой лекции по монго, 

Изменил размер чанка 
use config
db.settings.updateOne(
  { _id: "chunksize" },
  { $set: { _id: "chunksize", value: 1 } },
  { upsert: true }
)

включил шардинг на коллекцию, выбрав ключом хэшированный _id
что-то в духе:
sh.enableSharding("billing")
db.payments.ensureIndex( { "_id": "hashed" } )
sh.shardCollection( "billing.payments", { "_id": "hashed" } )

Потом поронял по очереди контейнеры командой docker stop имя_контейнера и посмотрел как будет выполняться досуп к данным из compass

Касаемо авторизаций: 
1) Развернул с помощь docker сompose указанного выше, наполнил данными
2) Посоздавал пользователей командой подключившись к бд, что-то в духе как и в практике:
3) use моя_база
4) db.createUser({
        user: "readWriteUser",
        pwd: "strictReadWritePassword",
        roles: [
                { role: "readWrite", db: "test" }
] })
Проверил  через compas созданный пользователь видит только свою БД




