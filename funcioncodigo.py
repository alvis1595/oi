CREATE OR REPLACE FUNCTION actualizar_cis_registro(
    p_cr_id INT,
    p_servidor TEXT,
    p_ip TEXT,
    p_tipo_servidor TEXT,
    p_entorno_ci TEXT,
    p_pais TEXT,
    p_aplicacion TEXT,
    p_lenguaje TEXT,
    p_proveedor TEXT,
    p_desarrollo TEXT,
    p_responsable TEXT,
    p_rep TEXT,
    p_alojamiento TEXT,
    p_esquema_de_continuidad TEXT,
    p_estrategias_de_recuperacion_infra TEXT,
    p_estrategias_de_recuperacion_datos TEXT,
    p_tiempo_de_instalacion_servidor TEXT,
    p_tiempo_de_instalacion_aplicacion TEXT,
    p_joya_de_la_corona TEXT
)
RETURNS VOID AS $$
BEGIN
    UPDATE cis_registros
    SET cr_servidor = p_servidor,
        cr_direccion_ip = p_ip,
        cr_tipo_servidor = p_tipo_servidor,
        cr_entorno_ci = p_entorno_ci,
        cr_pais = p_pais,
        cr_aplicacion = p_aplicacion,
        cr_lenguaje = p_lenguaje,
        cr_proveedor = p_proveedor,
        cr_desarrollo = p_desarrollo,
        cr_mesa_responsable = p_responsable,
        cr_rep = p_rep,
        cr_alojamiento = p_alojamiento,
        cr_esquema_de_continuidad = p_esquema_de_continuidad,
        cr_estrategias_de_recuperacion_infra = p_estrategias_de_recuperacion_infra,
        cr_estrategias_de_recuperacion_datos = p_estrategias_de_recuperacion_datos,
        cr_tiempo_de_instalacion_servidor = p_tiempo_de_instalacion_servidor,
        cr_tiempo_de_instalacion_aplicacion = p_tiempo_de_instalacion_aplicacion,
        cr_joya_de_la_corona = p_joya_de_la_corona
    WHERE cr_id = p_cr_id;
END;
$$ LANGUAGE plpgsql;
###########################################################################################################################

@cmdb.route('/cmdb/edit', methods=['POST'])
@require_api_key
def edit_record():
    try:
        errorcode = 0
        errormsg = ""
        data = request.get_json()
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
        user_groups = ldap_login(creador, data['upwd'].replace('"',''))

        connection = psycopg2.connect(user=db_User,
                                      password=db_Pass,
                                      host=db_Host,
                                      port=db_Port,
                                      database="cmdb_integracion")
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        # Validar usuario que edita
        cursor.execute(
            f"SELECT cr_creador FROM cis_registros WHERE cr_id = {cr_id}")
        result = cursor.fetchone()
        var = False
        for group in user_groups:
            if 'ccyl' in group:
                print('parte del grupo')
                var = True
                break
        if var == False:
            if creador not in result.values():
                errorcode = 1
                raise Exception

        # Llamar a la función almacenada en la base de datos
        cursor.callproc('actualizar_cis_registro', [
            cr_id, servidor, ip, tipo_servidor, entorno_ci, pais, aplicacion,
            lenguaje, proveedor, desarrollo, responsable, rep, alojamiento,
            esquema_de_continuidad, estrategias_de_recuperacion_infra,
            estrategias_de_recuperacion_datos, tiempo_de_instalacion_servidor,
            tiempo_de_instalacion_aplicacion, joya_de_la_corona
        ])
        connection.commit()

    except (Exception, Error):
        if errorcode == 1:
            errormsg = jsonify("ERROR: No puede modificar este registro!")
            print("ERROR: 1")
        else:
            logging.error(f"[ERROR]: Algo ha salido mal al intentar guardar.")
    finally:
        if connection:
            cursor.close()
            connection.close()

    if errorcode != 0:
        return (errormsg)
    else:
        return jsonify("Se editó el registro correctamente!")
######################################################################################################################################3
probar

