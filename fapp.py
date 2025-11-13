from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Integer, String, Boolean, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, scoped_session, sessionmaker

app = Flask(__name__)

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
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    points_number: Mapped[int] = mapped_column(Integer, nullable=False)

def run_app():
    app.config["SECRET_KEY"] = "123456789"

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.remove()

    return app

@app.route("/player/create", methods=['POST'])
def create_player():
    user = Player(points_number=0)

    db.add(user)
    succ, err = commit_sesison()
    if not succ:
        return json_resp(500, False, err)
    
    return json_resp(200, True, f"You have created a player")


@app.route("/boss/defeat", methods=['POST'])
def defeat_boss():
    data: dict = request.get_json()

    number = data.get("pts")

    stmt = select(stmt).where(Player.id == 1)



if __name__ == '__main__':
    app = run_app()

    app.run(debug=True)