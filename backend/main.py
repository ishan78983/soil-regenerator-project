from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import SoilDataInput
from .services import get_ai_recommendation
from . import database as db

# Initialize the FastAPI app
app = FastAPI(
    title="Soil Regeneration API",
    description="API for generating AI-driven soil regeneration practices.",
    version="1.0.0"
)

# Allow the frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    """Initialize the database when the API starts."""
    db.init_database()

@app.post("/generate", summary="Generate Soil Recommendation")
async def generate_recommendation(soil_data: SoilDataInput):
    """
    Receives soil data, gets a recommendation from the AI, saves it,
    and returns the recommendation.
    """
    try:
        data_dict = soil_data.dict()
        recommendation_text = get_ai_recommendation(data_dict)
        
        db_data = data_dict.copy()
        db_data['recommendation_text'] = recommendation_text
        
        conn = db.create_connection()
        if conn:
            db.save_recommendation(conn, db_data)
            conn.close()
        
        return {"recommendation": recommendation_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history", summary="Get All Recommendations")
async def get_history():
    """Retrieves all past recommendations from the database."""
    conn = db.create_connection()
    if conn:
        recommendations = db.get_all_recommendations(conn)
        conn.close()
        return recommendations
    else:
        raise HTTPException(status_code=500, detail="Could not connect to the database.")