# Часть 1
1. Посмотрел лекцию по etcd
2. Покопался с докер компоуз файлом, развернул etcd его помощь кластер из 3х машин, (рабочий файл compose прилагаю, лежит рядом)
3. Выполнил команды по вставке, получению значений: etcdctl get foo, etcd put foo2 bar2 и т.д.
4. etcdctl --write-out=table endpoint status - посмотрел статусы в 3х контейнерах, увидел кто лидер.
<img width="1433" alt="image" src="https://github.com/Rutkovski/NoSql/assets/64417045/52bc7c0c-80bf-43d0-82eb-d7f73a1fd014">
5. Выключил контейнер лидера  docker stop etcd3, посмотрел что появился новый лидер.
<img width="1432" alt="image" src="https://github.com/Rutkovski/NoSql/assets/64417045/eacf979e-7988-42ce-babb-1d8ff4c8f18a">
6. Включил лидера назад через , посмотрел что он рабоатает и в кластере  docker run etcd3 

# Часть 2 

1. Развернул кластер consul как в лекции с помощью compose файла
2. Как и в лекции поронял то один то другой сервера, запуская и останавливая контейнеры.
3. Увидел что лидер переизбирается.

<img width="1419" alt="image" src="https://github.com/Rutkovski/NoSql/assets/64417045/8d715e7a-1d43-4b35-981e-658ed4bd31dd">
<img width="1409" alt="image" src="https://github.com/Rutkovski/NoSql/assets/64417045/07c54de3-4916-4c56-856a-40b5960dd9c7">



