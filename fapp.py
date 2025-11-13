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
    points_number: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)

    def get_data(self):
        return {
            "id": self.id,
            "points_number": self.points_number,
            "level": self.level,
        }

class Shop(Base):
    __tablename__ = "shop"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    shop_item: Mapped[str] = mapped_column(String(128), nullable=False)
    is_unlocked: Mapped[bool] = mapped_column(Boolean, default=False)
    item_level: Mapped[int] = mapped_column(Integer, default=0)

    def get_data(self):
        return {
            "id": self.id,
            "shop_item": self.shop_item,
            "is_unlocked": self.is_unlocked,
            "item_level": self.item_level,
        }
    
class Coins(Base):
    __tablename__ = "coins"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    amount: Mapped[int] = mapped_column(Integer, default=0)

    def get_data(self):
        return {
            "id": self.id,
            "shop_item": self.amount,
        }

def run_app():
    app.config["SECRET_KEY"] = "123456789"

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.remove()

    return app

@app.route("/player/create", methods=['GET'])
def create_player():
    user = Player(points_number=0, level=0)

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

@app.route("/shop/display", methods=['GET'])
def shop_display():
    stmt = select(Shop)
    shop_items = db.scalars(stmt).all()

    data = []

    for i in shop_items:
        data.append(i.get_data())

    return json_resp(200, True, data)

@app.route("/shop/buy", methods=['PATCH'])
def shop_buy():
    data: dict = request.get_json()

    item_id = data.get("id")

    item_db = db.get(Shop, int(item_id))

    if item_db.is_unlocked != True:
        item_db.is_unlocked = True

    item_db.item_level += 1

    succ, err = commit_sesison()
    if not succ:
        return json_resp(500, False, err)
    
    return json_resp(200, True, f"You have leveled up item No.{item_id}")

@app.route("/boss/defeat", methods=['POST'])
def defeat_boss():
    data: dict = request.get_json()

    number = data.get("pts")

    player = db.get(Player, 1)
    
    if not player:
        return json_resp(404, False, "You did not find a player")
    
    player.points_number += int(number)

    succ, err = commit_sesison()
    if not succ:
        return json_resp(500, False, err)

    return json_resp(200, True, "You have defeated a boss")

@app.route("/shop/unock", methods=['PATCH'])
def shop_unlock():
    item1 = select(Shop).where(Shop.id == 1)
    item2 = select(Shop).where(Shop.id == 2)
    playerstmt = select(Player).where(Player.id == 1)

    ishop1 = db.scalars(item1).first()
    ishop2 = db.scalars(item2).first()
    player = db.scalars(playerstmt).first()

    if not ishop1 or not ishop2:
        return json_resp(204, False, "there is no shop item")
    
    if not player:
        return json_resp(204, False, "There is no player")
    
    if player.points_number >= 100:
        print("You have unlocked item 1")
        ishop1.is_unlocked = True

    if player.points_number >= 1000:
        print("You have unlocked item 1")
        ishop2.is_unlocked = True

    succ, err = commit_sesison()
    if not succ:
        return json_resp(500, False, err)
    
    return json_resp(200, True, "You have unlocked shop")
    
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

@app.route("/coins/gain", methods=['POST'])
def coins_gain():
    data: dict = request.get_json()

    coins = data.get("coins")

    coins = db.get(Coins, 1)

    coins.amount += int(coins)

    return json_resp(200, True, "You have gained coins")

if __name__ == '__main__':
    app = run_app()
    Base.metadata.create_all(engine)

    app.run(debug=True)