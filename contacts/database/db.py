from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# docker run --name db-postgres -p 5432:5432 -e POSTGRES_USER=eles -e POSTGRES_PASSWORD=567234 -e POSTGRES_DB=fastapi_db -d postgres
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://eles:567234@localhost:5432/fastapi_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
