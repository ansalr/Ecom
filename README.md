## Setup & Run

### Option 1: Docker
1. **Prerequisites**: Docker & Docker Compose.
2. **Run**:
   ```bash
   docker-compose up --build
   ```
3. **Migrate** (first time only):
   ```bash
   docker-compose exec web python manage.py migrate
   ```
4. **Create Admin User**:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```
5. **Access**: Open (http://localhost:8000).

### Option 2: Local Method
1. **Prerequisites**: Python 3.12+, pip.
   **Note**: Uses SQLite by default locally.
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment Setup**:
   Ensure `.env` exists (see below).
4. **Migrate**:
   ```bash
   python manage.py migrate
   ```
5. **Create User**:
   ```bash
   python manage.py createsuperuser
   ```
6. **Run Server**:
   ```bash
   python manage.py runserver
   ```

## Environment Variables (.env)
Create a `.env` file in the root directory:
```
DEBUG=True
SECRET_KEY=dev-secret-key-12345
POSTGRES_DB=minicrm
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Testing
Run automated tests:
```bash
python manage.py test core
```

## API Docs
- Health Check: `GET /health/`
- API Root: `/api/`


# Architecture Documentation 

## Components

### 1. Django Backend 
- **Core App**: Contains all business logic and models.
- **Models**:
  - `Organization` & `Contact`: Customer data.
  - `Product` & `SizePrice`: Catalog data with support for dynamic variation pricing.
  - `Order` & `OrderItem`: Transactional data.
  - `User`: Extended Custom User model with Role-Based Access Control.
- **Service Layer (`services.py`)**:
  - Encapsulates Price Calculation and Cart Merging logic.
  - Keeps Views thin and testable.
- **API Layer (django restframework)**:
  - Exposes RESTful endpoints.
  - Uses JWT (JSON Web Tokens) for stateless authentication.

### 2. Database sqllite
- Relational schema with foreign key constraints ensures data integrity.
- `JSONField` used in `OrderItem` for `extras` allows flexibility for product customization without schema migration.

### 3. Frontend (Vanilla JS + Templates)
- Lightweight client-side application.
- Decoupled from backend logic; communicates strictly via JSON API.
- **Benefits**: Fast load times, no complex build step (Webpack/Vite), easy to debug.

## Trade-offs
- **SQLite vs Postgres**: Setup supports both. SQLite is used for local dev simplicity (no Docker requirement), while Postgres is configured for production reliability.
- **Vanilla JS vs React/Vue**: Chosen Vanilla JS for simplicity and to demonstrate core understanding of DOM/Fetch without framework overhead. For larger scale, React would be preferred for state management.
- **JSONField for Extras**: chosen for flexibility. Trade-off is less ability to query deep into structure efficiently compared to a normalized EAV model, but sufficient for order history.

## Scaling & Security
- **Security**:
  - JWT Auth ensures stateless secure access.
  - Env vars for secrets.
  - `ALLOWED_HOSTS` and `DEBUG` checks.
- **Scaling**:
  - Dockerized container allows horizontal scaling behind a Load Balancer.
  - Database can be moved to a managed instance (RDS/Cloud SQL).
  - Static files served by Nginx/CDN (in production setup).