from fastapi import APIRouter, HTTPException

from communication.engine_instance import engine
from communication.schemas import LoadModelRequest

router = APIRouter()


# =====================================================
# GET AVAILABLE MODELS
# =====================================================

@router.get("/models")
def get_models():

    return engine.get_available_models()


# =====================================================
# LOAD MODEL
# =====================================================

@router.post("/model/load")
def load_model(
    request: LoadModelRequest
):

    try:

        engine.load_model(

            request.model_name

        )

        return engine.get_loaded_model_info()

    except ValueError as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )
    

# =====================================================
# GET CURRENT MODEL
# =====================================================

@router.get("/model/current")
def get_current_model():

    return engine.get_current_model()


@router.post("/detection/run")
def run_detection():

    try:

        return engine.run_detection()

    except ValueError as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )