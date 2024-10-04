CREATE OR REPLACE FUNCTION remove_catalog_item(
    catalog_name TEXT,
    id INT  -- Cambia el tipo de dato a INT para el ID
) RETURNS TEXT AS $$
DECLARE
    table_name TEXT;
    column_id TEXT;
    exists_count INT;
BEGIN
    -- Mapeo de catálogos a tablas y columnas de ID
    IF catalog_name = 'Alojamiento' THEN
        table_name := 'cis_alojamiento';
        column_id := 'ca_id';
    ELSIF catalog_name = 'Desarrollo' THEN
        table_name := 'cis_desarrollo';
        column_id := 'cd_id';
    ELSIF catalog_name = 'Entorno' THEN
        table_name := 'cis_entorno_ci';
        column_id := 'cec_id';
    ELSIF catalog_name = 'Lenguaje' THEN
        table_name := 'cis_lenguaje';
        column_id := 'cl_id';
    ELSIF catalog_name = 'Aplicacion' THEN
        table_name := 'cis_nombre_aplicacion';
        column_id := 'cna_id';
    ELSIF catalog_name = 'Pais' THEN
        table_name := 'cis_pais_servidor';
        column_id := 'cps_id';
    ELSIF catalog_name = 'Proveedor' THEN
        table_name := 'cis_proveedor';
        column_id := 'cp_id';
    ELSIF catalog_name = 'Responsable' THEN
        table_name := 'cis_responsable_aplicacion';
        column_id := 'cra_id';
    ELSIF catalog_name = 'Tipo Servidor' THEN
        table_name := 'cis_tipo_servidor';
        column_id := 'cts_id';
    ELSIF catalog_name = 'Esquema de Continuidad' THEN
        table_name := 'cis_esquema';
        column_id := 'ce_id';
    ELSIF catalog_name = 'Estrategias de Recuperación Infra' THEN
        table_name := 'cis_estrategias_infra';
        column_id := 'cei_id';
    ELSIF catalog_name = 'Estrategias de Recuperación Datos' THEN
        table_name := 'cis_estrategias_datos';
        column_id := 'ced_id';
    ELSIF catalog_name = 'Tiempo de Instalación (Servidor)' THEN
        table_name := 'cis_tiempo_infra_servidor';
        column_id := 'ctis_id';
    ELSIF catalog_name = 'Tiempo de Instalación (Aplicación)' THEN
        table_name := 'cis_tiempo_infra_aplicacion';
        column_id := 'ctia_id';
    ELSIF catalog_name = 'Joya de la Corona' THEN
        table_name := 'cis_joya';
        column_id := 'cj_id';
    ELSE
        RETURN 'ERROR: Catálogo no reconocido.';
    END IF;

    -- Verifica si el ID existe en la tabla
    EXECUTE FORMAT('SELECT COUNT(*) FROM %I WHERE %I = $1', table_name, column_id)
    INTO exists_count USING id;

    IF exists_count = 0 THEN
        RETURN 'ERROR: El ID no existe en el catálogo.';
    END IF;

    -- Elimina el registro
    EXECUTE FORMAT('DELETE FROM %I WHERE %I = $1', table_name, column_id) USING id;

    RETURN 'Se eliminó el registro correctamente!';
END;
$$ LANGUAGE plpgsql;
