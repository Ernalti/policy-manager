from fastapi import APIRouter, HTTPException, Depends
from pydantic import ValidationError
from app.utils.dto import PolicyDto
from app.service.policy_service import PolicyService
from typing import List

# Инициализация роутера
router = APIRouter()

# Инициализация сервиса
policy_service = PolicyService()

@router.get("/policies", response_model=List[PolicyDto])
async def get_policies():
    """Получить список политик"""
    try:
        policies = await policy_service.get_all_policies()
        return policies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/policies", response_model=PolicyDto, status_code=201)
async def create_policy(data: PolicyDto):
    """Создать новую политику"""
    try:
        policy = await policy_service.create_policy(data)
        return policy
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/policies/{id}", response_model=PolicyDto)
async def get_policy(id: int):
    """Получить политику по ID"""
    try:
        policy = await policy_service.get_policy_by_id(id)
        if policy:
            return policy
        else:
            raise HTTPException(status_code=404, detail="Policy not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/policies/{id}", response_model=PolicyDto)
async def update_policy(id: int, data: PolicyDto):
    """Обновить существующую политику"""
    try:
        updated_policy = await policy_service.update_policy(id, data)
        if updated_policy:
            return updated_policy
        else:
            raise HTTPException(status_code=404, detail="Policy not found")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/policies/{id}", status_code=200)
async def delete_policy(id: int):
    """Удалить политику по ID"""
    try:
        success = await policy_service.delete_policy(id)
        if success:
            return {"message": "Policy deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Policy not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/policies/{policy_id}/validate", status_code=200)
async def validate_policy_text(policy_id: int, text: str):
    """Валидация текста политики"""
    try:
        if not text:
            raise HTTPException(status_code=400, detail="Text is required")

        result = await policy_service.validate_policy_text_for_id(policy_id, text)
        if result:
            return {"message": "Validation successful"}
        else:
            raise HTTPException(status_code=400, detail="Text does not match the first letter of the policy text")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
