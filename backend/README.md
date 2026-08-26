# AI-Based Road Damage & Pothole Detection System - Backend

A complete FastAPI backend system for reporting, verifying, and managing pothole repairs using AI-powered image verification and geographic risk zone detection.

## 🎯 Features

- **User Authentication**: JWT-based authentication with role-based access (user/authority)
- **Pothole Reporting**: Image upload with GPS coordinates and automatic AI verification
- **AI Verification**: Mock CNN-based pothole detection with confidence scoring
- **Risk Zone Detection**: Geographic clustering to identify high-risk areas
- **Repair Management**: Track repair actions and status progression
- **Role-Based Access**: Different permissions for regular users and authorities

## 📋 Requirements

- Python 3.9+
- MongoDB 4.4+
- 2GB RAM minimum
- 500MB free disk space for uploads

## 🚀 Quick Start

### Prerequisites Checked Automatically

✅ The backend now **automatically verifies** all requirements when you run it:
- Python version (3.9+)
- All dependencies installed
- Project structure
- Environment configuration
- Virtual environment status

### Simple Run Command

```powershell
# Navigate to backend directory
cd "c:\Users\Admin\React\ai based road detection s\backend"

# Activate virtual environment
.\venv\Scripts\activate

# Run the server (automatic verification included!)
uvicorn app.main:app --reload
```

**What happens automatically:**
1. ✅ Checks Python 3.9+
2. ✅ Verifies all packages (FastAPI, Motor, JWT, etc.)
3. ✅ Validates project structure
4. ✅ Checks .env configuration
5. ✅ Confirms virtual environment
6. 🚀 Starts server if all checks pass

If anything is missing, you'll see:
- **Detailed error messages** showing what's wrong
- **Step-by-step instructions** on how to fix it
- **Automatic exit** to prevent running with missing dependencies

### First Time Setup (if needed)

If the automatic verification shows missing components:

```powershell
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

## 📚 API Documentation

### Interactive API Docs

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "1234567890",
  "role": "user",
  "password": "password123"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "password123"
}

Response:
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

### Report Endpoints

#### Submit Pothole Report
```http
POST /api/reports
Authorization: Bearer <token>
Content-Type: multipart/form-data

image: <file>
latitude: 34.0522
longitude: -118.2437
description: "Large pothole on Main St"
```

#### Get Reports
```http
GET /api/reports?status=pending&limit=50
Authorization: Bearer <token>
```

#### Update Report Status (Authority Only)
```http
PUT /api/reports/{report_id}/status
Authorization: Bearer <authority_token>
Content-Type: application/json

{
  "status": "verified",
  "notes": "Verified and assigned for repair"
}
```

### Risk Zone Endpoints

#### Get All Risk Zones
```http
GET /api/zones
Authorization: Bearer <token>
```

#### Get High-Risk Zones Only
```http
GET /api/zones/high-risk
Authorization: Bearer <token>
```

#### Recalculate Risk Zones (Authority Only)
```http
POST /api/zones/recalculate
Authorization: Bearer <authority_token>
```

### Repair Action Endpoints

#### Create Repair Action (Authority Only)
```http
POST /api/repairs
Authorization: Bearer <authority_token>
Content-Type: application/json

{
  "zone_id": "507f1f77bcf86cd799439011",
  "assigned_department": "Public Works - District 4",
  "repair_status": "pending"
}
```

#### Update Repair Status (Authority Only)
```http
PUT /api/repairs/{repair_id}
Authorization: Bearer <authority_token>
Content-Type: application/json

{
  "repair_status": "completed"
}
```

## 🗄️ Database Schema

### Collections

- **users**: User accounts with roles
- **pothole_reports**: Submitted pothole reports with images
- **image_verification**: AI verification results
- **risk_zones**: Geographic clusters of potholes
- **repair_actions**: Repair assignments and tracking

See [Database Schema Documentation](../README.md) for detailed field descriptions.

## 🧪 Testing

### Using cURL

#### Test Registration
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "phone": "1234567890",
    "role": "user",
    "password": "password123"
  }'
```

