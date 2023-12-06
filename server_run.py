#api - API(Apliction programing Interface)
#набор правил для взаимодействия программ между собой
from flask import Flask,jsonify,request
from main import *

#http://23.65.234.344
#http://adress:port/(действие)

app = Flask(__name__)

@app.route("/get_items/",methods = ['GET'])
def get_items():
    items = get_item()
    return jsonify({'data':items})

@app.route("/",methods = ['GET'])
def main():
    return '<h1>asd</h1>'
@app.route("/create_item/",methods = ['POST'])
def create_item_rq():
    data = request.get_json()
    item = ItemPydantic(
        name = data.get('name','no name'),
        description = data.get('desc','nodesc'),
        price = data.get('price',0))
    create_item(item)
    return jsonify({'message':'created sucessfully'})
    

@app.route("/retrieve_item/<int:item_id>/",methods = ['GET'])
def get_one_item(item_id):
    item = retrieve(item_id)
    if not item:
        return jsonify({'message':'not found'})
    return jsonify({'data':item})

@app.route("/update_items/<int:item_id>/",methods = ['PUT'])
def update_items(item_id):
    try:
        data = request.get_json()
        update_item(item_id,data)
        return f'Успешно,поле с id = {item_id} изменилось на {data}'
    except:
        return 'Ошибка, неверные входные данные'
    

@app.route("/delete_items/<int:item_id>/",methods = ['DELETE'])
def delete_items(item_id):
    try:
        delete_item(item_id)
        return f'Успешно удалено поле с id = {item_id}'
    except:
        return 'Ошибка' 

app.run(host='localhost',port=8000)