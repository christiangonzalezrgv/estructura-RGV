// static/js/dynamic_table_init.js

document.addEventListener("alpine:init", () => {
    // Obtener el elemento que contiene la data
    const tableDataElement = document.getElementById("table-data");
    const tableName = tableDataElement ? tableDataElement.getAttribute("data-table") : "";
    // Leer el array de columnas (en formato JSON)
    const tableColumns = tableDataElement ? JSON.parse(tableDataElement.getAttribute("data-columns")) : [];

    // Inicializar el componente Alpine para la tabla de datos
    Alpine.data("tabla", () => {
        return createDataTable({
            apiEndpoint: `/db/${tableName}/datos`, // Asegúrate de que este endpoint esté implementado en Flask
            view: 50,
            offset: 5,
            defaultSortField: "fecha_creado",
            defaultSortRule: "desc",
            searchKeys: ["id", "descripcion", "estatus", "notas", "empleado_responsable"],
            // Pasar las columnas leídas para que el template las use al renderizar
            columns: tableColumns,
        });
    });
});

/**
 * Función para generar Excel a partir de la tabla actual.
 * Se debe implementar la lógica correspondiente en el backend.
 * @param {string} tableName - Nombre de la tabla.
 */
function generarExcel(tableName) {
    window.location.href = `/generar_excel?tabla=${tableName}`;
}
