from fastapi import FastAPI, Request

from common.auth import CurrentUser, decode_jwt
from context_vars import user_context
from common.logger import logger

def create_middlewares(app: FastAPI):
    @app.middleware("http")
    def get_current_user_middleware(request: Request, call_next):
        authorization = request.headers.get("Authorization")
        if authorization:
            splits = authorization.split(" ")
            if splits[0] == "Bearer":
                token = splits[1]
                payload = decode_jwt(token)
                user_id = payload.get("user_id")
                user_role = payload.get("user_role")
                user_context.set(CurrentUser(user_id, user_role))
                print("[debug] user_context:", user_context.get())

        logger.info(request.url)
        response = call_next(request)

        return response