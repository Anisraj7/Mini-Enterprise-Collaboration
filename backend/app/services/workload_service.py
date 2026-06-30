from datetime import datetime

from app.repository.team_repository import (
    TeamRepository
)

from app.repository.team_member_repository import (
    TeamMemberRepository
)

from app.repository.task_repository import (
    TaskRepository
)

from app.repository.project_repository import (
    ProjectRepository
)

from app.repository.task_repository import (
    TaskRepository
)

class WorkloadService:

    @staticmethod
    def get_team_workload(
        db,
        organization_id: int,
        team_id: int
    ):

        team = TeamRepository.get_by_id(
            db,
            team_id,
            organization_id
        )

        if not team:
            raise ValueError(
                "Team not found"
            )

        members = (
            TeamMemberRepository
            .get_team_members(
                db,
                team_id
            )
        )

        tasks = (
            TaskRepository.get_by_team(
                db,
                team_id
            )
        )

        total_tasks = len(tasks)

        completed_tasks = len(
            [
                task
                for task in tasks
                if task.status == "COMPLETED"
            ]
        )

        pending_tasks = len(
            [
                task
                for task in tasks
                if task.status != "COMPLETED"
            ]
        )

        overdue_tasks = len(
            [
                task
                for task in tasks
                if (
                    task.due_date
                    and task.due_date < datetime.utcnow()
                    and task.status != "COMPLETED"
                )
            ]
        )

        user_workload = []

        for member in members:

            user_tasks = [
                task
                for task in tasks
                if task.assigned_to == member.user_id
            ]

            user_workload.append(
                {
                    "user_id": member.user_id,
                    "total_tasks": len(user_tasks),
                    "completed_tasks": len(
                        [
                            t
                            for t in user_tasks
                            if t.status == "COMPLETED"
                        ]
                    ),
                    "pending_tasks": len(
                        [
                            t
                            for t in user_tasks
                            if t.status != "COMPLETED"
                        ]
                    )
                }
            )

        return {
            "team_id": team.id,
            "team_name": team.name,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "overdue_tasks": overdue_tasks,
            "member_count": len(members),
            "user_workload": user_workload
        }

    @staticmethod
    def get_project_workload(
        db,
        organization_id: int,
        project_id: int
    ):

        project = ProjectRepository.get_by_id(
            db,
            project_id,
            organization_id
        )

        if not project:
            raise ValueError(
                "Project not found"
            )

        tasks = TaskRepository.get_by_project(
            db,
            organization_id,
            project_id
        )

        total_tasks = len(tasks)

        completed_tasks = len(
            [
                task
                for task in tasks
                if task.status == "COMPLETED"
            ]
        )

        pending_tasks = len(
            [
                task
                for task in tasks
                if task.status != "COMPLETED"
            ]
        )

        workload_by_team = {}

        for task in tasks:

            if not task.team_id:
                continue

            workload_by_team.setdefault(
                task.team_id,
                0
            )

            workload_by_team[
                task.team_id
            ] += 1

        return {
            "project_id": project.id,
            "project_name": project.name,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "workload_by_team": workload_by_team
        }