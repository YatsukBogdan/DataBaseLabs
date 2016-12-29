### Кожокарь Олександр КП-42 Лаб.2 БД
#### Мета
Метою роботи є здобуття практичних навичок створення та обробки бази даних типу NoSQL на прикладі СУБД MongoDB.Основою розробки є програмні засоби, розроблені у лабораторній роботі No2 частини 1(ЛРNo2 - Ч1) дисципліни «Бази даних».

#### Завдання роботи полягає у наступному:
1. Розробити схему бази даних на основі предметної галузі з ЛРNo2-Ч1у спосіб, що застосовується в СУБД MongoDB.  
2. Розробити модуль роботи з базою даних на основі пакету PyMongo.  
3. Реалізувати дві операції на вибір із використанням паралельної обробки даних Map/Reduce.
4. Реалізувати обчисленнята виведення результату складного агрегативного запиту  до  бази  даних з  використанням функції aggregate() сервера MongoDB.

#### MAP/REDUCE
```
def getTotalClubRevenue(self):
        map = Code("""
                    function () {
                        emit(this.from.name, +this.price);
                    }
                   """)
        
        reduce = Code("""
                        function(key, values) {
                            return Array.sum(values);
                    }
                    """)
        
        return list(self.db.Transfer.map_reduce(map, reduce, 'result').find())
```

#### AGGREGATE
```
def getSalesStatistics(self):
        pipeline = [
          {
              "$group" : {
              "_id" : { "$concat" : ["$fp.first_name"," ","$fp.last_name"] }, 
              "maxPrice" : { "$max" : "$price"},
              "minPrice" : { "$min" : "$price" },
              }
          }
        ]
        return list(self.db.Transfer.aggregate(pipeline))
```

