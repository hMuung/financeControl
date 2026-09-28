# src/views/components/expenses_record_table.py
from views.components.common.base_record_table import BaseRecordGlassTable


class GastosGlassTable(BaseRecordGlassTable):

    def __init__(
        self,
        title: str = "Gastos",
        detail_title: str = "Detalles del registro",
        edit_title: str = "Edición de registro",
        filter_title: str = "Filtrar",
        columns_config: list[dict] = None,
        data: list[dict] = None,
        categories_options: list = None,
        origins_options: list = None,
        empty_message: str = "No hay gastos que coincidan.",
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