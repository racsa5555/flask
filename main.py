from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_sqlalchemy import sqlalchemy_to_pydantic


DATABASE_URL = "postgresql://ascar:1@localhost/product_items"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer,primary_key = True,autoincrement = True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)

Base.metadata.create_all(bind=engine)

ItemPydantic = sqlalchemy_to_pydantic(Item,exclude=["id"])

db_item = ItemPydantic(name = 'ite4',description = 'desqwsc',price = 13000)

def create_item(db_item:ItemPydantic):
    with SessionLocal() as db:
        db_item = Item(**db_item.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
    return db_item
def get_item():
    result = []
    with SessionLocal() as db:
        items = db.query(Item).all()
        for item in items:
            result.append({'id':item.id,
                            'name': item.name,
                           'description':item.description,
                           'price':item.price})
    return result



def retrieve(id):
    result = []
    with SessionLocal() as db:
        items = db.query(Item).all()
        for item in items:
            if item.id == id:
                result.append({'id': item.id,
                            'name': item.name,
                           'description':item.description,
                           'price':item.price})
                return result
        return None


#retrieve - выдача данных по айди

def update_item(item_id,item):
    with SessionLocal() as db:
        db_item = db.query(Item).filter(Item.id ==item_id).first()
        for field,value in item.items():
            setattr(db_item,field,value)
        db.commit()
        db.refresh(db_item)
        return db_item
print(get_item())
# print(update_item(0,{'name':'danil','description':'not have','price':441}))

#update

def delete_item(item_id):
    with SessionLocal() as db:
        db_item = db.query(Item).filter(Item.id ==item_id).first()
        db.delete(db_item)
        db.commit()
        return db_item

# print(delete_item(3))
print(get_item())



