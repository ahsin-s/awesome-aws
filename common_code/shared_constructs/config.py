import pydantic

def clean_object_name(object_name: str):
    object_name = object_name.strip("/")
    return object_name

class LambdaBatchS3SolutionConfig:
    RAW_FILE_UPLOAD_PREFIX = "uploads"
    PREPROCESSED_PREFIX = "preprocessed"
    INFERENCE_PREFIX = "inference"

    JOB_METADATA_TABLE = 'batch-jobs-metadata'

    AUDIO_PREFIXES = ["mp3", "wav", "m4a", "mpeg", "mov"]


    @classmethod
    def get_raw_file_upload_path(cls, user_id: str, object_name: str):
        object_name = clean_object_name(object_name)
        return f"{cls.RAW_FILE_UPLOAD_PREFIX}/user={user_id}/{object_name}"

    @classmethod
    def get_preprocessed_path(cls, user_id: str, job_id: str, object_name: str):
        object_name = clean_object_name(object_name)
        return f"{cls.PREPROCESSED_PREFIX}/user={user_id}/job_id={job_id}/{object_name}"

    @classmethod
    def get_inference_path(cls, user_id: str, job_id: str, object_name: str):
        object_name = clean_object_name(object_name)
        return f"{cls.INFERENCE_PREFIX}/user={user_id}/job_id={job_id}/{object_name}/inference.txt"

