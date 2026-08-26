import pymongo
from passlib.context import CryptContext

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["pothole_detection"]
users = db["users"]

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

admin_email = "admin@city.gov"
admin_password = "admin123"

hashed_password = pwd_context.hash(admin_password)

# Check if user exists
user = users.find_one({"email": admin_email})

if user:
    users.update_one({"email": admin_email}, {"$set": {"hashed_password": hashed_password}})
    print(f"Updated password for {admin_email}")
else:
    users.insert_one({
        "email": admin_email,
        "hashed_password": hashed_password,
        "role": "authority"
    })
    print(f"Created admin user {admin_email}")

print("Done.")
