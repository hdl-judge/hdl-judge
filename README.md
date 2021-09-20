# HDL Judge
An online environment for learning digital systems with Hardware Description Languages (HDLs)

## Folder organization
```
./src/
├── backend/
│   ├── adapters/
│   │   ├── primary/     main interfaces of the application
│   │   └── secondary/   code that interfaces with the database and external services
│   ├── controllers/     main business logic
│   └── dependencies/    code for dependency injection
└── frontend/
    ├── src/
    │   ├── components/  components meant to be reused
    │   ├── routes/      the main pages of the web app
    │   └── utils/       useful functions
    └── public/          global html, css and images
```

## Running the frontend

First enter the frontend folder and install the dependencies with `npm i`, then run the development server with
`npm run dev`

## Running the backend

First, make sure you have a venv setup for the project, then enter the backend folder and install the dependencies with
`pip -r requirements.txt`. Make sure to also have ghdl installed and available on the PATH. To run the development
server you can use the command `python ./src/backend/start.py` or use PyCharm which has the command configured.