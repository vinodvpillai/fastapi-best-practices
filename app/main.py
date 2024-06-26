from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controller.article_controller import article_controller
from app.core.log_middleware import LoggingMiddleware
from app.core.env_settings import settings
from app.core.database import engine, Base

app = FastAPI()

# Cross-Origin Resource Sharing (CORS), which allows to control which domains can access your API.
origins = settings.CLIENT_ORIGIN

# Create the database tables
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Custom Logging Middleware
app.add_middleware(LoggingMiddleware)

# Include the router
app.include_router(article_controller.router, tags=['Articles'], prefix='/api/articles')


@app.get('/api/healthchecker')
def root():
    return {'message': 'Service is running'}

# Run the application
# To run: `uvicorn app.main:app --reload`
