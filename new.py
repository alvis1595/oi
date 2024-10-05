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


#######################################################################################################################################33
@cmdb.route('/cmdb/edit', methods=['POST'])
@require_api_key
def edit_record():
    try:
        errorcode = 0
        errormsg = ""
        data = request.get_json()

        # Obtención de los datos del request
        creador = data['creador'].replace('"', '')
        cr_id = data['cr_id']
        servidor = data['servidor']
        ip = data['ip']
        tipo_servidor = data['tipo_servidor']
        entorno_ci = data['entorno_ci']
        pais = data['pais']
        aplicacion = data['aplicacion']
        lenguaje = data['lenguaje']
        proveedor = data['proveedor']
        desarrollo = data['desarrollo']
        responsable = data['responsable']
        rep = data['rep']
        alojamiento = data['alojamiento']
        esquema_de_continuidad = data['esquema_de_continuidad']
        estrategias_de_recuperacion_infra = data['estrategias_de_recuperacion_infra']
        estrategias_de_recuperacion_datos = data['estrategias_de_recuperacion_datos']
        tiempo_de_instalacion_servidor = data['tiempo_de_instalacion_servidor']
        tiempo_de_instalacion_aplicacion = data['tiempo_de_instalacion_aplicacion']
        joya_de_la_corona = data['joya_de_la_corona']
        
        # Lógica para autenticación LDAP o validación de grupos
        user_groups = ldap_login(creador, data['upwd'].replace('"', ''))

        connection = psycopg2.connect(user=db_User,
                                      password=db_Pass,
                                      host=db_Host,
                                      port=db_Port,
                                      database="cmdb_integracion")
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        # Validar usuario que edita
        cursor.execute(f"SELECT cr_creador FROM cis_registros WHERE cr_id = %s", (cr_id,))
        result = cursor.fetchone()
        var = False

        for group in user_groups:
            if 'ccyl' in group:
                var = True
                break

        if not var and creador not in result.values():
            errorcode = 1
            raise Exception("No puede modificar este registro!")

        # Llamada a la función almacenada de PostgreSQL
        sql = """
            CALL update_cis_registros(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(sql, (
            cr_id, servidor, ip, tipo_servidor, entorno_ci, pais, aplicacion, lenguaje, proveedor,
            desarrollo, responsable, rep, alojamiento, esquema_de_continuidad,
            estrategias_de_recuperacion_infra, estrategias_de_recuperacion_datos,
            tiempo_de_instalacion_servidor, tiempo_de_instalacion_aplicacion, joya_de_la_corona
        ))
        connection.commit()

    except (Exception, Error) as e:
        if errorcode == 1:
            errormsg = jsonify("ERROR: No puede modificar este registro!")
            print(f"ERROR: {e}")
        else:
            logging.error(f"[ERROR]: Algo ha salido mal al intentar guardar. {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

    if errorcode != 0:
        return (errormsg)
    else:
        return jsonify("Se editó el registro correctamente!")

