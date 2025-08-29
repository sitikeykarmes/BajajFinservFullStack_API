from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
import os
from pydantic import BaseModel
from typing import List, Any

# Create the main app
app = FastAPI(title="BFHL Array Data Processing API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models
class BFHLRequest(BaseModel):
    data: List[Any]

class BFHLResponse(BaseModel):
    is_success: bool
    user_id: str
    email: str
    roll_number: str
    odd_numbers: List[str]
    even_numbers: List[str]
    alphabets: List[str]
    special_characters: List[str]
    sum: str
    concat_string: str

# Helper functions
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_alphabet(s):
    return s.isalpha() and len(s) == 1

def process_array_data(data_array):
    odd_numbers = []
    even_numbers = []
    alphabets = []
    special_characters = []
    all_alphabets_for_concat = []
    total_sum = 0
    
    for item in data_array:
        item_str = str(item)
        
        if is_number(item_str):
            num = int(item_str)
            total_sum += num
            if num % 2 == 0:
                even_numbers.append(item_str)
            else:
                odd_numbers.append(item_str)
        elif is_alphabet(item_str):
            alphabets.append(item_str.upper())
            all_alphabets_for_concat.append(item_str)
        else:
            if len(item_str) > 1 and item_str.isalpha():
                alphabets.append(item_str.upper())
                for char in item_str:
                    all_alphabets_for_concat.append(char)
            else:
                special_characters.append(item_str)
    
    concat_string = create_alternating_caps_string(all_alphabets_for_concat)
    
    return {
        "odd_numbers": odd_numbers,
        "even_numbers": even_numbers,
        "alphabets": alphabets,
        "special_characters": special_characters,
        "sum": str(total_sum),
        "concat_string": concat_string
    }

def create_alternating_caps_string(alphabet_chars):
    if not alphabet_chars:
        return ""
    
    reversed_chars = list(reversed(alphabet_chars))
    result = ""
    for i, char in enumerate(reversed_chars):
        if i % 2 == 0:
            result += char.lower()
        else:
            result += char.upper()
    
    return result

# API Routes
@api_router.get("/")
async def root():
    return {"message": "BFHL Array Data Processing API", "status": "running", "docs": "/docs"}

@api_router.post("/bfhl")
async def process_bfhl_data(request: BFHLRequest):
    try:
        processed_data = process_array_data(request.data)
        
        return BFHLResponse(
            is_success=True,
            user_id="john_doe_17091999",
            email="john@xyz.com",
            roll_number="ABCD123",
            odd_numbers=processed_data["odd_numbers"],
            even_numbers=processed_data["even_numbers"],
            alphabets=processed_data["alphabets"],
            special_characters=processed_data["special_characters"],
            sum=processed_data["sum"],
            concat_string=processed_data["concat_string"]
        )
        
    except Exception as e:
        return BFHLResponse(
            is_success=False,
            user_id="john_doe_17091999",
            email="john@xyz.com", 
            roll_number="ABCD123",
            odd_numbers=[],
            even_numbers=[],
            alphabets=[],
            special_characters=[],
            sum="0",
            concat_string=""
        )

# Include router
app.include_router(api_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],  # Allow all origins for now
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def health_check():
    return {"status": "healthy", "message": "BFHL API is running"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)