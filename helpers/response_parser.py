from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status

from schemas import response_schema


def generate_response(
    status_code=status.HTTP_200_OK,
    message=None,
    data={},
    headers={},
    success=True,
    media_type="application/json",
):
    if status_code not in [200, 201, 202, 204]:
        return HTTPException(
            status_code=status_code,
            detail=jsonable_encoder(
                response_schema.ApiResponse(
                    status_code=status_code,
                    message=str(message),
                    data=data,
                    success=success,
                ).model_dump()
            ),
        )

    return JSONResponse(
        status_code=status_code,
        media_type=media_type,
        headers=headers,
        content=jsonable_encoder(
            response_schema.ApiResponse(
                status_code=status_code,
                message=str(message),
                data=data,
                success=success,
            ).model_dump()
        ),
    )
