from fastapi import FastAPI


# create an instance of the FastAPI class
app = FastAPI()


# Define a path operation for the root URL
@app.get("/")
async def read_root():
    return {"message": "authentication api is running"}

