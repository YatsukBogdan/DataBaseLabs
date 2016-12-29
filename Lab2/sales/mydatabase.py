from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.code import Code

import sys

import xml.etree.ElementTree as ET

class Database:
    def __init__(self):
        self.db = MongoClient('localhost', 27017).sales

    def importFromXML(self, filename):
        tree = ET.parse("sales/static/xml/" + filename)
        root = tree.getroot()

        self.db.shops.delete_many({})
        self.db.products.delete_many({})
        self.db.sales.delete_many({})

        for child in root:
            if child.tag == "shops":
                for shop in child:
                    for child_prods in shop:
                        products = []
                        for product in child_prods:
                            products.append({
                                'name': product.attrib['name'],
                                'wholesale_price': product.attrib['wholesale_price'],
                                'retail_price': product.attrib['retail_price']
                            })
                        self.db.shops.insert_one({
                            'name': shop.attrib["name"],
                            'owner': shop.attrib["owner"],
                            'products': products
                        })
            if child.tag == "products":
                for product in child:
                    self.db.products.insert_one({
                        'name': product.attrib['name'],
                        'wholesale_price': product.attrib['wholesale_price'],
                        'retail_price': product.attrib['retail_price']
                    })

    def getTable(self, name):
        return list(self.db[name].find({}))

    def deleteFromTableByID(self, table, id):
        self.db[table].remove(
            {'_id': ObjectId(id)}
        )
        return list(self.db[table].find())

    def updateSales(self, request):
        product = self.getProduct(request["editProduct"])
        self.db.sales.update_one({
            '_id': ObjectId(request["editId"])
        }, {
            '$set': {
                'shop': self.getShop(request["editShop"]),
                'product': product,
                'date': request["editDate"],
                'quantity': request["editQuantity"],
                'price': int(request["editQuantity"]) * int(product["retail_price"])
            }
        }, upsert=False)

    def insertSales(self, request):
        product = self.getProduct(request["addProduct"])
        self.db.sales.insert_one({
           'shop': self.getShop(request["addShop"]),
           'product': self.getProduct(request["addProduct"]),
           'date': request["addDate"],
           'quantity': request["addQuantity"],
           'price': int(request["addQuantity"]) * int(product["retail_price"])
        })

    def getProductsName(self):
        return [(str(product['_id']), product['name']) for product in list(self.db.products.find())]

    def getProduct(self, id):
        return list(self.db.products.find({'_id': ObjectId(id)}))[0]

    def getShopsName(self):
        return [(str(shop['_id']), shop['name']) for shop in list(self.db.shops.find())]

    def getShop(self, id):
        return list(self.db.shops.find({'_id': ObjectId(id)}))[0]
   
    def getProducts(self):
        return [(str(product['_id']), product['name']) for product in list(self.db.products.find())]

    def getTotalShopSales(self):
        map = Code('function() { emit(this.shop.name, this.quantity * this.product.retail_price); }')

        reduce = Code('function(key, values) { return Array.sum(values); }')

        return list(self.db.sales.map_reduce(map, reduce, 'result').find())
    
    def getSalesStatistics(self):
        pipeline = [{
            "$group": {
                "_id": "$shop.name",
                "maxPrice": {"$max": "$price"},
                "minPrice": {"$min": "$price"},
            }
        }]
        return list(self.db.sales.aggregate(pipeline))
