from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status

from database.engine import SessionDep
from schemas import user_schema
from services import user_service
from helpers import response_parser, chatbot_config

router = APIRouter()


@router.get("/")
async def get_users(db: SessionDep):
    users_list = user_service.get_users_list(db=db)

    if not users_list:
        raise response_parser.generate_response(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Users not found",
            success=False,
        )

    return response_parser.generate_response(
        status_code=status.HTTP_200_OK,
        message="User's list",
        data=[user_schema.UserResponse.model_validate(user) for user in users_list],
    )


@router.get("/{user_id}")
async def get_users_by_id(db: SessionDep, user_id: int):
    existing_user = user_service.get_users_by_id(db=db, user_id=user_id)

    if not existing_user:
        raise response_parser.generate_response(
            status_code=status.HTTP_404_NOT_FOUND,
            message="User not found",
            success=False,
        )

    return response_parser.generate_response(
        status_code=status.HTTP_200_OK,
        message="User",
        data=user_schema.UserResponse.model_validate(existing_user).model_dump(),
    )


@router.post("/")
async def create_new_users(db: SessionDep, payload: user_schema.UserCreate):
    existing_email = user_service.get_users_by_email(db=db, user_email=payload.email)

    if existing_email:
        raise response_parser.generate_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Email already exists",
            success=False,
        )

    new_user = user_service.create_new_users(db=db, payload=payload)

    return response_parser.generate_response(
        status_code=status.HTTP_200_OK,
        message="User",
        data=user_schema.UserResponse.model_validate(new_user).model_dump(),
    )


@router.put("/{user_id}")
async def update_users(db: SessionDep, user_id: int, payload: user_schema.UserUpdate):
    if payload.email:
        existing_email = user_service.get_users_by_email(
            db=db, user_email=payload.email
        )

        if existing_email:
            raise response_parser.generate_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Email already exists",
                success=False,
            )

    user_service.update_users(db=db, user_id=user_id, payload=payload)

    return response_parser.generate_response(
        status_code=status.HTTP_202_ACCEPTED, message="User updated successfully"
    )


@router.delete("/{user_id}")
async def delete_users(db: SessionDep, user_id: int):
    existing_user = user_service.get_users_by_id(db=db, user_id=user_id)

    if not existing_user:
        raise response_parser.generate_response(
            status_code=status.HTTP_404_NOT_FOUND,
            message="User not found",
            success=False,
        )

    user_service.delete_users(db=db, user_id=user_id)

    return response_parser.generate_response(
        status_code=status.HTTP_200_OK, message="User deleted successfully"
    )


@router.websocket("/{user_id}/chat")
async def chatbot(db: SessionDep, user_id: int, websocket: WebSocket):
    try:
        existing_user = user_service.get_users_by_id(db=db, user_id=user_id)

        if not existing_user:
            await websocket.send_text("User not found")
            await websocket.close()
            return

        await websocket.accept()

        while True:
            message = await websocket.receive_text()

            response = chatbot_config.llm.invoke(message)

            await websocket.send_text(response.content)

            user_service.save_users_chat(
                db=db, user_id=user_id, message=message, response=response.content
            )

    except RuntimeError:
        raise response_parser.generate_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Disconnected",
            success=False,
        )

    except WebSocketDisconnect:
        raise response_parser.generate_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Disconnected",
            success=False,
        )

    finally:
        await websocket.close()
