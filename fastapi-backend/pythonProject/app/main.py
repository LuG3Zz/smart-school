from fastapi import FastAPI
from aioredis import create_redis_pool, Redis
# from app.routers import usersRouter
# from app.routers import courseRouter
from app.api.app_v1.endpoints.course import *
from app.api.app_v1.endpoints.dormitory import dormitoryRouter, student_dormitoryRouter
from app.api.app_v1.endpoints.image import ImageRouter
from app.api.app_v1.endpoints.leave_school import LeaveSchoolRouter
from app.api.app_v1.endpoints.notification import NotificationRouter
from app.api.app_v1.endpoints.student_record import StudentRecordRouter
from app.api.app_v1.endpoints.studentdiscipline import *
from app.api.app_v1.endpoints.department import departmentRouter
from app.api.app_v1.endpoints.student import studentRouter
from app.api.app_v1.endpoints.student_course import studentCourseRouter
from app.api.app_v1.endpoints.user import *
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.util.config import *
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles

app = FastAPI()


#
# # 前端页面url
# origins = [
#     "http://localhost.tiangolo.com",
#     "http://localhost:8080",
#     "http://192.168.31.35",
# ]
#
# # 后台api允许跨域
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

async def get_redis_pool() -> Redis:
    if EVENT == "test":
        redis = await create_redis_pool(
            f"redis://:@" + testredishost + ":" + testredisport + "/" + testredisdb + "?encoding=utf-8")
    else:
        redis = await create_redis_pool(f"redis://:@" + redishost + ":" + redisport + "/" + redisdb + "?encoding=utf-8")

    return redis


@app.on_event("startup")
async def startup_event():
    app.state.redis = await get_redis_pool()


@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()
    await app.state.redis.wait_closed()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        content=jsonable_encoder({"message": exc.errors(), "code": 421}),
    )


app.include_router(usersRouter, prefix="/user", tags=['users'])
app.include_router(courseRouter, prefix='/course', tags=['course'])
app.include_router(studentRouter, prefix='/student', tags=['student'])
app.include_router(departmentRouter, prefix='/department', tags=['department'])
app.include_router(studentCourseRouter, prefix='/student_course', tags=['studentCourse'])
app.include_router(DisciplineRouter, prefix='/discipline', tags=['discipline'])
app.include_router(StudentRecordRouter, prefix='/record', tags=['record'])
app.include_router(ImageRouter, prefix='/image', tags=['image'])
app.include_router(NotificationRouter, prefix='/notification', tags=['notification'])
app.include_router(LeaveSchoolRouter, prefix='/LeaveSchool', tags=['LeaveSchool'])
app.include_router(dormitoryRouter, prefix='/dormitory', tags=['dormitory'])
app.include_router(student_dormitoryRouter, prefix='/student_dormitory', tags=['student_dormitory'])


app.mount("/public", StaticFiles(directory="../public"), name="public")
if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app='main:app', host="127.0.0.1", port=8000, reload=True, debug=True)
