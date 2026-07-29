from fastapi import APIRouter, HTTPException

from communication.engine_instance import engine
from communication.schemas import (
    LoadDatasetRequest,
    WindowConfigurationRequest,
    RandomConfigurationRequest,
    ConfigurationRequest,
    RunPreprocessingRequest,
)
import cv2
import tempfile

from fastapi.responses import FileResponse

router = APIRouter()


# =====================================================
# GET AVAILABLE DATASETS
# =====================================================

@router.get("/datasets")
def get_datasets():

    return engine.get_available_datasets()


# =====================================================
# GET AVAILABLE MODELS
# =====================================================

@router.get("/models")
def get_models():

    return engine.get_available_models()

# =====================================================
# LOAD DATASET
# =====================================================

@router.post("/dataset/load")
def load_dataset(
    request: LoadDatasetRequest
):

    try:

        engine.load_dataset(
            request.dataset_name
        )

        return engine.get_dataset_info()

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# =====================================================
# GET LABELS
# =====================================================

@router.get("/labels")
def get_labels():

    try:

        return engine.get_labels()

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# =====================================================
# GET PACKETS BY LABEL
# =====================================================

@router.get("/packets/{label}")
def get_packets(

    label: str,

    offset: int = 0,

    limit: int = 500,

):

    try:

        packets = engine.get_packets_by_label(label)

        return packets[offset:offset + limit]

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# =====================================================
# CONFIGURATION
# =====================================================

@router.post("/configuration")
def set_configuration(

    request: ConfigurationRequest

):

    print("\n========== CONFIGURATION RECEIVED ==========")

    print(f"Window Size : {request.window_size}")

    print(f"DWT Level   : {request.dwt_level}")

    print("============================================\n")

    engine.set_configuration(

        window_size=request.window_size,

        dwt_level=request.dwt_level,

    )

    return engine.get_configuration()

# =====================================================
# ADD WINDOW CONFIGURATION
# =====================================================

@router.post("/configuration/add")
def add_configuration(
    request: WindowConfigurationRequest
):

    try:

        engine.add_window_configuration(

            packet_number=request.packet_number,

            position=request.position

        )

        return engine.get_window_configurations()

    except ValueError as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )

# =====================================================
# GET WINDOW CONFIGURATIONS
# =====================================================

@router.get("/window/configurations")
def get_window_configurations():

    return engine.get_window_configurations()


# =====================================================
# RANDOM WINDOW CONFIGURATION
# =====================================================

@router.post("/configuration/random")
def generate_random_configuration(
    request: RandomConfigurationRequest
):

    try:

        return engine.generate_random_configurations(

            request.count

        )

    except ValueError as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )


# =====================================================
# REMOVE WINDOW CONFIGURATION
# =====================================================

@router.delete("/configuration/{packet_number}")
def remove_configuration(
    packet_number: int
):

    try:

        engine.remove_window_configuration(
            packet_number
        )

        return engine.get_window_configurations()

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    

# =====================================================
# PREPARE WINDOWS
# =====================================================

@router.post("/window/prepare")
def prepare_windows():

    try:

        total = engine.prepare_windows()

        return {

            "prepared": total

        }

    except ValueError as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )
    
# =====================================================
# GET PREPARED WINDOW INFO
# =====================================================

@router.get("/window/prepared")
def get_prepared_windows():

    try:

        return engine.get_prepared_window_info()

    except ValueError as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )
    
# =====================================================
# RUN PREPROCESSING
# =====================================================

@router.post("/preprocessing/run")
def run_preprocessing():

    try:

        total = engine.run_preprocessing()

        return {

            "processed": total

        }

    except ValueError as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )
    
    

# =====================================================
# GET PREPROCESSED IMAGE INFO
# =====================================================

@router.get("/preprocessing/images")
def get_preprocessed_images():

    try:

        return engine.get_preprocessed_image_info()

    except ValueError as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )


# =====================================================
# GET PREPROCESSED DATA
# =====================================================

@router.get("/preprocessing/data")
def get_preprocessed_data():

    try:

        result = []

        for item in engine.get_preprocessed_data():

            result.append({

                "packet_number": item["packet_number"],

                "selected_label": item["selected_label"],

                "window_label": item["window_label"],

                "trigger_packet": item["trigger_packet"],

                "attack_labels": item["attack_labels"],

                "position": item["position"],

                "image": item["image"].tolist()

            })

        return result

    except ValueError as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )

# =====================================================
# GET PREPROCESSED IMAGE
# =====================================================

@router.get("/preprocessing/image/{index}")
def get_preprocessed_image(
    index: int
):

    try:

        image = engine.get_preprocessed_image(index)

        temp = tempfile.NamedTemporaryFile(

            suffix=".png",

            delete=False

        )

        cv2.imwrite(

            temp.name,

            image

        )

        return FileResponse(

            temp.name,

            media_type="image/png"

        )

    except ValueError as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )
    
# =====================================================
# GET PREPROCESSED IMAGE
# =====================================================

@router.get("/preprocessing/image/{index}")
def get_preprocessed_image(
    index: int
):

    return FileResponse(

        f"cache/images/image_{index}.png",

        media_type="image/png"

    )


# =====================================================
# CLEAR WINDOW CONFIGURATION
# =====================================================

@router.delete("/configuration")
def clear_configurations():

    engine.clear_window_configurations()

    return engine.get_window_configurations()