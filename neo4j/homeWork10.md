
Домашка:
    1) 4 туроператора выбрать и сделать нодой
Pegas Touristik.
AnexTour.
FUN&SUN (бывший TUI)
Biblio Globus.
Coral Travel.

    1) 10 направлений в которые эти операторы предоставляют путевки. Связки нод страна - конкретное место.
    
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

    1) Ближайшие к курортам города с аэропортом или вокзалом- ноды.
    2) Сделать маршруты между городами в виде связей. У каждой связи есть свойство - вид транспорта, который позволяет перемещаться между точками
    3) Написать запрос, который бы выводил направление (со всеми промежуточными точками), который можно осуществить только наземным транспортом.
    4) Составить план запроса из пункта 7.
    5) Добавить индексы для оптимизации запроса
    6) Еще раз посмотреть план запроса и убедиться, что индексыпозволили оптимизировать запрос
    7) 
    

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

match(r:TransportCity{name:'Gazipasha'})
create (r)-[airplain]->(:TransportCity)
create (TransportCity)-[airplain]->(r)

MATCH (t1:TransportCity), (t2:TransportCity{type: 'only_airport'})
WHERE t1 <> t2
CREATE (t1)-[:TRANSPORT {type: 'airplain'}]->(t2)

MATCH (t1:TransportCity{type:'airport_or_train'}), (t2:TransportCity{type:'airport_or_train'})
WHERE t1 <> t2
CREATE (t1)-[:TRANSPORT {type: 'train'}]->(t2)