{
  "creador": "admin",
  "cr_id": 123,
  "servidor": "servidor1",
  "ip": "192.168.1.1",
  "tipo_servidor": "producción",
  "entorno_ci": "producción",
  "pais": "Honduras",
  "aplicacion": "CRM",
  "lenguaje": "Python",
  "proveedor": "ProveedorX",
  "desarrollo": "Interno",
  "responsable": "IT",
  "rep": "Backup",
  "alojamiento": "On-premise",
  "esquema_de_continuidad": "Plan A",
  "estrategias_de_recuperacion_infra": "Estrategia 1",
  "estrategias_de_recuperacion_datos": "Estrategia 2",
  "tiempo_de_instalacion_servidor": "2 horas",
  "tiempo_de_instalacion_aplicacion": "4 horas",
  "joya_de_la_corona": "Sí",
  "upwd": "123456"
}

#########################################################  Segunda api  ##################################################################
funcion sql:
CREATE OR REPLACE FUNCTION delete_cis_registro(p_cr_id INT)
RETURNS VOID AS $$
BEGIN
    DELETE FROM cis_registros WHERE cr_id = p_cr_id;
END;
$$ LANGUAGE plpgsql;

##################################### API  #####################################################################################################
@cmdb.route('/cmdb/delete', methods=['POST'])
@require_api_key
def delete_record():
    try:
        data = request.get_json()
        creador = data['creador'].replace('"', '')
        cr_id = data['cr_id']
        user_groups = ldap_login(creador, data['upwd'].replace('"', ''))

        # Validar permisos
        if not any('ccyl' in group for group in user_groups):
            return jsonify({"error": "No tiene permisos para eliminar registros!"}), 403
        
        # Conexión a la base de datos con manejo de errores
        with psycopg2.connect(user=db_User, password=db_Pass, host=db_Host, port=db_Port, database="cmdb_integracion") as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                sql = "DELETE FROM cis_registros WHERE cr_id = %s"
                cursor.execute(sql, (cr_id,))
                connection.commit()

        return jsonify({"message": "Se eliminó el registro!"})
    
    except (psycopg2.DatabaseError) as e:
        logging.error(f"[ERROR]: Error en la base de datos: {str(e)}")
        return jsonify({"error": "Error al eliminar el registro!"}), 500

    except Exception as e:
        logging.error(f"[ERROR]: {str(e)}")
        return jsonify({"error": "Algo salió mal!"}), 500


Probar:

Usando Postman
En Postman, puedes seguir estos pasos:

Abre Postman y selecciona POST como el método de la solicitud.

En el campo URL, ingresa http://localhost:5000/cmdb/delete.

En la pestaña Headers, añade lo siguiente:

Key: Content-Type
Value: application/json
En la pestaña Body, selecciona la opción raw y luego selecciona JSON (desde el menú desplegable). Ingresa el siguiente contenido en el cuerpo:

json
Copy code
{
    "creador": "nombre_usuario",
    "upwd": "password_usuario",
    "cr_id": 123
}
##################################################################################################################################################################
CREATE OR REPLACE FUNCTION obtener_catalogos()
RETURNS JSONB AS $$
DECLARE
    tablas TEXT[] := ARRAY[
        'cis_alojamiento', 'cis_desarrollo', 'cis_entorno_ci', 
        'cis_lenguaje', 'cis_nombre_aplicacion', 'cis_pais_servidor',
        'cis_proveedor', 'cis_responsable_aplicacion', 'cis_tipo_servidor',
        'cis_esquema', 'cis_estrategias_infra', 'cis_estrategias_datos',
        'cis_tiempo_infra_servidor', 'cis_tiempo_infra_aplicacion', 
        'cis_joya'
    ];
    resultado JSONB := '[]'::JSONB;
    consulta TEXT;
    fila JSONB;
BEGIN
    -- Iterar sobre cada tabla en el array de tablas
    FOREACH consulta IN ARRAY tablas LOOP
        -- Ejecutar la consulta y agregar el resultado a un objeto JSON
        EXECUTE format('SELECT json_agg(t) FROM %I t', consulta)
        INTO fila;
        
        -- Agregar el resultado de la tabla al JSON final
        resultado := resultado || jsonb_build_object(consulta, COALESCE(fila, '[]'::jsonb));
    END LOOP;

    RETURN resultado;
END;
$$ LANGUAGE plpgsql;

