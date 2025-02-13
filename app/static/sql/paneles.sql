WITH total_registros AS (
    SELECT 
        COUNT(*) AS registros_totales
    FROM nombre_app_prueba
),
numero_mayor AS (
    SELECT 
        MAX(numero) AS max_number
    FROM nombre_app_prueba
),
numero_menor AS (
    SELECT 
        MIN(numero) AS min_number
    FROM nombre_app_prueba
)
SELECT 
    registros_totales,
    max_number,
    min_number
FROM 
    total_registros registros_totales, 
    numero_mayor max_number, 
    numero_menor min_number;