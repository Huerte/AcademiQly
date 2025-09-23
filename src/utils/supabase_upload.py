from datetime import timedelta
from utils.supabase_client import supabase

def upload_file(bucket: str, file_obj, file_name: str) -> str:
    path = f"{file_name}"

    file_obj.seek(0)

    supabase.storage.from_(bucket).upload(
        path,
        file_obj.read(),
        {"upsert": "true"}
    )

    public_url = supabase.storage.from_(bucket).get_public_url(path)
    return public_url
