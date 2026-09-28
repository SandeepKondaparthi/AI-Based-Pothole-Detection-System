# RoadCare - AI-Based Pothole Detection System

## Overview

**RoadCare** is a full-stack system for automated pothole detection and infrastructure management. Using advanced AI-powered computer vision RoadCare efficiently detect, verify and prioritize potholes complaints making it easy to manage roads.

### Key Features
- **AI-Powered Detection** - YOLOv8-based deep learning for accurate damage identification
- **Citizen Reporting** - Mobile-friendly interface allowing public to easily report potholes
- **Auto-Verification** - Confidence-based verification system with human review
- **Geolocation Mapping** - GPS-based pothole reporting and clustering
- **Risk Analytics** - Identify high-risk zones requiring immediate attention
- **Real-time Dashboard** - Authority monitoring and repair coordination
- **Role-Based Access** - Secure authentication for citizens and authorities

---

## Problem Statement

Manual road inspection is:
- **Time-consuming** - Intensive field surveys
- **Expensive** - High operational costs
- **Inconsistent** - Human error and bias in assessments
- **Reactive** - Addresses issues after complaints

**RoadCare solves this** by automating detection and enabling easy infrastructure management.

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | React 18, Vite, Tailwind CSS, React Router |
| **Backend** | FastAPI, Python 3.9+, Async I/O |
| **AI/ML** | YOLOv8, OpenCV, TensorFlow, NumPy |
| **Database** | MongoDB with geospatial indexing |
| **Geospatial** | Uber H3 hexagonal clustering |
| **Authentication** | JWT tokens with role-based access |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                     │
│  ┌────────────────┐  ┌──────────────────┐  ┌────────────┐   │
│  │  Citizen App   │  │ Authority Admin  │  │ Dashboard  │   │
│  │    (React)     │  │   Dashboard      │  │ Analytics  │   │
│  └────────────────┘  └──────────────────┘  └────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ↓ HTTPS/WebSocket
┌─────────────────────────────────────────────────────────────┐
│                      API Layer (FastAPI)                    │
│  ┌──────────────┐  ┌────────────┐  ┌──────────────────┐     │
│  │ Auth Routes  │  │ Report API │  │  Zone Clustering │     │
│  └──────────────┘  └────────────┘  └──────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   AI/ML Processing Engine                   │
│  ┌────────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Image Upload   │  │ YOLOv8 Model │  │ Confidence      │  │
│  │ Processing     │  │ Inference    │  │ Scoring         │  │
│  └────────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              Data Persistence & Analytics                   │
│  ┌──────────────────┐  ┌────────────────┐  ┌────────────┐   │
│  │    MongoDB       │  │ H3 Clustering  │  │  Reports   │   │
│  │   Geospatial DB  │  │ Risk Zones     │  │ Analytics  │   │
│  └──────────────────┘  └────────────────┘  └────────────┘   │
└─────────────────────────────────────────────────────────────┘

```

---

## Project Structure

```
RoadCare/
├── backend/                                       # Python FastAPI Backend
│   ├── app/
│   │   ├── main.py                                # FastAPI application
│   │   ├── config/
│   │   │   ├── database.py                        # MongoDB connection
│   │   │   └── settings.py                        # Configuration
│   │   ├── models/                                # Data models
│   │   │   ├── user.py
│   │   │   ├── report.py
│   │   │   ├── verification.py
│   │   │   ├── risk_zone.py
│   │   │   └── repair.py
│   │   ├── routes/                                # API endpoints
│   │   │   ├── auth.py
│   │   │   ├── reports.py
│   │   │   ├── zones.py
│   │   │   └── repairs.py
│   │   ├── services/                             # Business logic
│   │   │   ├── ai_verification_service.py        # YOLOv8 inference
│   │   │   ├── image_service.py
│   │   │   └── clustering_service.py
│   │   └── utils/
│   ├── requirements.txt
│   └── run.py
│
├── frontend/                                     # React Vite Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── LoadingSpinner.jsx
│   │   │   └── ProtectedRoute.jsx
│   │   ├── pages/
│   │   │   ├── HomePage.jsx
│   │   │   ├── ReportPotholePage.jsx
│   │   │   ├── AuthorityDashboardPage.jsx
│   │   │   └── ComplaintDetailPage.jsx
│   │   ├── context/
│   │   │   ├── AuthContext.jsx
│   │   │   └── ThemeContext.jsx
│   │   ├── services/
│   │   │   └── apiService.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── .env.example                                  # Environment template
├── .gitignore
└── README.md

```

---

## Key Workflows

### Citizen Report Flow
1. User uploads pothole image
2. GPS coordinates auto-captured
3. AI instantly verifies damage
4. Report submitted with confidence score
5. Real-time status tracking

### Authority Review Flow
1. Dashboard shows pending reports
2. Authority reviews AI assessment
3. Approves or rejects verification
4. Views clustered risk zones
5. Creates repair actions

---

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/refresh` - Refresh JWT token

### Reports
- `POST /api/reports` - Submit pothole report (with image)
- `GET /api/reports` - List all reports (paginated)
- `GET /api/reports/{id}` - Get report details
- `PUT /api/reports/{id}/status` - Update report status (authority only)

### Risk Zones
- `GET /api/zones` - Get all risk zones
- `GET /api/zones/high-risk` - Get high-severity zones
- `POST /api/zones/recalculate` - Recalculate zones (authority only)

### Repairs
- `POST /api/repairs` - Create repair action (authority only)
- `PUT /api/repairs/{id}` - Update repair status
- `GET /api/repairs` - List repair actions

---


## Real-World Applications

- **Municipal Road Maintenance** - Automated inspection reports
- **Smart Cities** - Real-time road quality monitoring
- **Insurance Claims** - Objective damage documentation
- **Urban Planning** - Infrastructure assessment data
- **Fleet Management** - Route optimization