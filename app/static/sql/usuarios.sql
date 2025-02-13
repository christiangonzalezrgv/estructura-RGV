WITH fecha AS (
    SELECT 
        date_joined
    FROM auth_user
),
id_user AS (
    SELECT 
        id
    FROM auth_user
)
SELECT 
    date_joined,
    id
FROM 
    fecha fecha_creado, 
    id_user id;