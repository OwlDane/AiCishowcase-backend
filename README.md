# AiCi Showcase Backend

Official backend API for the AiCi Showcase platform, a digital gallery for student AI projects.

## Tech Stack

- Python 3.x
- Django 6.0
- Django Rest Framework (DRF)
- PostgreSQL (Supabase)
- SimpleJWT (Authentication)
- Django-cors-headers

## Project Structure

This project follows a modular Django architecture, where functionality is split into specialized apps located in the `apps/` directory:

- `apps.users`: Handles custom User models, roles (Admin, Siswa, Public), and Student Profiles.
- `apps.projects`: Manages project categories, submissions, and the moderation workflow (Pending, Approved, Rejected).
- `apps.interactions`: Implements the engagement system, specifically the project liking mechanism with anti-spam logic.

## Key Features

- **Role-Based Access Control**: Different permissions for Admins, Students, and Public visitors.
- **Automated Profiles**: Student profiles are created automatically upon registration via Django signals.
- **Project Moderation**: Projects require admin approval before becoming publicly visible.
- **Fair Engagement**: Project likes are restricted by both User ID (for authenticated users) and IP Address (for public users) to prevent spam.
- **Advanced Filtering**: Support for searching and filtering by category, batch (angkatan), and status.

## Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd aicishowcase-backend
   ```

2. **Setup Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**
   Copy the example environment file and fill in your credentials:

   ```bash
   cp .env.example .env
   ```

5. **Run Migrations**

   ```bash
   python manage.py migrate
   ```

6. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

## Core API Endpoints

### Authentication

- `POST /api/users/register/`: Register a new account.
- `POST /api/users/login/`: Obtain JWT access and refresh tokens.
- `GET /api/users/me/`: Retrieve current user information.

### Showcase

- `GET /api/showcase/projects/`: List approved projects.
- `POST /api/showcase/projects/`: Submit a new project (requires Siswa role).
- `GET /api/showcase/categories/`: List available project categories.

### Interactions

- `POST /api/interactions/likes/toggle/`: Toggle like/unlike on a project.

## Development Standards

- **DRY Principle**: Logic is kept in models (fat models) or serializers where appropriate.
- **Scalability**: Modular apps allow for easy feature expansion.
- **Security**: Sensitive data is managed through environment variables and is excluded from version control.
