from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient
from backend.app.core.config import settings

# PostgreSQL
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# MongoDB
mongo_client: AsyncIOMotorClient = None

async def connect_to_mongo():
    global mongo_client
    mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
    print("Connected to MongoDB!")

async def close_mongo_connection():
    global mongo_client
    if mongo_client:
        mongo_client.close()
        print("MongoDB connection closed.")

def get_mongo_db():
    return mongo_client.get_database()
