from django import forms
from .mydatabase import Database
import datetime

db = Database()

class DeleteForm(forms.Form):
    transfer_id = forms.CharField(max_length=100)


class AddSale(forms.Form):
        addShop = forms.ChoiceField(label='Shop', required=True, choices=(db.getShopsName()))
        addProduct = forms.ChoiceField(label="Product", required=True, choices=(db.getProductsName()))
        addQuantity = forms.DecimalField(label="Quantity", required=True)
        addDate = forms.DateField(initial=datetime.date.today, label="Date", required=True)

class EditSale(forms.Form):
        editId = forms.CharField(label='ID:', max_length=100)

        editShop = forms.ChoiceField(label='Shop', required=True, choices=(db.getShopsName()))
        editProduct = forms.ChoiceField(label="Product", required=True, choices=(db.getProductsName()))
        editQuantity = forms.DecimalField(label="Quantity", required=True)
        editDate = forms.DateField(label="Date", required=True)

