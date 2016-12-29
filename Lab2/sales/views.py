from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import EditSale
from .forms import AddSale

# Create your views here.
from django.shortcuts import render
from .mydatabase import Database


mydb = Database()

def sales_editor(request):
    shops = mydb.getTable("shops")
    products = mydb.getTable("products")

    sales = mydb.getTable("sales")
    editSale = EditSale()
    addSale = AddSale()
    sales_stats = mydb.getSalesStatistics()
    shop_sales = mydb.getTotalShopSales()
    return render(request, 'sales/index.html', {
        'response': {
            'shops': shops,
            'products': products,
            'sales': sales,
            'editSale': editSale,
            'addSale': addSale,
            'sales_stats': sales_stats,
            'shop_sales': shop_sales
        }
    })

def delete(request):
    if request.method == 'POST':
        mydb.deleteFromTableByID("sales", request.POST["sale_id"])
        return HttpResponseRedirect('/')

def update(request):
    if request.method == 'POST':
        mydb.updateSales(request.POST)
        return HttpResponseRedirect('/')

def insert(request):
    if request.method == 'POST':
        form = AddSale(request.POST)
        print form.is_valid()
        if form.is_valid():
            mydb.insertSales(request.POST)
        return HttpResponseRedirect('/')

def salesfilter(request):
    shops = mydb.getTable("shops")
    products = mydb.getTable("products")
    sales = mydb.filter(request.POST["name"])
    return render(request, 'sales/index.html', {'response': {'shops': shops, 'products': products, 'sales': sales}})

def loadxml(request):
    mydb.importFromXML("data.xml")
    return HttpResponseRedirect('/')

