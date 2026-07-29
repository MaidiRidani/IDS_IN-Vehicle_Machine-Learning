from pydantic import BaseModel


# =====================================================
# DATASET
# =====================================================

class LoadDatasetRequest(BaseModel):

    dataset_name: str


# =====================================================
# WINDOW CONFIGURATION
# =====================================================

class WindowConfigurationRequest(BaseModel):

    packet_number: int

    position: int

class RandomConfigurationRequest(BaseModel):

    count: int
# =====================================================
# CONFIGURATION
# =====================================================

class ConfigurationRequest(BaseModel):

    window_size: int

    dwt_level: int  

# =====================================================
# PREPROCESSING
# =====================================================

class RunPreprocessingRequest(BaseModel):

    pass


