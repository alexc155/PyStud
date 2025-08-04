from pydantic import BaseModel


class ProjectImport(BaseModel):
    project_name: str
    project_file: str
