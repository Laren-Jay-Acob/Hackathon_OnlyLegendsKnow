from flask import Flask, request, jsonify
from enum import Enum
from sqlalchemy import create_engine, Integer, String, Boolean, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, scoped_session, sessionmaker

app = Flask(__name__)

class Shops_item(Enum):
    AUTO_CLICK = "auto_clicker"
    CLICK_DMG = "click_dmg"

class Base(DeclarativeBase):
    pass

def commit_sesison():
    try:
        db.commit()
        return True, None
    except Exception as e:
        db.rollback()
        return False, str(e)
    
def json_resp(status: int, ok: bool, msg: str | dict, **kwargs):
    resp = jsonify({
            "status": status,
            "ok": ok,
            "msg": msg,
            **kwargs,
        })
    resp.status_code = status
    return resp

engine = create_engine("sqlite:///andy.db", future=True, echo=False)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
db = scoped_session(SessionLocal)

class Player(Base):
    __tablename__ = "player"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    level: Mapped[int] = mapped_column(Integer, nullable=False)

    def get_data(self):
        return {
            "id": self.id,
            "level": self.level,
        }

class Shop(Base):
    __tablename__ = "shop"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    shop_item: Mapped[str] = mapped_column(String(128), nullable=False)
    item_level: Mapped[int] = mapped_column(Integer, default=0)

    def get_data(self):
        return {
            "id": self.id,
            "shop_item": self.shop_item,
            "item_level": self.item_level,
        }
    
class Coins(Base):
    __tablename__ = "coins"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    amount: Mapped[int] = mapped_column(Integer, default=0)

    def get_data(self):
        return {
            "id": self.id,
            "amount": self.amount,
        }

def run_app():
    app.config["SECRET_KEY"] = "123456789"

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.remove()

    return app

@app.route("/player/create", methods=['GET'])
def create_player():
    user = Player(level=0)

    db.add(user)
    succ, err = commit_sesison()
    if not succ:
        return json_resp(500, False, err)
    
    return json_resp(200, True, f"You have created a player")

@app.route("/shop/create", methods=['GET'])
def create_shop():
    for ishop in Shops_item:
        items = Shop(shop_item=ishop.value)
        db.add(items)

    succ, err = commit_sesison()
    if not succ:
        return json_resp(500, False, err)
    
    return json_resp(200, True, "You have created the shop")

@app.route("/coins/create", methods=['GET'])
def create_coins():
    coins = Coins(amount=0)

    db.add(coins)
    succ, err = commit_sesison()
    if not succ:
        return json_resp(500, False, err)
    
    return json_resp(200, True, f"You have created a coins")
    
@app.route("/player/level_up", methods=['GET'])
def player_level_up():

    player = db.get(Player, 1)

    if not player:
        return json_resp(404, False, "Player not found")
    
    player.level += 1

    succ, err = commit_sesison()
    if not succ:
        return json_resp(500, False, err)
    
    return json_resp(200, True, "You have levelop up")

@app.route("/coins/gain", methods=['PATCH'])
def coins_gain():
    data: dict = request.get_json()

    coins_data = data.get("coins")

    coins = db.get(Coins, 1)

    coins.amount += int(coins_data)

    succ, err = commit_sesison()
    if not succ:
        return json_resp(500, False, err)

    return json_resp(200, True, "You have gained coins")

@app.route("/shop/item_level", methods=['PATCH'])
def shop_level_item():
    data: dict = request.get_json()

    item_id = data.get("id")

    ishop = db.get(Shop, int(item_id))

    ishop.item_level += 1

    succ, err = commit_sesison()
    if not succ:
        return json_resp(500, False, err)
    
    return json_resp(200, False, "You have leveled up")

@app.route("/all/get", methods=['GET'])
def get_all():
    stmt = select(Shop)

    items = db.scalars(stmt).all()
    player = db.get(Player, 1)
    coins = db.get(Coins, 1)

    data = {
        "items": [item.get_data() for item in items],
        "player": player.get_data(),
        "coins": coins.get_data(),
    }

    return json_resp(200, True, data)

if __name__ == '__main__':
    app = run_app()
    Base.metadata.create_all(engine)

    app.run(debug=True)