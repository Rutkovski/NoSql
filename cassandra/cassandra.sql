CREATE KEYSPACE IF NOT EXISTS keyspace_test_claster WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 2};
describe cluster;
describe  keyspaces;
CREATE TABLE keyspace_test_claster.races(
race_year int,
race_name text,
cyclist_name text,
rank int,
id timeuuid,
PRIMARY KEY ((race_year, race_name), id)
)
WITH CLUSTERING ORDER BY (id DESC);

CREATE TABLE keyspace_test_claster.books(
book_year int,
book_name text,
author text,
rating float,
PRIMARY KEY (book_year, author, book_name)
)
WITH CLUSTERING ORDER BY (author DESC);

insert into books(book_year, book_name, author, rating) values (1873,'War and piece','Tolstoy',8.2);
select * from books;
select * from races;
-- Не работает, нужно ALLOW FILTERING или вторичный индекс
select * from races where cyclist_name = 'velocity';
-- Не работает, нужно ALLOW FILTERING или вторичный индекс
select * from races where id = 43d97284-217f-11ef-88d5-5a80d7b12606;
-- А так - работает
select * from races where race_name = 'narcotics' and race_year = 1896;
-- ну и с AllowFiletering работает конечно тоже
select * from races where id = 43a89754-217f-11ef-88d5-5a80d7b12606 allow filtering;
-- Вторичный индекс на поле не входящее в primary
create index on races (cyclist_name);
select * from races where cyclist_name = 'directive';
-- На поле входяще в primary
create index on races (race_name);
select * from races where race_name = 'narcotics';
DROP TABLE  keyspace_test_claster.books;
DROP TABLE  keyspace_test_claster.races;

