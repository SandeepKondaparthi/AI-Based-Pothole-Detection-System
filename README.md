# RoadCare — AI-Based Pothole Detection System

A production-oriented, full-stack platform for **automated pothole detection, citizen reporting, and infrastructure repair coordination**, powered by computer vision and geospatial analytics.

---

## Overview

**RoadCare** is an end-to-end system that helps municipalities, smart-city programs, and road authorities detect, verify, prioritize, and fix potholes at scale. It combines a **citizen-facing reporting experience** with an **authority dashboard**, an **AI verification pipeline** (YOLOv8), and **geospatial risk clustering** so teams move from reactive complaint handling to proactive maintenance.

The platform supports the full lifecycle:

- **Citizens** capture a photo, attach GPS location, and submit a report; AI scores confidence in near real time.
- **Authorities** review AI assessments, approve or reject reports, inspect high-risk zones, and create repair actions.
- **Operators** monitor dashboards, track status, and coordinate repairs with role-based access control.

Authentication is **JWT-based** with role separation (citizen vs authority). Reports and zones are stored in **MongoDB** with geospatial indexes; risk zones use **Uber H3** hexagonal clustering. The stack is designed for local development and deployment with clear API boundaries between the React portal, FastAPI services, and the ML inference path.

---

## Problem Statement

Manual road inspection is typically:

| Challenge | Impact |
|-----------|--------|
| **Time-consuming** | Intensive field surveys and slow coverage |
| **Expensive** | High labor and operational cost |
| **Inconsistent** | Subjective severity ratings and human bias |
| **Reactive** | Damage often addressed only after repeated complaints |

**RoadCare** addresses this by automating visual detection, standardizing confidence scores, clustering reports into risk zones, and giving authorities a single place to verify, prioritize, and assign repairs.

---

## Stack

| Layer | Technology | Notes |
|-------|------------|--------|
| **Frontend** | React 18, Vite, Tailwind CSS, React Router | Citizen app, authority dashboard, analytics views |
| **Backend** | FastAPI, Python 3.9+, async I/O | REST APIs, file upload, JWT auth |
| **AI / ML** | YOLOv8, OpenCV, TensorFlow, NumPy | Image inference, confidence scoring |
| **Database** | MongoDB | Document store with geospatial indexes |
| **Geospatial** | Uber H3 | Hexagonal clustering of reports into risk zones |
| **Authentication** | JWT | Access tokens with role-based authorization |
| **Real-time (optional)** | WebSocket / polling | Status updates on reports and repairs |

---

## Features

### 1. AI-powered detection
- YOLOv8-based inference on uploaded road images.
- Confidence score per detection to drive auto-verification thresholds.
- Image preprocessing via OpenCV before model input.

### 2. Citizen reporting
- Mobile-friendly report flow: photo upload + GPS coordinates.
- Optional description and severity hints from the user.
- Immediate feedback when AI verification completes.
- Track personal report status over time.

### 3. Auto-verification with human review
- Confidence-based rules (e.g. auto-flag high-confidence detections).
- Authority queue queue for borderline or disputed cases.
- Approve / reject with audit-friendly status transitions.

### 4. Geolocation and mapping
- GPS attached at report time (browser or device location).
- Map-oriented listing and detail views for authorities.
- Spatial queries over MongoDB geospatial indexes.

### 5. Risk analytics and zone clustering
- H3 hexagonal aggregation of nearby reports.
- High-risk zone identification for prioritization.
- Recalculate zones on demand after new batches of reports.

### 6. Authority dashboard
- Pending reports, verified damage, and repair pipeline in one place.
- Filters by status, severity, and geography.
- Create and update repair actions linked to reports or zones.

### 7. Role-based access
- **Citizen** — submit and track own reports.
- **Authority** — verify, manage zones, assign repairs.
- Protected routes on the frontend; JWT-enforced APIs on the backend.

### 8. Repair coordination
- Create repair tickets from verified reports or risk zones.
- Update repair status (scheduled, in progress, completed).
- List and filter repair actions for operational follow-up.

---

## Architecture overview

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                     │
│  ┌────────────────┐  ┌──────────────────┐  ┌────────────┐   │
│  │  Citizen App   │  │ Authority Admin  │  │ Dashboard  │   │
│  │    (React)     │  │    Dashboard     │  │ Analytics  │   │
│  └────────────────┘  └──────────────────┘  └────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │ HTTPS / WebSocket
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     API Layer (FastAPI)                     │
│  ┌──────────────┐  ┌────────────┐  ┌──────────────────┐     │
│  │ Auth Routes  │  │ Report API │  │ Zone Clustering  │     │
│  └──────────────┘  └────────────┘  └──────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   AI / ML Processing Engine                 │
│  ┌────────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Image Upload   │  │ YOLOv8 Model │  │ Confidence      │  │
│  │ Processing     │  │ Inference    │  │ Scoring         │  │
│  └────────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Data Persistence & Analytics                   │
│  ┌──────────────────┐  ┌────────────────┐  ┌────────────┐   │
│  │ MongoDB          │  │ H3 Clustering  │  │ Reports &  │   │
│  │ Geospatial DB    │  │ Risk Zones     │  │ Analytics  │   │
│  └──────────────────┘  └────────────────┘  └────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Key workflows

### Citizen report flow
1. User opens the report page and uploads a pothole image.
2. GPS coordinates are captured (or entered) with the submission.
3. Backend stores the report and runs YOLOv8 inference.
4. A confidence score is attached; status is set (e.g. pending review / auto-verified).
5. Citizen can track status from their report list or detail view.

