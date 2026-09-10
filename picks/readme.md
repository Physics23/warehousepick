# 🏭 Warehouse Pick-Station Kiosk (Full-Stack Clone)

A full-stack web application that simulates an Amazon-style warehouse pick-station kiosk. 
Operators log in, see the current item to pick, update its status (picked, missing, unscannable, or problem tote), and view live operational metrics (UPH, cycle time, total units).

The app includes an **auto-pilot "Demo Mode"** that randomly simulates real operator behavior, and an **infinite re-seeding loop** so the simulation never runs out of items.

---

## 🧠 Tech Stack

| Layer | Technology |
| :--- | :--- |
| Backend | Python 3.13, Django 6.1, Django REST Framework |
| Database | SQLite (dev) |
| Authentication | Django Session Auth (CSRF-exempt for React SPA) |
| Frontend | React 18 (Vite), Axios, Plain CSS |
| Image Handling | Internet URLs (picsum.photos) for demo |

---

## 🏗️ Architecture

### Backend (Django + DRF)
- **Models**: `Station`, `Item`, `Tote`, `PickSession`, `PickTask`
- **Serializers**: Convert database models to JSON for React
- **Views**:
  - `ModelViewSet` for CRUD on Stations, Items, Totes, Sessions, Tasks
  - `GenericAPIView` for custom endpoints: Current Task and Stats
  - `@action` endpoints: `update_status`, `re-seed`, `start_session`
- **Live Stats**: Computed from `picked_at` timestamps, not stored directly
- **Auth**: Session-based with custom `CsrfExemptSessionAuthentication`

### Frontend (React)
- **Component Architecture**:
  - `LoginScreen` – handles authentication
  - `Header` – displays station ID and live stats
  - `CurrentItem` – shows SKU, name, description, and image
  - `ComparisonPanel` – shows source & destination totes
  - `ActionButtons` – Picked / Unscannable / Missing / Problem Tote
  - `ProblemOverlay` – pauses workflow when a problem is flagged
- **State Management**: Centralized in `App.jsx` (polling every 5 seconds)
- **Demo Mode**: Randomly picks items every 3 seconds with weighted probabilities (70% picked, 10% each for problems)

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm

### 1. Backend Setup
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

# Install dependencies
pip install django djangorestframework django-cors-headers pillow

# Navigate to project
cd warehouse_kiosk

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser (for admin access)
python manage.py createsuperuser

# Run the backend server
python manage.py runserver 127.0.0.1:8000