from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from pydantic import BaseModel
from typing import List, Any


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

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


# Helper functions for BFHL logic
def is_number(s):
    """Check if string represents a number"""
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_alphabet(s):
    """Check if string is an alphabetic character"""
    return s.isalpha() and len(s) == 1

def process_array_data(data_array):
    """Process the input array and categorize elements"""
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
            # Handle multi-character strings containing alphabets
            if len(item_str) > 1 and item_str.isalpha():
                alphabets.append(item_str.upper())
                # Add each character for concatenation
                for char in item_str:
                    all_alphabets_for_concat.append(char)
            else:
                special_characters.append(item_str)
    
    # Create concatenated string with alternating caps
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
    """Create concatenated string in reverse order with alternating caps"""
    if not alphabet_chars:
        return ""
    
    # Reverse the order of characters
    reversed_chars = list(reversed(alphabet_chars))
    
    # Apply alternating caps (start with lowercase for first char)
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
    return {"message": "BFHL Array Data Processing API", "status": "running"}

@api_router.post("/bfhl", response_model=BFHLResponse)
async def process_bfhl_data(request: BFHLRequest):
    """
    Process array data and return categorized results
    """
    try:
        # Process the input data
        processed_data = process_array_data(request.data)
        
        # Create response
        response = BFHLResponse(
            is_success=True,
            user_id="john_doe_17091999",  # Static user info as per example
            email="john@xyz.com",
            roll_number="ABCD123",
            odd_numbers=processed_data["odd_numbers"],
            even_numbers=processed_data["even_numbers"],
            alphabets=processed_data["alphabets"],
            special_characters=processed_data["special_characters"],
            sum=processed_data["sum"],
            concat_string=processed_data["concat_string"]
        )
        
        return response
        
    except Exception as e:
        # Log the error for debugging
        logger.error(f"Error processing BFHL data: {str(e)}")
        
        # Return error response
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

# Include the router in the main app
app.include_router(api_router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)