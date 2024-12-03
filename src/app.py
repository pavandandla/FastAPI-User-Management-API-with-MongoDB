from fastapi import FastAPI
from routes.user_bp import user_bp
from config.database import client, db  # Import client and db to ensure MongoDB connection
from models.all_models import UserModel

app = FastAPI()

# Register the user routes
app.include_router(user_bp)

@app.on_event("startup")
async def startup_event():
    # Ensure the collection exists
    collection_name = UserModel.collection  # Referencing the collection name
    collections = await db.list_collection_names()
    
    if collection_name not in collections:
        # Create an empty document to initialize the collection
        await db[collection_name].insert_one({})
        await db[collection_name].delete_many({})  # Clean up after initialization
    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
