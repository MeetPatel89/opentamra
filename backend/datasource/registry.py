from __future__ import annotations

from backend.datasource.base import BaseDataSource
from backend.datasource.local import LocalFileSystemSource
from backend.settings import Settings


def create_datasource(settings: Settings) -> BaseDataSource:
    ds_type = settings.datasource_type
    if ds_type == "local":
        return LocalFileSystemSource(base_dir=settings.paths_input_dir)
    elif ds_type == "azure":
        from backend.datasource.azure_datalake import AzureDataLakeSource
        return AzureDataLakeSource()
    elif ds_type == "sql":
        from backend.datasource.sql_database import SqlDatabaseSource
        return SqlDatabaseSource()
    else:
        raise ValueError(f"Unknown datasource type: {ds_type}")
