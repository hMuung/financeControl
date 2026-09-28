# src/views/components/incomes_record_table.py
from views.components.common.base_record_table import BaseRecordGlassTable


class IngresosGlassTable(BaseRecordGlassTable):

    def __init__(
        self,
        title: str = "Ingresos",
        detail_title: str = "Detalles del ingreso",
        edit_title: str = "Edición de ingreso",
        filter_title: str = "Filtrar Ingresos",
        columns_config: list[dict] = None,
        data: list[dict] = None,
        categories_options: list = None,
        origins_options: list = None,
        empty_message: str = "No hay ingresos que coincidan.",
        on_delete=None,
        on_edit=None,
    ):
        super().__init__(
            title=title,
            detail_title=detail_title,
            edit_title=edit_title,
            filter_title=filter_title,
            columns_config=columns_config,
            data=data,
            categories_options=categories_options,
            origins_options=origins_options,
            empty_message=empty_message,
            on_delete=on_delete,
            on_edit=on_edit,
        )