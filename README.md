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

## Running the frontend

First enter the frontend folder and install the dependencies with `npm i`, then run the development server with
`npm run dev`

## Running the backend

First, make sure you have a venv setup for the project, then enter the backend folder and install the dependencies with
`pip: -r requirements.txt`. Make sure to also have ghdl installed and available on the PATH. To run the development
server you can use the command `uvicorn main:app --reload` or use PyCharm which has the command configured.