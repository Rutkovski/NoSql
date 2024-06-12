1) Установил MongoDB c помощь docker compose на ВМ c ubuntu, доступна для проверки по адресу 95.174.93.240:27017, установил на локальный MacOS mongosh и compass
2) Импортировал базы с gitHub как в уроке, поделал вслед за преподавателем CRUD, и как в файле для практики
3) Задание со звездочкой*
а) Нашел по одной из ссылок к лекции БД samples trades с 1 000 000 документов и импортировал ее (искал что-бы протестировать скорость индекса большой объем)
б) Нашел и переделал функцию для замены значений в поле price случайными числами: db.trades.updateMany( { rand: { $exists: false } }, [{ $set: { price: { $function: { body: function () {return Math.round((Math.random()*100),0);}, args: [], lang: "js" } } } }] ) 
в) Добавил простой индекс через compass по полю price

Результат выполнения без индекса по полю "price" без индекса - 71ms
{
 "stage": "COLLSCAN",
 "filter": {
  "price": {
   "$eq": 100
  }
 },
 "nReturned": 5067,
 "executionTimeMillisEstimate": 71,
 "works": 1000004,
 "advanced": 5067,
 "needTime": 994936,
 "needYield": 0,
 "saveState": 1000,
 "restoreState": 1000,
 "isEOF": 1,
 "direction": "forward",
 "docsExamined": 1000003
}
![image](https://github.com/Rutkovski/NoSql/assets/64417045/8c234ce5-79de-46b8-81db-80028427370d)

Результат выполнения с индексом - 1ms
{
 "stage": "IXSCAN",
 "nReturned": 5067,
 "executionTimeMillisEstimate": 0,
 "works": 5068,
 "advanced": 5067,
 "needTime": 0,
 "needYield": 0,
 "saveState": 5,
 "restoreState": 5,
 "isEOF": 1,
 "keyPattern": {
  "price": -1
 },
 "indexName": "price_-1",
 "isMultiKey": false,
 "multiKeyPaths": {
  "price": []
 },
 "isUnique": false,
 "isSparse": false,
 "isPartial": false,
 "indexVersion": 2,
 "direction": "forward",
 "indexBounds": {
  "price": [
   "[100, 100]"
  ]
 },
 "keysExamined": 5067,
 "seeks": 1,
 "dupsTested": 0,
 "dupsDropped": 0
}
{
 "stage": "FETCH",
 "nReturned": 5067,
 "executionTimeMillisEstimate": 1,
 "works": 5068,
 "advanced": 5067,
 "needTime": 0,
 "needYield": 0,
 "saveState": 5,
 "restoreState": 5,
 "isEOF": 1,
 "docsExamined": 5067,
 "alreadyHasObj": 0
}

![image](https://github.com/Rutkovski/NoSql/assets/64417045/915b3c71-b44e-46d2-b837-ff2a6e92692e)


