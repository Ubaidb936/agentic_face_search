import logging
from io import BytesIO
from pydantic import BaseModel
from starlette.datastructures import UploadFile as StarletteUploadFile
from fastapi import APIRouter, HTTPException, UploadFile, File, Query, Path


from app.utils.schema import Image
from app.llm_service.openai_client import openai_client
from app.storage_service.superbase_client import superbase_client
from app.face_search_service.inhouse_client import inhouse_face_search_client

logger = logging.getLogger(__name__)

class ParsedResponse(BaseModel):
    answer: str

router = APIRouter()

@router.post("/upload/{user_id}")
async def upload(
    user_id: str = Path(...),
    file: UploadFile = File(...),
    conversation: str = Query(...)
):
    try:
        contents = await file.read()  
        superbase_client.upload_file("images", file_bytes=contents, file_path=f"{user_id}/{file.filename}")
        image = Image(
            user_id=user_id,
            conversation=conversation,
            photo_id=file.filename
        )
        superbase_client.put("images", image.model_dump(exclude_none=True))
        await file.seek(0)
        await inhouse_face_search_client.upload(user_id, file)
    except Exception as e:
        logger.exception("Upload failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/search/{user_id}")
async def search(user_id: str = Path(...), file: UploadFile = File(...)):
    try:
        contents = await file.read()
        file_for_search = StarletteUploadFile(
            filename=file.filename,
            file=BytesIO(contents),
            headers=file.headers,
        )
        photo_ids: list[str] = await inhouse_face_search_client.search(user_id, file_for_search)


        superbase_client.upload_file("searches", file_bytes=contents, file_path=f"{user_id}/{file.filename}")
        search_image_url = superbase_client.get_file_url("searches", f"{user_id}/{file.filename}")["signedUrl"]
        
        image_objs: list[Image] = []
        for photo_id in photo_ids:
            result = superbase_client.get("images", "user_id", user_id, "photo_id", photo_id).data
            if result and len(result) > 0:
                image_objs.append(Image(**result[0]))

        prompt = """
        You are a fun, warm narrator for a personal photo memory app — think nostalgic TV host meets a close friend.
        Your job is to identify who is on screen by visually comparing their face to the reference faces that follow.
        CRITICAL: You must only name someone if their face is a strong visual match to a reference face — same facial features, structure, and appearance.
        Do NOT rely solely on memory notes to assign a name. The notes describe who is in each reference, but the reference may not contain the person on screen.
        If the face on screen does not closely match any reference face, say you don't recognise them yet — do not guess or assign a name from unrelated references.
        When you do find a match, always use the person's name from their memory note.
        Speak naturally to the user as if describing what they are looking at right now — never reference any image, photo, picture, or visual.
        Never say "in this image", "in the first image", "in the photo", "pictured", or anything that draws attention to the medium.
        Just talk about the person directly, as if they are right there.
        Keep it to 1-3 sentences. Be specific, warm, and a little playful.
        Never use words like "context", "metadata", "reference", or "based on".
        If you cannot identify anyone, say so in a fun, encouraging way without mentioning images or photos.
        """
        content = [
            {"type": "input_image", "image_url": search_image_url},
            {"type": "input_text", "text": prompt},
        ]

        for image_obj in image_objs:
            image_url = superbase_client.get_file_url("images", f"{user_id}/{image_obj.photo_id}")["signedUrl"]
            content.append({"type": "input_image", "image_url": image_url})
            content.append({"type": "input_text", "text": f"Memory note: {image_obj.conversation}"})


        response = await openai_client.parse(
            llm_input=[{"role": "user","content": content}],
            response_format=ParsedResponse,
            temperature=0.1
        )
        logger.info("Search answer: %s", response.answer)
        return response
    except Exception as e:
        logger.exception("Face search failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

