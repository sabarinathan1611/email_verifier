from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from email_verifier import verify_email
from pymongo import MongoClient
from datetime import datetime
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv(verbose=True)

app = FastAPI()

# MongoDB connection with secure defaults
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
print(f"MongoDB URL: {MONGODB_URL}")

try:
    client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
    # Test the connection
    client.admin.command('ping')
    print("MongoDB connection successful")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    raise

db = client.email_verifier
collection = db.verifications

class EmailRequest(BaseModel):
    email: EmailStr

class EmailVerificationResult(BaseModel):
    email: str
    is_valid: bool
    verified_at: datetime
    id: Optional[str] = None

@app.post("/")
async def verify_email_endpoint(data: EmailRequest):
    try:
        email = data.email
        result = verify_email(email)
        
        # Create verification record
        verification_record = {
            "email": email,
            "is_valid": result,
            "verified_at": datetime.utcnow()
        }
        
        # Check if email already exists and update, or insert new record
        existing_record = collection.find_one_and_update(
            {"email": email},
            {"$set": verification_record},
            upsert=True,
            return_document=True
        )
        
        verification_record["_id"] = str(existing_record["_id"])
        
        return {
            "email": email,
            "is_valid": result,
            "verified_at": verification_record["verified_at"],
            "id": str(existing_record["_id"]),
            "updated": existing_record.get("_id") is not None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/verifications")
async def get_verifications(limit: int = 10):
    """Get recent email verifications"""
    try:
        verifications = list(collection.find().sort("verified_at", -1).limit(limit))
        for v in verifications:
            v["_id"] = str(v["_id"])
        return verifications
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching verifications: {str(e)}")

@app.get("/verifications/{email}")
async def get_verification_by_email(email: str):
    """Get verification history for a specific email"""
    try:
        verifications = list(collection.find({"email": email}).sort("verified_at", -1))
        for v in verifications:
            v["_id"] = str(v["_id"])
        return verifications
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching verification: {str(e)}")