# HDL Judge
An online environment for learning digital systems with Hardware Description Languages (HDLs)

## Folder organization
```
./src/
├── backend/
│   ├── api/             code specific to fastapi 
│   │   ├── controllers/ definition of the api endpoints
│   │   └── schemas/     definitions of pydantic schemas
│   ├── models/          database models
│   ├── repos/           code that interfaces with the database and external services
│   ├── services/        code that contains the business logic
│   ├── tests/           tests
│   └── worker/          code specific to celery
└── frontend/
    ├── src/
    │   ├── components/  components meant to be reused
    │   └── routes/      the main pages of the web app
    ├── public/          global html, css and images
    └── tests/           tests
```