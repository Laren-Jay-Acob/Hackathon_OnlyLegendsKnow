from flask import Flask, request
from sqlalchemy import create_engine, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, scoped_session, sessionmaker

app = Flask(__name__)

class Base(DeclarativeBase):
    pass

engine = create_engine("sqlite:///andy.db", future=True, echo=False)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
db = scoped_session(SessionLocal)

class Points(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    points_number: Mapped[int] = mapped_column(Integer, nullable=False)

def run_app():
    app.config["SECRET_KEY"] = "123456789"

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        # db.remove()
        pass

    return app

@app.route("/boss/defeat", methods=['POST'])
def defeat_boss():
    data: dict = request.get_json()

    number = data.get("pts")

    


    

if __name__ == '__main__':
    app = run_app()

    app.run(debug=True)