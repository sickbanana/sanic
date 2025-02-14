from sanic import Sanic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
import settings

from api import users_blueprint, admin_blueprint

app = Sanic(__name__)

bind = create_async_engine(f"postgresql+asyncpg://postgres:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}/postgres", echo=True)
_sessionmaker = sessionmaker(
    bind, class_=AsyncSession, expire_on_commit=False
)

app.blueprint(users_blueprint)
app.blueprint(admin_blueprint)


@app.middleware("request")
async def inject_session(request):
    request.ctx.session = _sessionmaker()


@app.listener('before_server_stop')
async def disconnect_db(app, loop):
    await bind.dispose()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)


