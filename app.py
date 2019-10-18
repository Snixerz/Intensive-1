from flask import  Flask, request, url_for, render_template, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
db = client.intensive1
items = db.items

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('intensive1.html')

@app.route('/test')
def test():
    return render_template('intensive1-backpage.html', item = items.find())

@app.route('/delete', methods=['POST'])
def delete():
    db.items.remove({"_id": ObjectId(request.form.get('item'))})
    return redirect(url_for('home_page'))

@app.route('/add_item', methods=['POST'])
def add_item():
    item = request.form.get('item')
    print("This is what we are adding:", item)
    cart_item = {
        'item': item
    }
    items.insert_one(cart_item)
    return redirect(url_for('home_page'))

@app.route('/edit', methods=['POST'])
def edit_item():
    item = items.find_one({'_id':ObjectId(request.form.get('item'))})
    amount = request.form.get('amount')
    cart_item = {
        'item': amount
    }
    items.update_one({"_id": ObjectId(request.form.get('item'))},
                                    {'$set': cart_item})

    return redirect(url_for('test'))

if __name__ == '__main__':
    app.run(debug=True)
