# Protected Route Template
# Copy to app/routes/resource_name.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, list

from app.database import get_db
from app.models.resource import Resource
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/api/resources", tags=["resources"])


@router.get("/", response_model=list[dict])
async def get_resources(
    search: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all resources for the authenticated user.
    """
    query = db.query(Resource).filter(Resource.user_id == current_user_id)

    if search:
        query = query.filter(Resource.name.ilike(f"%{search}%"))

    offset = (page - 1) * limit
    resources = query.order_by(Resource.created_at.desc()).offset(offset).limit(limit).all()

    return [r.to_dict() for r in resources]


@router.get("/{resource_id}", response_model=dict)
async def get_resource(
    resource_id: str,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific resource by ID.
    Returns 404 if not found or not owned by user.
    """
    resource = db.query(Resource).filter(
        Resource.id == resource_id,
        Resource.user_id == current_user_id  # CRITICAL: User isolation
    ).first()

    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    return resource.to_dict()


@router.post("/", response_model=dict, status_code=201)
async def create_resource(
    resource_data: dict,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new resource.
    Automatically assigned to the authenticated user.
    """
    resource = Resource(
        **resource_data,
        user_id=current_user_id  # Assign to authenticated user
    )
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource.to_dict()


@router.put("/{resource_id}", response_model=dict)
async def update_resource(
    resource_id: str,
    resource_update: dict,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a resource.
    Only allows updating resources belonging to the authenticated user.
    """
    resource = db.query(Resource).filter(
        Resource.id == resource_id,
        Resource.user_id == current_user_id  # CRITICAL
    ).first()

    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    for field, value in resource_update.items():
        setattr(resource, field, value)

    db.commit()
    db.refresh(resource)
    return resource.to_dict()


@router.delete("/{resource_id}", status_code=204)
async def delete_resource(
    resource_id: str,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a resource.
    Only allows deleting resources belonging to the authenticated user.
    """
    resource = db.query(Resource).filter(
        Resource.id == resource_id,
        Resource.user_id == current_user_id  # CRITICAL
    ).first()

    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    db.delete(resource)
    db.commit()
    return None