#### Test Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

#### Test Report Submission
```bash
curl -X POST http://localhost:8000/api/reports \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "image=@pothole.jpg" \
  -F "latitude=34.0522" \
  -F "longitude=-118.2437" \
  -F "description=Test pothole report"
```

### Using Swagger UI

1. Navigate to http://localhost:8000/docs
2. Click "Authorize" and enter your JWT token
3. Test endpoints interactively

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config/
│   │   ├── __init__.py       # Settings configuration
│   │   └── database.py       # MongoDB connection
│   ├── models/               # Pydantic data models
│   │   ├── user.py
│   │   ├── report.py
│   │   ├── verification.py
│   │   ├── risk_zone.py
│   │   └── repair.py
│   ├── routes/               # API endpoints
│   │   ├── auth.py
│   │   ├── reports.py
│   │   ├── zones.py
│   │   └── repairs.py
│   ├── services/             # Business logic
│   │   ├── image_service.py
│   │   ├── ai_verification_service.py
│   │   └── clustering_service.py
│   └── utils/                # Utilities
│       ├── auth.py
│       └── validators.py
├── uploads/                  # Uploaded images
├── .env                      # Environment variables
├── .env.example              # Example environment config
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🔒 Security

- Passwords are hashed using bcrypt
- JWT tokens expire after 30 minutes (configurable)
- File uploads are validated for type and size
- Role-based access control on sensitive endpoints
- CORS configured for frontend access

**⚠️ Production Recommendations:**
- Change `JWT_SECRET_KEY` to a strong random value
- Use HTTPS only
- Restrict CORS origins to your frontend domain
- Use environment variables for all secrets
- Enable MongoDB authentication
- Implement rate limiting

## 🌐 Frontend Integration

The backend is designed to work with the frontend HTML pages. To connect the frontend:

1. Add JavaScript `fetch()` calls to the HTML pages
2. Store JWT token in localStorage after login
3. Include token in Authorization header for protected endpoints
4. Handle file uploads using FormData

Example JavaScript:
```javascript
// Login
const response = await fetch('http://localhost:8000/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password })
});
const { access_token } = await response.json();
localStorage.setItem('token', access_token);

// Submit Report
const formData = new FormData();
formData.append('image', fileInput.files[0]);
formData.append('latitude', 34.0522);
formData.append('longitude', -118.2437);

await fetch('http://localhost:8000/api/reports', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}` },
  body: formData
});
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGODB_URI` | MongoDB connection string | `mongodb://localhost:27017` |
| `MONGODB_DB_NAME` | Database name | `pothole_detection` |
| `JWT_SECRET_KEY` | JWT signing secret | *Required* |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry time | `30` |
| `UPLOAD_DIR` | Upload directory | `uploads` |
| `MAX_FILE_SIZE_MB` | Max upload size | `10` |

## 🐛 Troubleshooting

### MongoDB Connection Error
```
Error connecting to MongoDB: ServerSelectionTimeoutError
```
**Solution**: Make sure MongoDB is running on `localhost:27017` or update `MONGODB_URI` in `.env`

### Module Not Found Error
```
ModuleNotFoundError: No module named 'fastapi'
```
**Solution**: Activate virtual environment and install dependencies:
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Port Already in Use
```
ERROR: Address already in use
```
**Solution**: Change port or kill the process using port 8000:
```bash
uvicorn app.main:app --reload --port 8001
```

## 📞 Support

For issues or questions:
- Check API documentation at `/docs`
- Review error messages in terminal
- Ensure MongoDB is running
- Verify environment variables are set correctly

## 📄 License

This project is part of an academic assignment for AI-Based Road Damage Detection.

---

**Built with**: FastAPI, MongoDB, Python 3.9+
