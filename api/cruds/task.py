from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result, result

import api.models.task as task_model
import api.schemas.task as task_schema

from typing import List, Tuple, Optional


# task_idでtaskが存在しているかのチェック
async def get_task(db: AsyncSession, task_id: int) -> Optional[task_model.Task]:
    result: Result = await db.execute(
        select(task_model.Task).filter(task_model.Task.id == task_id)
    )
    task: Optional[Tuple[task_model.task]] = result.first()
    # 要素が一つであってもTupleで返ってくるので、１つ目の要素を取り出す
    return task[0] if task is not None else None


# Create
async def create_task(db: AsyncSession, task_create: task_schema.TaskCreate) -> task_model.Task:
    task = task_model.Task(**task_create.dict())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


# Read
async def get_tasks_with_done(db: AsyncSession) -> List[Tuple[int, str, bool]]:
    result: Result = await(
        db.execute(
            select(
                task_model.Task.id,
                task_model.Task.title,
                task_model.Done.id.isnot(None).label('done')
            ).outerjoin(task_model.Done)
        )
    )
    return result.all()


# Update
# チェックで存在した場合は更新、存在しない場合は404エラー
async def update_task(
    db: AsyncSession, task_create: task_schema.TaskCreate, original: task_model.Task
) -> task_model.Task:
    original.title = task_create.title
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original


# Delete
# チェックで存在した場合は削除、存在しない場合は404エラー
async def delete_task(db: AsyncSession, original: task_model.Task) -> None:
    await db.delete(original)
    await db.commit()

