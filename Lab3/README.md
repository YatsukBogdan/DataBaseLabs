# Neo4j(Python)

```
def get_common_hobbies(first_id, second_id):
    return session.run("MATCH (p1:Person) WHERE id(p1) = " + str(first_id) + 
                       " MATCH (p2:Person) WHERE id(p2) = " + str(second_id) + 
                       " MATCH (h:Hobby) WHERE (p1)-[:LIKES]->(h) AND (p2)-[:LIKES]->(h)" +
                       " return count(h), collect(h.name)")
                       
def get_people_with_no_hobbies():
    return session.run("MATCH (p:Person) WHERE NOT (p)-[:LIKES]->()" +
                       " return collect(id(p))" ) 
```
  

# MongoDB  (Python)
```
def url_visits_count():
    result = db.Urls.aggregate([
            { "$group": { "_id" : "$date",
                          "urls" :{ "$push": "$url"} }
            },
            {"$unwind": "$urls" } ,
            { "$group": { "_id" : "$_id",
                          "urls" : { "$addToSet": "$urls"} }
            },
            {"$project":{"url_count": {"$size": "$urls"} }}
        ])
    return result
 
def ips_list():
    urls = db.Urls.aggregate([
        {"$group": {"_id": "$url"}
        }
    ])
    result = db.Urls.aggregate([
        {"$group": {"_id": "$ip",
                    "urls": {"$push": "$url"}}
        },
        {"$unwind": "$urls"},
        {"$group": {"_id": "$_id",
                    "urls": {"$addToSet": "$urls"} }
        },
        { "$project": {"number_of_visits_urls": {"$size": "$urls"} } },
        { "$match" : { "number_of_visits_urls" : len(list(urls)) } },
        { "$group": {"_id": "$_id" } }
    ])
    return result
    
 
def insert_doc():
    collection = db.Urls
    doc = {"ip" : choice(ips), 
           "url" : choice(urls), 
           "date" : datetime.strptime(str(getDate()), '%Y-%m-%d')}
    collection.insert_one(doc)

```
