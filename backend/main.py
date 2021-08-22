import subprocess

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI()

origins = [
    "http://localhost:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/test/execute")
async def execute_test(file: UploadFile = File(...)):
    content = await file.read()

    with open("adder.vhdl", "wb") as f:
        f.write(content)

    subprocess.run(["ghdl", "-a", "adder.vhdl", "adder_tb.vhdl"])
    subprocess.run(["ghdl", "-e", "adder_tb"])
    subprocess.run(["ghdl", "-r", "adder_tb", "--vcd=adder.vcd"])

    return FileResponse("adder.vcd", filename="adder.vcd")
