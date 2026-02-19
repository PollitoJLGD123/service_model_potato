from fastapi import APIRouter
from src.controllers.auth import router as auth_router
from src.controllers.evaluation import router as evaluation_router
from src.controllers.train import router as train_router

router = APIRouter()

router.include_router(auth_router, tags=["auth"])
router.include_router(evaluation_router,prefix="/evaluation", tags=["evaluation"])
router.include_router(train_router,prefix="/train", tags=["train"])