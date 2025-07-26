from supabase import create_client
import os
import requests
from dotenv import load_dotenv
load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_BUCKET = "book-covers"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def upload_to_supabase(file):
    file_path = f"book-covers/{file.name}"
    file_content = file.read()  
    file_options = {"content-type": file.content_type}

    response = supabase.storage.from_("book-covers").upload(file_path, file_content, file_options)

    if response:
        return f"{SUPABASE_URL}/storage/v1/object/public/book-covers/{file.name}"
    else:
        raise Exception("Upload failed")