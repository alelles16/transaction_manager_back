from app.infrastructure.database.models import Base
from app.infrastructure.database.session import engine


def init_db():
    print("Creating tables in the database...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully.")
