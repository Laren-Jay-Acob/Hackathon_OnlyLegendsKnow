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

class Shop(Base):
    __tablename__ = "shop"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    shop_item: Mapped[str] = mapped_column(String(128), nullable=False)
    is_unlocked: Mapped[bool] = mapped_column(Boolean, default=False)

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

@app.route("/boss/defeat", methods=['POST'])
def defeat_boss():
    data: dict = request.get_json()

    number = data.get("pts")

    stmt = select(stmt).where(Player.id == 1)

if __name__ == '__main__':
    app = run_app()
    Base.metadata.create_all(engine)

    app.run(debug=True)