import json
from aiohttp import web
from db import engine, Base, Session, User, Advertisement
from sqlalchemy.exc import IntegrityError
from bcrypt import hashpw, gensalt, checkpw
from schema import validate_create_advertisement, validate_create_user
from sqlalchemy.future import select

app = web.Application()


async def orm_context(app: web.Application):
    print("Start")
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        # await conn.commit()
        await conn.run_sync(Base.metadata.create_all)

    yield
    await engine.dispose()
    print("Stop")


# функция будет выполняться при каждом запросе
@web.middleware
async def session_midleware(request: web.Request, handler):
    async with Session() as session:
        request["session"] = session
        return await handler(request)


app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_midleware)


async def test(request: web.Request):
    json_data = await request.json()
    headers = request.headers
    qs = request.query
    print(f"{json_data=}")
    print(f"{headers=}")
    print(f"{qs=}")
    return web.json_response({"hello": "world"})


async def get_user(user_id: int, session: Session):
    user = await session.get(User, user_id)

    if user is None:
        raise web.HTTPNotFound(
            text=json.dumps({"status": "error", "message": "user not found"}),
            content_type="application/json",
        )
    return user


async def get_adv(adv_id: int, session: Session):
    adv = await session.get(Advertisement, adv_id)
    if adv is None:
        raise web.HTTPNotFound(
            text=json.dumps({"status": "error", "message": "Post not found"}),
            content_type="application/json",
        )
    return adv


def hash_password(password: str):
    password = password.encode()
    password = hashpw(password, salt=gensalt())
    return password.decode()


class UserView(web.View):
    async def get(self):
        session = self.request["session"]

        if self.request.match_info.get("user_id") is None:
            q = select(User)
            result = await session.execute(q)
            users = result.scalars()
            return web.json_response({
                "users": [
                    {"id": u.id,
                     "name": u.username,
                     "creation_time": u.creation_time.isoformat()} for u in users]
            })
        else:
            user_id = int(self.request.match_info["user_id"])
            user = await get_user(user_id, session)
            return web.json_response(
                {
                    "id": user.id,
                    "name": user.username,
                    "creation_time": user.creation_time.isoformat(),
                }
            )

    async def post(self):
        session = self.request["session"]
        json_data = await self.request.json()
        json_data = validate_create_user(json_data)
        json_data["password"] = hash_password(json_data["password"])
        user = User(**json_data)
        session.add(user)
        try:
            await session.commit()
        except IntegrityError as er:
            raise web.HTTPConflict(
                text=json.dumps({"status": "error", "message": "user already exist"}),
                content_type="application/json",
            )
        return web.json_response({"id": user.id})

    async def patch(self):
        session = self.request["session"]
        user_id = int(self.request.match_info["user_id"])
        user = await get_user(user_id, session)
        json_data = await self.request.json()
        if "password" in json_data:
            json_data["password"] = hash_password(json_data["password"])
        for field, value in json_data.items():
            setattr(user, field, value)
        self.request["session"].add(user)
        await self.request["session"].commit()
        return web.json_response({"status": "success"})

    async def delete(self):
        session = self.request["session"]
        user_id = int(self.request.match_info["user_id"])
        user = await get_user(user_id, session)
        await self.request["session"].delete(user)
        await self.request["session"].commit()
        return web.json_response({"status": "success"})


class AdvView(web.View):

    async def post(self):
        session = self.request["session"]
        json_data = await self.request.json()
        json_data = validate_create_advertisement(json_data)
        adv = Advertisement(**json_data)
        session.add(adv)
        try:
            await session.commit()
        except IntegrityError as er:
            raise web.HTTPConflict(
                text=json.dumps({"status": "error", "message": "user already exist"}),
                content_type="application/json",
            )
        return web.json_response({"id": adv.id, 'title': adv.title})

    async def patch(self):
        session = self.request["session"]
        adv_id = int(self.request.match_info["adv_id"])
        adv = await get_adv(adv_id, session)
        json_data = await self.request.json()
        for field, value in json_data.items():
            setattr(adv, field, value)
        self.request["session"].add(adv)
        try:
            await session.commit()
        except IntegrityError as er:
            raise web.HTTPConflict(
                text=json.dumps({"status": "error", "message": "user not exist"}),
                content_type="application/json",
            )
        return web.json_response({"status": "success"})

    async def delete(self):
        session = self.request["session"]
        adv_id = int(self.request.match_info["adv_id"])
        adv = await get_adv(adv_id, session)
        await self.request["session"].delete(adv)
        await self.request["session"].commit()
        return web.json_response({"status": "success"})

    async def get(self):
        session = self.request["session"]
        adv_id = int(self.request.match_info["adv_id"])
        adv = await get_adv(adv_id, session)
        return web.json_response(
            {
                "id": adv.id,
                "title": adv.title,
                "creation_time": adv.creation_time.isoformat(),
                'autor': adv.user.username
            }
        )


app.add_routes(
    [
        web.post("/test/", test),

        web.get("/users/{user_id:\d+}/", UserView),
        web.get("/users/", UserView),

        web.post("/users/", UserView),
        web.patch("/users/{user_id:\d+}/", UserView),
        web.delete("/users/{user_id:\d+}/", UserView),

        web.get("/adv/{adv_id:\d+}/", AdvView),
        web.post("/adv/", AdvView),
        web.patch("/adv/{adv_id:\d+}/", AdvView),
        web.delete("/adv/{adv_id:\d+}/", AdvView)
    ]
)

if __name__ == "__main__":
    web.run_app(app)