#######################################################################################################################################################################
@cmdb.route('/cmdb/catalog', methods=['GET'])
@require_api_key
def catalogos():
    if request.method == 'GET':
        connection = None
        result2 = []
        try:
            # Conectar a la base de datos
            connection = psycopg2.connect(user=db_User,
                                          password=db_Pass,
                                          host=db_Host,
                                          port=db_Port,
                                          database="cmdb_integracion")
            cursor = connection.cursor()
            
            # Ejecutar la función de PostgreSQL
            cursor.execute("SELECT obtener_catalogos();")
            result = cursor.fetchone()[0]  # Obtener el resultado en formato JSON
            
            result2.append(result)
            logging.info(json.dumps(result2))
        except Error as e:
            logging.error(f"[ERROR]: Algo ha salido mal: {e.pgerror}")
        finally:
            if connection:
                cursor.close()
                connection.close()
                
    return json.dumps(result2, ensure_ascii=False).encode('utf8')

########################################################################################################################################################################
@cmdb.route('/cmdb/delete_catalog', methods=['POST'])
@require_api_key
def deleteCatalog():
    if request.method == 'POST':
        connection = None
        id = request.form.get('id').replace('"', '') 
        catalogo = request.form.get('cat').replace('"', '') 
        
        try:
            connection = psycopg2.connect(user=db_User,
                                          password=db_Pass,
                                          host=db_Host,
                                          port=db_Port,
                                          database="cmdb_integracion")
            cursor = connection.cursor()
            # Llamada a la función de PostgreSQL para eliminar el registro
            cursor.execute("SELECT delete_catalog_entry(%s, %s);", (catalogo, id))
            connection.commit()
        except Error as e:
            logging.error(f"[ERROR]: Algo ha salido mal al intentar eliminar: {e.pgerror}")
            return jsonify(f"Error al eliminar el registro: {e.pgerror}"), 500
        finally:
            if connection:
                cursor.close()
                connection.close()
        
    return jsonify("Se eliminó el registro correctamente!")


#########################################################################################################################################################################
sql
CREATE OR REPLACE FUNCTION delete_catalog_entry(catalogo_name VARCHAR, entry_id VARCHAR)
RETURNS VOID AS $$
DECLARE
    catalog_table TEXT;
    column_id TEXT;
BEGIN
    -- Mapea el nombre del catálogo a su tabla y columna correspondiente
    CASE catalogo_name
        WHEN 'Alojamiento' THEN
            catalog_table := 'cis_alojamiento';
            column_id := 'ca_id';
        WHEN 'Desarrollo' THEN
            catalog_table := 'cis_desarrollo';
            column_id := 'cd_id';
        WHEN 'Entorno' THEN
            catalog_table := 'cis_entorno_ci';
            column_id := 'cec_id';
        WHEN 'Lenguaje' THEN
            catalog_table := 'cis_lenguaje';
            column_id := 'cl_id';
        WHEN 'Aplicacion' THEN
            catalog_table := 'cis_nombre_aplicacion';
            column_id := 'cna_id';
        WHEN 'Pais' THEN
            catalog_table := 'cis_pais_servidor';
            column_id := 'cps_id';
        WHEN 'Proveedor' THEN
            catalog_table := 'cis_proveedor';
            column_id := 'cp_id';
        WHEN 'Responsable' THEN
            catalog_table := 'cis_responsable_aplicacion';
            column_id := 'cra_id';
        WHEN 'Tipo Servidor' THEN
            catalog_table := 'cis_tipo_servidor';
            column_id := 'cts_id';
        WHEN 'Esquema de Continuidad' THEN
            catalog_table := 'cis_esquema';
            column_id := 'ce_id';
        WHEN 'Estrategias de Recuperación Infra' THEN
            catalog_table := 'cis_estrategias_infra';
            column_id := 'cei_id';
        WHEN 'Estrategias de Recuperación Datos' THEN
            catalog_table := 'cis_estrategias_datos';
            column_id := 'ced_id';
        WHEN 'Tiempo de Instalación (Servidor)' THEN
            catalog_table := 'cis_tiempo_infra_servidor';
            column_id := 'ctis_id';
        WHEN 'Tiempo de Instalación (Aplicación)' THEN
            catalog_table := 'cis_tiempo_infra_aplicacion';
            column_id := 'ctia_id';
        WHEN 'Joya de la Corona' THEN
            catalog_table := 'cis_joya';
            column_id := 'cj_id';
        ELSE
            RAISE EXCEPTION 'Catálogo no válido: %', catalogo_name;
    END CASE;

    -- Ejecuta la eliminación basada en el catálogo y ID proporcionados
    EXECUTE format('DELETE FROM %I WHERE %I = %L', catalog_table, column_id, entry_id);
END;
$$ LANGUAGE plpgsql;
