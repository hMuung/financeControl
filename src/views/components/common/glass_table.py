# src/views/components/common/glass_table.py
import flet as ft
from views.components.common.glass_card import GlassCard
from views.utils.theme import HEADER_TEXT_COLOR


class GlassDataTable(GlassCard):
    """
    Tabla estilizada reutilizable sobre un GlassCard con ordenamiento integrado.
    
    :param columns_config: Lista de dicts con la configuración de columnas:
        [
            {"label": "Categoría", "key": "category", "numeric": False},
            {"label": "Monto", "key": "amount", "numeric": True},
        ]
    :param data: Lista de diccionarios con los datos a mostrar.
    :param empty_message: Mensaje cuando no hay registros.
    """

    def __init__(self, columns_config: list[dict], data: list[dict] = None, empty_message: str = "Sin datos registrados"):
        self.columns_config = columns_config
        self.raw_data = data or []
        self.empty_message = empty_message
        
        self.sort_column_index = None
        self.sort_ascending = True

        # Tabla Flet con estilos adaptados al Glass Theme
        self.table = ft.DataTable(
            columns=self._build_columns(),
            rows=self._build_rows(),
            heading_row_color=ft.Colors.with_opacity(0.12, ft.Colors.BLACK),
            heading_row_height=42,
            data_row_min_height=40,
            divider_thickness=0.5,
            column_spacing=18,
            horizontal_margin=12,
            border_radius=12,
        )

        # Contenedor con scroll horizontal para pantallas estrechas (Android)
        scrollable_table = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            controls=[
                ft.Row(
                    controls=[self.table],
                    scroll=ft.ScrollMode.AUTO,
                )
            ]
        )

        super().__init__(content=scrollable_table)

    def _build_columns(self) -> list[ft.DataColumn]:
        """Genera las columnas con eventos de ordenamiento."""
        cols = []
        for index, col in enumerate(self.columns_config):
            cols.append(
                ft.DataColumn(
                    label=ft.Text(
                        col["label"],
                        weight=ft.FontWeight.BOLD,
                        size=13,
                        color=HEADER_TEXT_COLOR,
                    ),
                    numeric=col.get("numeric", False),
                    on_sort=lambda e, col_idx=index: self._sort_data(col_idx),
                )
            )
        return cols

    def _build_rows(self) -> list[ft.DataRow]:
        """Genera las filas a partir de la lista de diccionarios."""
        if not self.raw_data:
            # Fila vacía cuando no hay datos
            return [
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(
                                self.empty_message,
                                color=ft.Colors.BLACK_54,
                                italic=True
                            )
                        )
                    ] + [ft.DataCell(ft.Text("")) for _ in range(len(self.columns_config) - 1)]
                )
            ]

        rows = []
        for item in self.raw_data:
            cells = []
            for col in self.columns_config:
                val = item.get(col["key"], "")
                
                # Formato visual del texto de las celdas
                text_val = f"${val:.2f}" if isinstance(val, (int, float)) and col.get("numeric") else str(val)
                
                cells.append(
                    ft.DataCell(
                        ft.Text(
                            text_val,
                            size=13,
                            color=HEADER_TEXT_COLOR,
                            weight=ft.FontWeight.W_500 if col.get("numeric") else ft.FontWeight.NORMAL,
                        )
                    )
                )
            rows.append(ft.DataRow(cells=cells))
        return rows

    def _sort_data(self, column_index: int):
        """Ordena la tabla alternando Ascendente / Descendente al hacer clic en la columna."""
        if self.sort_column_index == column_index:
            self.sort_ascending = not self.sort_ascending
        else:
            self.sort_column_index = column_index
            self.sort_ascending = True

        col_key = self.columns_config[column_index]["key"]

        # Ordenar lista internamente
        self.raw_data.sort(
            key=lambda x: (x.get(col_key) is None, x.get(col_key)),
            reverse=not self.sort_ascending,
        )

        # Actualizar estado de la tabla
        self.table.sort_column_index = column_index
        self.table.sort_ascending = self.sort_ascending
        self.table.rows = self._build_rows()
        self.update()

    def update_data(self, new_data: list[dict]):
        """Permite recargar los datos desde la vista exterior."""
        self.raw_data = new_data
        if self.sort_column_index is not None:
            self._sort_data(self.sort_column_index)
        else:
            self.table.rows = self._build_rows()
            self.update()