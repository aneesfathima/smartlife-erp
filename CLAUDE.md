# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SmartLife ERP is an Odoo 17-based Enterprise Resource Planning system with custom modules for asset management, volunteer coordination, loyalty points, and RESTful API access. The system runs in Docker containers with PostgreSQL as the database backend.

## Technology Stack

- **Framework**: Odoo 17.0 (Python-based ERP framework)
- **Database**: PostgreSQL 16
- **Containerization**: Docker Compose
- **API**: Custom REST API with JWT authentication
- **Platform**: Windows (development environment)

## Development Commands

### Docker & Container Management

```bash
# Start the ERP system
docker-compose up

# Restart services
docker-compose restart

# View running containers
docker ps

# View logs
docker-compose logs odoo17
docker-compose logs postgres-db

# Execute commands in containers
docker-compose exec odoo17 bash
docker-compose exec postgres-db psql -U odoo -d erp.smartlifefoundation.org
```

### Database Operations

```bash
# Access database from container
docker-compose exec postgres-db psql -U odoo -d erp.smartlifefoundation.org

# Restore database from backup (PowerShell)
powershell -ExecutionPolicy Bypass -File "E:\git\smartlife-erp\scripts\erp-smartlifefoundation-to-local\to-local.ps1"
```

### Testing

```bash
# Run API tests (Python 3)
python test_attendance_api.py
python test_user_activity_api.py
python test_students_endpoint.py
python test_signup.py
python verify_signup.py
```

### Odoo Development

```bash
# Restart Odoo after code changes
docker-compose restart odoo17

# Update module after changes
# Access Odoo UI at http://localhost:8091
# Apps menu -> Update module
```

## Architecture

### Service Architecture

- **odoo17**: Main application server (port 8091 for HTTP, 8092 for long polling)
- **postgres-db**: PostgreSQL database (port 5432)
- Network: `network-odoo` (external Docker network)

### Directory Structure

- `addons/`: Custom Odoo modules
  - `rest_api/`: RESTful API module with JWT authentication
  - `eg_asset_management/`: Asset and volunteer management
  - `eg_asset_signup/`: User registration functionality
  - `muk_web_*`: UI theme modules
  - `auto_database_backup/`: Automated backup functionality
- `config/`: Odoo configuration files (odoo.conf)
- `data/`: Odoo data directory
- `uploads/`: File uploads
- `media/`: Media files
- `scripts/`: Database restore and utility scripts
- `test_*.py`: API test scripts (root level)

### Key Custom Modules

**rest_api** (v17.0.1.14.8)
- JWT-based authentication system (`controllers/auth.py`, `controllers/jwt_utils.py`)
- Token management with Redis/simple store options
- Custom controllers for domain-specific endpoints:
  - `attendance_controller.py`: Student attendance management
  - `loyalty_controller.py`: Loyalty points system
  - `user_activity_controller.py`: User activity tracking
  - `volunteer_controller.py`: Volunteer management
  - `asset_controller.py`: Asset operations
  - `projects_controller.py`: Project management APIs
  - `registration_controller.py`: User registration
  - `survey_controller.py`, `helpdesk_controller.py`, `promotion_controller.py`
- Models: `loyalty_points.py`, `user_activity.py`, `app_usage_rule.py`
- Rate limiting and request validation

**eg_asset_management**
- Models: Assets, locations, moves, volunteers, projects, tasks, attendance
- Custom fields on `res.users` and `res.partner` for volunteer data
- Task attendance tracking with approval workflows
- Integration with loyalty points system

### Authentication Flow

1. Client requests tokens via `/api/auth/get_tokens` with username/password
2. Server validates credentials and returns JWT access + refresh tokens
3. Subsequent requests include `Authorization: Bearer <token>` header
4. JWT tokens decoded using `get_user_id_from_jwt()` helper
5. Token refresh via `/api/auth/refresh_token`

### Database Configuration

- Database name: `erp.smartlifefoundation.org`
- User: `odoo` / Password: `odoo`
- Connection pooling: 64 max connections
- Memory limits: 2GB soft / 2.5GB hard
- Workers: 0 (single-threaded mode)

## Key Conventions

### Odoo Module Structure
- `__manifest__.py`: Module metadata, dependencies, data files
- `models/`: Python models (ORM classes)
- `controllers/`: HTTP controllers for web/API routes
- `views/`: XML view definitions
- `security/`: Access control (ir.model.access.csv)
- `data/`: XML data files (cron jobs, config parameters, rules)

### API Controller Pattern
- Inherit from `http.Controller`
- Use `@http.route()` decorator for endpoints
- JWT validation via `get_user_id_from_jwt()` helper
- Return JSON responses via `request.make_json_response()`
- Standard error codes: 400 (bad request), 401 (unauthorized), 403 (forbidden), 500 (server error)

### Model Conventions
- Inherit from `models.Model` for persistent models
- Use `_name`, `_description`, `_order` attributes
- Field definitions use `fields.Type()` format
- Use `@api.depends()` for computed fields
- Use `@api.constrains()` for validation

### Testing Pattern
- Test scripts use `requests` library
- Base URL: `http://localhost:8091`
- Authenticate first, then test endpoints
- Store session/tokens for subsequent requests

## Configuration Files

- `config/odoo.conf`: Main Odoo configuration
  - Addons path: `/mnt/extra-addons` (mapped to `./addons`)
  - Database connection settings
  - Performance tuning parameters
  - Logging configuration

## Database Restore Process

The `scripts/erp-smartlifefoundation-to-local/to-local.ps1` script automates:
1. Creating backup on remote server (194.163.184.76)
2. Downloading database dump and filestore
3. Stopping local Odoo container
4. Dropping and recreating local database
5. Restoring database and filestore
6. Restarting services

## Important Notes

- Windows platform: Use PowerShell for scripts, paths use backslashes
- Always restart Odoo container after code changes: `docker-compose restart odoo17`
- JWT secret stored in `ir.config_parameter` as `rest_api.jwt_secret`
- Custom addons auto-loaded from `./addons` directory
- Database backups stored in `C:\odoo\restore-bk`
