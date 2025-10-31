# to-do-notes-manager-216126-216135

Backend Django API provides CRUD endpoints for to-do notes.

How to run locally:
- Install dependencies: pip install -r backend_django_api/requirements.txt
- Apply migrations:
  - cd backend_django_api
  - python manage.py migrate
- Start server: python manage.py runserver 0.0.0.0:3001
- API docs: http://localhost:3001/docs (Swagger UI)
- OpenAPI JSON: http://localhost:3001/openapi.json

Endpoints (all return/accept JSON):
- GET    /api/notes/            -> list notes
- POST   /api/notes/            -> create note (title required)
- GET    /api/notes/<id>/       -> retrieve note
- PUT    /api/notes/<id>/       -> update note
- PATCH  /api/notes/<id>/       -> partial update
- DELETE /api/notes/<id>/       -> delete note

Model:
- id (auto), title (required), description (optional), is_completed (bool, default false), created_at, updated_at

Validation:
- title is required on create; 400 returned if missing or blank.

CORS:
- Configured permissively for local preview.

Env:
- No required environment variables for local SQLite setup.
