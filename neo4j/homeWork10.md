Домашка:

1) Взять 4-5 популярных туроператора.
2) Каждый туроператор должен быть представлен в виде ноды neo4j
3) Взять 10-15 направлений, в которые данные операторы предосавляют путевки.
4) Представить направления в виде связки нод: страна - конкретное место
5) Взять ближайшие к туриситческим локацимя города, в которых есть аэропорты или вокзалы и представить их в виде нод
6) Представить маршруты между городми в виде связей. Каждый маршрут должен быть охарактеризован видом транспорта, который позволяет переместиться между точками.
7) Написать запрос, который бы выводил направление (со всеми промежуточными точками), который можно осуществить только наземным транспортом.
8) Составить план запроса из пункта 7.
9) Добавить индексы для оптимизации запроса
10) Еще раз посмотреть план запроса и убедиться, что индексы позволили оптимизировать запрос


Пункты 1 и 2
Взять 4-5 популярных туроператора.
Каждый туроператор должен быть представлен в виде ноды neo4j

Pegas Touristik.
AnexTour.
FUN&SUN (бывший TUI)
Biblio Globus.
Coral Travel.

    1) 10 направлений в которые эти операторы предоставляют путевки. Связки нод страна - конкретное место.
Пукты 3 и 4
Взять 10-15 направлений, в которые данные операторы предосавляют путевки.
Представить направления в виде связки нод: страна - конкретное место

Турция - Аланья - Газипаша(Аэропорт)
Турция - Кемер - Анталия (Аэропорт)
Турция - Сиде - Анталия (Аэропорт)
Египет - Хургада - Хургада (аэропорт)
Египет - Шарм-эль-Шейх - Шарм -эль-Шейх (Аэропорт)
Египет - Каир - Каир (аэропорт)
Россия - Сочи - Адлер (Аэропорт, Вокзал)
Россия - Санкт-Петербург - Санкт-Петербург (Аэропорт, Вокзал)
Россия - Калининград - Калининград (Аэропорт)
Россия - Казань - Казань (Аэропорт, Вокзал)

 
Пункты 1-6 в виде запросов.   
match (n) detach delete n
match (n) -[r]- () return n, r

create (:Country {name:"Russian"}), (:Country {name:"Turkey"}),(:Country {name:"Egypt"})
create (:TourAgency {name:"Pegas Touristik"}), (:TourAgency {name:"AnexTour"}), (:TourAgency {name:"FUN&SUN"}),(:TourAgency {name:"Coral Travel"})

match (t:TourAgency), (c:Country )
create (t) -[:DIRECTION]-> (c)

match (Turkey:Country {name:"Turkey"}), (Russian:Country {name:"Russian"}),(Egypt:Country {name:"Egypt",  type:'only_airport'})
merge (Turkey) -[:PLACE]->(:Resort{name:'Alaniya'}) <-[:TRANSPORT_POINT]-(:TransportCity{name:'Gazipasha', type:'only_airport'}) 
merge (Turkey) -[:PLACE]->(:Resort{name:'Side'}) <-[:TRANSPORT_POINT]-(r:TransportCity{name:'Antaliya' , type:'only_airport'}) 
merge (Turkey) -[:PLACE]->(:Resort{name:'Kemer'}) <-[:TRANSPORT_POINT]-(r) 
merge (Russian) -[:PLACE]->(:Resort{name:'Razan'})<-[:TRANSPORT_POINT]-(:TransportCity{name:'Razan',  type:'airport_or_train'}) 
merge (Russian) -[:PLACE]->(:Resort{name:'SPB'})<-[:TRANSPORT_POINT]-(:TransportCity{name:'SPB', type:'airport_or_train'}) 
merge (Russian) -[:PLACE]->(:Resort{name: 'Kaliningrad'})<-[:TRANSPORT_POINT]-(:TransportCity{name:'Kaliningrad', type:'only_airport'}) 
merge (Russian) -[:PLACE]->(:Resort{name: 'Sochi'})<-[:TRANSPORT_POINT]-(:TransportCity{name:'Sochi', type:'airport_or_train'}) 
merge (Egypt) -[:PLACE]->(:Resort{name:'Hurgada'})<-[:TRANSPORT_POINT]-(:TransportCity{name:'Hurgada', type:'only_airport'}) 
merge (Egypt) -[:PLACE]->(:Resort{name:'Kair'})<-[:TRANSPORT_POINT]-(:TransportCity{name:'Kair', type:'only_airport'}) 
merge (Egypt) -[:PLACE]->(:Resort{name: 'Sharm-al-Sheich'})<-[:TRANSPORT_POINT]-(:TransportCity{name:'Sharm-al-Sheich', type:'only_airport'}) 

MATCH (t1:TransportCity), (t2:TransportCity{type: 'only_airport'})
WHERE t1 <> t2
CREATE (t1)-[:TRANSPORT {type: 'airplain'}]->(t2)

MATCH (t1:TransportCity{type:'airport_or_train'}), (t2:TransportCity{type:'airport_or_train'})
WHERE t1 <> t2
CREATE (t1)-[:TRANSPORT {type: 'train'}]->(t2)


Пункт 7 - составлен некорректно в лексическом и смысловом плане, нужно исправление формулировки и помощщь в том, как это реализовать, на созданной выше структуре. 
7) Написать запрос, который бы выводил направление (со всеми промежуточными точками), который можно осуществить только наземным транспортом.
Который(мужской род) это что? Запрос который можно осуществить только наземным транспоротом? Направление? - оба варианта не подходят по смыслу.
Может быть имелся ввиду маршрут? Тогда причем тут направление? Маршрут в рамках всех направлений? В рамках одного направления? 

Задал вопрос в группе telegram но не получил ответа. Методист порекомендовал задать вопрос здесь.

Если никто не знает что имелось ввиду в задании - зачтите как выполненное, и пойдем дальше.