### Authority review flow
1. Dashboard lists pending and high-priority reports.
2. Authority opens a report, reviews image + AI assessment.
3. Approves or rejects verification and optionally adjusts severity.
4. Views clustered **risk zones** for the same area.
5. Creates a **repair action** and updates it through completion.

---

## API overview

Base path prefix: `/api` (adjust host/port per environment).

### Authentication — `/api/auth`

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/register` | Public | Register citizen or authority user |
| POST | `/login` | Public | Login; returns JWT (and refresh if implemented) |
| POST | `/logout` | JWT | Invalidate session / token side effects |
| POST | `/refresh` | Public / JWT | Refresh access token |

### Reports — `/api/reports`

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/` | JWT (Citizen) | Submit pothole report with image + location |
| GET | `/` | JWT | List reports (paginated; scoped by role) |
| GET | `/{id}` | JWT | Report detail including AI result |
| PUT | `/{id}/status` | JWT (Authority) | Update verification / workflow status |

### Risk zones — `/api/zones`

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/` | JWT | List risk zones |
| GET | `/high-risk` | JWT | High-severity zones only |
| POST | `/recalculate` | JWT (Authority) | Rebuild H3 clusters from current reports |

### Repairs — `/api/repairs`

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/` | JWT (Authority) | Create repair action |
| PUT | `/{id}` | JWT (Authority) | Update repair status / details |
| GET | `/` | JWT | List repair actions |

---

## Data model (logical schema)

RoadCare uses **MongoDB** collections rather than a relational schema. The logical model aligns with the backend `models/` package.

### Collections (conceptual)

| Collection | Purpose | Notable fields |
|------------|---------|----------------|
| **users** | Accounts and roles | email, password hash, role (`citizen` / `authority`), profile |
| **reports** | Citizen pothole submissions | image path/URL, GPS (`location` GeoJSON), AI confidence, status, severity, timestamps |
| **verifications** | AI + human verification trail | report id, model version, confidence, reviewer id, decision |
| **risk_zones** | H3-aggregated risk areas | H3 index, report count, severity score, bounds, last calculated |
| **repairs** | Work orders | linked report/zone ids, assignee, status, scheduled/completed dates |

### Geospatial notes
- Report locations should be stored in a form compatible with MongoDB **2dsphere** indexes (e.g. GeoJSON `Point`).
- Risk zones are derived via **Uber H3** resolution chosen for city-block vs neighborhood granularity.
- Indexes recommended: `reports.location`, `reports.status`, `reports.created_at`, `risk_zones.h3_index`.

---

## Project structure

```
RoadCare/
├── README.md
├── .env.example
├── .gitignore
│
├── backend/                          # FastAPI + AI services
│   ├── requirements.txt
│   ├── run.py
│   └── app/
│       ├── main.py                   # FastAPI application entry
│       ├── config/
│       │   ├── database.py           # MongoDB connection
│       │   └── settings.py           # Env / app configuration
│       ├── models/
│       │   ├── user.py
│       │   ├── report.py
│       │   ├── verification.py
│       │   ├── risk_zone.py
│       │   └── repair.py
│       ├── routes/
│       │   ├── auth.py
│       │   ├── reports.py
│       │   ├── zones.py
│       │   └── repairs.py
│       ├── services/
│       │   ├── ai_verification_service.py   # YOLOv8 inference
│       │   ├── image_service.py
│       │   └── clustering_service.py        # H3 risk zones
│       └── utils/
│
└── frontend/                         # React + Vite patient/citizen portal
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── components/
        │   ├── Header.jsx
        │   ├── Footer.jsx
        │   ├── LoadingSpinner.jsx
        │   └── ProtectedRoute.jsx
        ├── pages/
        │   ├── HomePage.jsx
        │   ├── ReportPotholePage.jsx
        │   ├── AuthorityDashboardPage.jsx
        │   └── ComplaintDetailPage.jsx
        ├── context/
        │   ├── AuthContext.jsx
        │   └── ThemeContext.jsx
        └── services/
            └── apiService.js
```

---

## Getting started

### Prerequisites
- Python 3.9+
- Node.js 18+ (20 recommended)
- MongoDB 6+ (local or Atlas)
- (Optional) CUDA-capable GPU for faster YOLOv8 inference

### Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env   # set MONGODB_URI, JWT_SECRET, model paths, etc.
python run.py
```

API typically at `http://localhost:8000`. Interactive docs: `http://localhost:8000/docs` (FastAPI Swagger).

### Frontend

```bash
cd frontend
npm install
npm run dev
```

UI typically at `http://localhost:5173`. Point the API base URL at the FastAPI server via env (e.g. `VITE_API_URL`).

### Environment (example)

| Variable | Description |
|----------|-------------|
| `MONGODB_URI` | MongoDB connection string |
| `JWT_SECRET` | Signing secret for tokens |
| `YOLO_MODEL_PATH` | Path to YOLOv8 weights |
| `UPLOAD_DIR` | Directory for stored report images |
| `H3_RESOLUTION` | Uber H3 resolution for clustering |
| `VITE_API_URL` | Frontend API base URL |

---

## Real-world applications

| Domain | Use |
|--------|-----|
| **Municipal road maintenance** | Automated inspection intake and work prioritization |
| **Smart cities** | Continuous road-quality signal from citizen + AI pipeline |
| **Insurance** | Objective, timestamped damage documentation |
| **Urban planning** | Aggregated infrastructure condition by zone |
| **Fleet / logistics** | Avoid high-risk segments; feed route planning |

