SELECT 
    TO_CHAR(fecha_hoy::DATE, 'YYYY-MM-DD') AS date,
    sum(numero) as total
FROM nombre_app_prueba
where numero is not null
