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

SELECT actualizar_cis_registro(1, 'servidor1', '192.168.0.1', 'web', 'prod', 'MX', 'app1', 'python', 'Proveedor1', 'Dev1', 'Resp1', 'Rep1', 'Alojamiento1', 'Esquema1', 'Estrategia1', 'Estrategia2', '1h', '2h', 'Si');


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


#######################################catalogo ####################################################################################################33





######################################### funcion agregar #################################################################################################################
CREATE OR REPLACE FUNCTION create_cis_record(
    cr_servidor text, cr_direccion_ip text, cr_tipo_servidor text, cr_entorno_ci text, 
    cr_pais text, cr_aplicacion text, cr_lenguaje text, cr_proveedor text, 
    cr_desarrollo text, cr_mesa_responsable text, cr_rep text, cr_alojamiento text, 
    cr_esquema_de_continuidad text, cr_estrategias_de_recuperacion_infra text, 
    cr_estrategias_de_recuperacion_datos text, cr_tiempo_de_instalacion_servidor text, 
    cr_tiempo_de_instalacion_aplicacion text, cr_joya_de_la_corona text, cr_creador text)
RETURNS void AS $$
BEGIN
    INSERT INTO cis_registros(cr_servidor, cr_direccion_ip, cr_tipo_servidor, cr_entorno_ci, 
                              cr_pais, cr_aplicacion, cr_lenguaje, cr_proveedor, cr_desarrollo, 
                              cr_mesa_responsable, cr_rep, cr_alojamiento, cr_esquema_de_continuidad, 
                              cr_estrategias_de_recuperacion_infra, cr_estrategias_de_recuperacion_datos, 
                              cr_tiempo_de_instalacion_servidor, cr_tiempo_de_instalacion_aplicacion, 
                              cr_joya_de_la_corona, cr_creador, cr_fecha)
    VALUES (cr_servidor, cr_direccion_ip, cr_tipo_servidor, cr_entorno_ci, cr_pais, cr_aplicacion, 
            cr_lenguaje, cr_proveedor, cr_desarrollo, cr_mesa_responsable, cr_rep, cr_alojamiento, 
            cr_esquema_de_continuidad, cr_estrategias_de_recuperacion_infra, cr_estrategias_de_recuperacion_datos, 
            cr_tiempo_de_instalacion_servidor, cr_tiempo_de_instalacion_aplicacion, cr_joya_de_la_corona, cr_creador, now());
END;
$$ LANGUAGE plpgsql;

##############api##############
@cmdb.route('/cmdb/create', methods=['POST'])
@require_api_key
def create_record():
    try:
        data = request.get_json()
        creador = data['creador'].replace('"', '')
        
        # Obtén los datos desde la solicitud JSON
        new_record = (
            data['servidor'], data['ip'], data['tipo_servidor'], data['entorno_ci'], data['pais'], 
            data['aplicacion'], data['lenguaje'], data['proveedor'], data['desarrollo'], 
            data['responsable'], data['rep'], data['alojamiento'], data['esquema_de_continuidad'], 
            data['estrategias_de_recuperacion_infra'], data['estrategias_de_recuperacion_datos'], 
            data['tiempo_de_instalacion_servidor'], data['tiempo_de_instalacion_aplicacion'], 
            data['joya_de_la_corona'], creador
        )

        # Conexión a la base de datos
        connection = psycopg2.connect(user=db_User,
                                      password=db_Pass,
                                      host=db_Host,
                                      port=db_Port,
                                      database="cmdb_integracion")
        cursor = connection.cursor()

        # Llamada a la función almacenada
        cursor.callproc('create_cis_record', new_record)

        # Confirmar los cambios en la base de datos
        connection.commit()
        
        return make_response('', 201)

    except Error as e:
        logging.error(f"[ERROR]: Algo ha salido mal al intentar guardar: {e.pgerror}")
    finally:
        if connection:
            cursor.close()
            connection.close()

    return make_response({'status': 'FAILED', 'message': 'Algo ha salido mal al guardar registro.'}, 500)



####################################################################################################################################################3
sql
CREATE OR REPLACE FUNCTION add_catalog_item(
    catalog_name TEXT,
    value TEXT
) RETURNS TEXT AS $$
DECLARE
    table_name TEXT;
    column_name TEXT;
    query TEXT;
    check_query TEXT;
    exists_count INT;
BEGIN
    -- Mapeo de catálogos a tablas y columnas
    IF catalog_name = 'Alojamiento' THEN
        table_name := 'cis_alojamiento';
        column_name := 'ca_tipo_alojamiento';
    ELSIF catalog_name = 'Desarrollo' THEN
        table_name := 'cis_desarrollo';
        column_name := 'cd_desarrollo';
    ELSIF catalog_name = 'Entorno' THEN
        table_name := 'cis_entorno_ci';
        column_name := 'cec_tipo';
    ELSIF catalog_name = 'Lenguaje' THEN
        table_name := 'cis_lenguaje';
        column_name := 'cl_lenguaje';
    ELSIF catalog_name = 'Aplicacion' THEN
        table_name := 'cis_nombre_aplicacion';
        column_name := 'cna_aplicacion';
    ELSIF catalog_name = 'Pais' THEN
        table_name := 'cis_pais_servidor';
        column_name := 'cps_servidor';
    ELSIF catalog_name = 'Proveedor' THEN
        table_name := 'cis_proveedor';
        column_name := 'cp_proveedor';
    ELSIF catalog_name = 'Responsable' THEN
        table_name := 'cis_responsable_aplicacion';
        column_name := 'cra_mesa';
    ELSIF catalog_name = 'Tipo Servidor' THEN
        table_name := 'cis_tipo_servidor';
        column_name := 'cts_tipo_servidor';
    ELSIF catalog_name = 'Esquema de Continuidad' THEN
        table_name := 'cis_esquema';
        column_name := 'ce_esquema';
    ELSIF catalog_name = 'Estrategias de Recuperación Infra' THEN
        table_name := 'cis_estrategias_infra';
        column_name := 'cei_estrategias';
    ELSIF catalog_name = 'Estrategias de Recuperación Datos' THEN
        table_name := 'cis_estrategias_datos';
        column_name := 'ced_estrategias';
    ELSIF catalog_name = 'Tiempo de Instalación (Servidor)' THEN
        table_name := 'cis_tiempo_infra_servidor';
        column_name := 'ctis_tiempo';
    ELSIF catalog_name = 'Tiempo de Instalación (Aplicación)' THEN
        table_name := 'cis_tiempo_infra_aplicacion';
        column_name := 'ctia_tiempo';
    ELSIF catalog_name = 'Joya de la Corona' THEN
        table_name := 'cis_joya';
        column_name := 'cj_joya';
    ELSE
        RETURN 'ERROR: Catálogo no reconocido.';
    END IF;

    -- Verifica si el valor ya existe en la tabla
    check_query := FORMAT('SELECT COUNT(*) FROM %I WHERE %I = $1', table_name, column_name);
    EXECUTE check_query INTO exists_count USING value;

    IF exists_count > 0 THEN
        RETURN 'ERROR: El dato ya existe en el catálogo.';
    END IF;

    -- Inserta el nuevo valor
    query := FORMAT('INSERT INTO %I (%I) VALUES ($1)', table_name, column_name);
    EXECUTE query USING value;

    RETURN 'Se agregó el registro correctamente!';
END;
$$ LANGUAGE plpgsql;

#####################################################################################################################################################
api 
@cmdb.route('/cmdb/add_catalog', methods=['POST'])
@require_api_key
def addCatalog():
    if request.method == 'POST':
        errorcode = 0
        errormsg = ""
        result = []
        connection = None

        value = request.form.get('value').replace('"', '') 
        catalogo = request.form.get('tabValue').replace('"', '') 
        
        try:
            connection = psycopg2.connect(user=db_User,
                                          password=db_Pass,
                                          host=db_Host,
                                          port=db_Port,
                                          database="cmdb_integracion")
            cursor = connection.cursor()

            # Llama a la función almacenada en PostgreSQL
            cursor.execute("SELECT add_catalog_item(%s, %s)", (catalogo, value))
            result = cursor.fetchone()[0]  # Obtiene el resultado devuelto por la función

            connection.commit()

        except Error as e:
            logging.error(f"[ERROR]: Algo ha salido mal al intentar guardar: {e.pgerror}")
            errormsg = jsonify(f"ERROR: {e.pgerror}")
            errorcode = 1
        finally:
            if connection:
                cursor.close()
                connection.close()
        
        if errorcode != 0:
            return errormsg
        else: 
            return jsonify(result)



#####################################################################################################################################
update catalogo
CREATE OR REPLACE FUNCTION update_catalogo(
    table_name TEXT,
    column_id TEXT,
    column_data TEXT,
    value TEXT,
    record_id TEXT
)
RETURNS TEXT AS $$
DECLARE
    exists_check INTEGER;
BEGIN
    -- Verificar si el valor ya existe
    EXECUTE format('SELECT COUNT(1) FROM %I WHERE %I = $1', table_name, column_data)
    INTO exists_check
    USING value;

    IF exists_check > 0 THEN
        RETURN 'ERROR: El dato ya existe en el catálogo.';
    END IF;

    -- Actualizar el registro
    EXECUTE format('UPDATE %I SET %I = $1 WHERE %I = $2', table_name, column_data, column_id)
    USING value, record_id;

    RETURN 'Se editó el registro correctamente!';
END;
$$ LANGUAGE plpgsql;
######################## api ##########################################################
@cmdb.route('/cmdb/edit_catalog', methods=['POST'])
@require_api_key
def editCatalog():
    if request.method == 'POST':
        errorcode = 0
        errormsg = ""
        connection = None

        # Listas originales
        catalogos = ["Alojamiento", "Desarrollo", "Entorno", "Lenguaje", 
                     "Aplicacion", "Pais", "Proveedor", "Responsable", 
                     "Tipo Servidor", "Esquema de Continuidad", 
                     "Estrategias de Recuperación Infra", 
                     "Estrategias de Recuperación Datos",
                     "Tiempo de Instalación (Servidor)",
                     "Tiempo de Instalación (Aplicación)", 
                     "Joya de la Corona"]
        
        tables = ["cis_alojamiento", "cis_desarrollo", "cis_entorno_ci", 
                  "cis_lenguaje", "cis_nombre_aplicacion", "cis_pais_servidor",
                  "cis_proveedor", "cis_responsable_aplicacion", "cis_tipo_servidor",
                  "cis_esquema", "cis_estrategias_infra", "cis_estrategias_datos",
                  "cis_tiempo_infra_servidor", "cis_tiempo_infra_aplicacion", 
                  "cis_joya"]
        
        col_id = ["ca_id", "cd_id", "cec_id", "cl_id", "cna_id", 
                  "cps_id", "cp_id", "cra_id", "cts_id", "ce_id",
                  "cei_id", "ced_id", "ctis_id", "ctia_id", "cj_id"]
        
        col_data = ["ca_tipo_alojamiento", "cd_desarrollo", "cec_tipo", 
                    "cl_lenguaje", "cna_aplicacion", "cps_servidor", 
                    "cp_proveedor", "cra_mesa", "cts_tipo_servidor", 
                    "ce_esquema", "cei_estrategias", "ced_estrategias",
                    "ctis_tiempo", "ctia_tiempo", "cj_joya"]

        # Obtener los datos del request y limpiar comillas
        id = request.form.get('id').replace('"', '') 
        value = request.form.get('value').replace('"', '') 
        catalogo = request.form.get('cat').replace('"', '') 

        if not id or not value or not catalogo:
            return jsonify("ERROR: Parámetros inválidos o incompletos."), 400

        try:
            # Verificar si el catálogo existe en la lista
            if catalogo not in catalogos:
                return jsonify("ERROR: Catálogo inválido."), 400
            
            # Obtener los índices correspondientes
            idx = catalogos.index(catalogo)
            table = tables[idx]
            column_id = col_id[idx]
            column_data = col_data[idx]

            # Conectar a la base de datos
            connection = psycopg2.connect(user=db_User,
                                          password=db_Pass,
                                          host=db_Host,
                                          port=db_Port,
                                          database="cmdb_integracion")
            cursor = connection.cursor()

            # Llamar a la función de PostgreSQL
            cursor.execute("SELECT update_catalogo(%s, %s, %s, %s, %s)", 
                           (table, column_id, column_data, value, id))

            # Obtener el mensaje de la función
            result = cursor.fetchone()[0]

            # Validar la respuesta de la función
            if "ERROR" in result:
                return jsonify(result), 400

            connection.commit()
            return jsonify(result), 200

        except (Exception, psycopg2.Error) as error:
            logging.error(f"[ERROR]: Algo ha salido mal al intentar editar: {error}")
            return jsonify(str(error)), 500

        finally:
            if connection:
                cursor.close()
                connection.close()
 para porbar 
. Añadir parámetros en el cuerpo (Body)
Haz clic en la pestaña Body.

Selecciona la opción x-www-form-urlencoded.

Añade los siguientes campos clave-valor, que representan los datos que envías al servidor:

id: El identificador del registro que quieres editar (ejemplo: 1).
value: El nuevo valor que deseas asignar (ejemplo: NuevoValor).
cat: El nombre del catálogo donde se encuentra el registro que vas a editar (ejemplo: Alojamiento).


#############################################################################################################################333
delete catalogo
@cmdb.route('/cmdb/delete_catalog', methods=['POST'])
@require_api_key
def deleteCatalog():
    if request.method == 'POST':
        connection = None
        id = request.form.get('id', '').replace('"', '') 
        catalogo = request.form.get('cat', '').replace('"', '') 

        catalogos = ["Alojamiento", "Desarrollo", "Entorno", "Lenguaje", 
                     "Aplicacion", "Pais", "Proveedor", "Responsable", "Tipo Servidor",
                     "Esquema de Continuidad", "Estrategias de Recuperación Infra",
                     "Estrategias de Recuperación Datos",
                     "Tiempo de Instalación (Servidor)",
                     "Tiempo de Instalación (Aplicación)", "Joya de la Corona"]
                     
        tables = ["cis_alojamiento", "cis_desarrollo", "cis_entorno_ci", 
                  "cis_lenguaje", "cis_nombre_aplicacion", "cis_pais_servidor",
                  "cis_proveedor", "cis_responsable_aplicacion", "cis_tipo_servidor",
                  "cis_esquema", "cis_estrategias_infra", "cis_estrategias_datos",
                  "cis_tiempo_infra_servidor", "cis_tiempo_infra_aplicacion",
                  "cis_joya"]
                  
        col_id = ["ca_id", "cd_id", "cec_id", "cl_id", "cna_id", 
                  "cps_id", "cp_id", "cra_id", "cts_id", "ce_id",
                  "cei_id", "ced_id", "ctis_id", "ctia_id", "cj_id"]

        # Obtener la tabla y la columna ID correspondientes
        catalog = None
        c_id = None

        for i, cat in enumerate(catalogos):
            if cat == catalogo:
                catalog = tables[i]
                c_id = col_id[i]
                break

        if not catalog or not c_id:
            return jsonify({"error": "Catálogo no válido"}), 400

        try:
            # Conectar a la base de datos
            connection = psycopg2.connect(user=db_User,
                                          password=db_Pass,
                                          host=db_Host,
                                          port=db_Port,
                                          database="cmdb_integracion")
            cursor = connection.cursor(cursor_factory=RealDictCursor)

            # Llamar a la función de PostgreSQL para eliminar
            cursor.callproc('delete_from_catalog', (catalog, id))
            connection.commit()

        except psycopg2.Error as e:
            logging.error(f"[ERROR]: Algo ha salido mal al intentar eliminar: {e.pgerror}")
            return jsonify({"error": "Error al eliminar el registro"}), 500

        finally:
            # Cerrar la conexión y el cursor
            if connection:
                cursor.close()
                connection.close()

        return jsonify("Se eliminó el registro correctamente!")

    return jsonify({"error": "Método no permitido"}), 405
##########################################################################################################################################
CREATE OR REPLACE FUNCTION delete_from_catalog(catalog_name TEXT, record_id INT)
RETURNS VOID AS $$
DECLARE
    query TEXT;
BEGIN
    -- Construir la consulta de eliminación
    query := format('DELETE FROM %I WHERE id = %L', catalog_name, record_id);
    
    -- Ejecutar la consulta dinámica
    EXECUTE query;
EXCEPTION
    WHEN others THEN
        RAISE EXCEPTION 'Error al eliminar el registro: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

#####################################################################################################################################################
Agregar Body:

Selecciona Body y luego elige la opción x-www-form-urlencoded.
Agrega los siguientes parámetros:
id: el ID del registro que deseas eliminar.
cat: el nombre del catálogo (por ejemplo, "Alojamiento")



#####################################################################################################################################################3
probar eliminar
@cmdb.route('/cmdb/remove_catalog', methods=['POST'])
@require_api_key
def removeCatalog():
    if request.method == 'POST':
        errorcode = 0
        errormsg = ""
        result = []
        connection = None

        value = request.form.get('value').replace('"', '') 
        catalogo = request.form.get('tabValue').replace('"', '') 
        
        try:
            connection = psycopg2.connect(user=db_User,
                                          password=db_Pass,
                                          host=db_Host,
                                          port=db_Port,
                                          database="cmdb_integracion")
            cursor = connection.cursor()

            # Llama a la función almacenada en PostgreSQL
            cursor.execute("SELECT remove_catalog_item(%s, %s)", (catalogo, value))
            result = cursor.fetchone()[0]  # Obtiene el resultado devuelto por la función

            connection.commit()

        except Error as e:
            logging.error(f"[ERROR]: Algo ha salido mal al intentar eliminar: {e.pgerror}")
            errormsg = jsonify(f"ERROR: {e.pgerror}")
            errorcode = 1
        finally:
            if connection:
                cursor.close()
                connection.close()
        
        if errorcode != 0:
            return errormsg
        else: 
            return jsonify(result)


CREATE OR REPLACE FUNCTION remove_catalog_item(
    catalog_name TEXT,
    value TEXT
) RETURNS TEXT AS $$
DECLARE
    table_name TEXT;
    column_name TEXT;
    query TEXT;
    check_query TEXT;
    exists_count INT;
BEGIN
    -- Mapeo de catálogos a tablas y columnas
    IF catalog_name = 'Alojamiento' THEN
        table_name := 'cis_alojamiento';
        column_name := 'ca_tipo_alojamiento';
    ELSIF catalog_name = 'Desarrollo' THEN
        table_name := 'cis_desarrollo';
        column_name := 'cd_desarrollo';
    ELSIF catalog_name = 'Entorno' THEN
        table_name := 'cis_entorno_ci';
        column_name := 'cec_tipo';
    ELSIF catalog_name = 'Lenguaje' THEN
        table_name := 'cis_lenguaje';
        column_name := 'cl_lenguaje';
    ELSIF catalog_name = 'Aplicacion' THEN
        table_name := 'cis_nombre_aplicacion';
        column_name := 'cna_aplicacion';
    ELSIF catalog_name = 'Pais' THEN
        table_name := 'cis_pais_servidor';
        column_name := 'cps_servidor';
    ELSIF catalog_name = 'Proveedor' THEN
        table_name := 'cis_proveedor';
        column_name := 'cp_proveedor';
    ELSIF catalog_name = 'Responsable' THEN
        table_name := 'cis_responsable_aplicacion';
        column_name := 'cra_mesa';
    ELSIF catalog_name = 'Tipo Servidor' THEN
        table_name := 'cis_tipo_servidor';
        column_name := 'cts_tipo_servidor';
    ELSIF catalog_name = 'Esquema de Continuidad' THEN
        table_name := 'cis_esquema';
        column_name := 'ce_esquema';
    ELSIF catalog_name = 'Estrategias de Recuperación Infra' THEN
        table_name := 'cis_estrategias_infra';
        column_name := 'cei_estrategias';
    ELSIF catalog_name = 'Estrategias de Recuperación Datos' THEN
        table_name := 'cis_estrategias_datos';
        column_name := 'ced_estrategias';
    ELSIF catalog_name = 'Tiempo de Instalación (Servidor)' THEN
        table_name := 'cis_tiempo_infra_servidor';
        column_name := 'ctis_tiempo';
    ELSIF catalog_name = 'Tiempo de Instalación (Aplicación)' THEN
        table_name := 'cis_tiempo_infra_aplicacion';
        column_name := 'ctia_tiempo';
    ELSIF catalog_name = 'Joya de la Corona' THEN
        table_name := 'cis_joya';
        column_name := 'cj_joya';
    ELSE
        RETURN 'ERROR: Catálogo no reconocido.';
    END IF;

    -- Verifica si el valor existe en la tabla
    check_query := FORMAT('SELECT COUNT(*) FROM %I WHERE %I = $1', table_name, column_name);
    EXECUTE check_query INTO exists_count USING value;

    IF exists_count = 0 THEN
        RETURN 'ERROR: El dato no existe en el catálogo.';
    END IF;

    -- Elimina el valor
    query := FORMAT('DELETE FROM %I WHERE %I = $1', table_name, column_name);
    EXECUTE query USING value;

    RETURN 'Se eliminó el registro correctamente!';
END;
$$ LANGUAGE plpgsql;


Body: En la pestaña "Body", selecciona x-www-form-urlencoded y agrega los siguientes parámetros:
value: El valor que deseas eliminar.
tabValue: El nombre del catálogo del cual deseas eliminar el valor.
Ejemplo:

value: "Alojamiento1"
tabValue: "Alojamiento"

#########################################################################################################################################
CREATE OR REPLACE FUNCTION update_catalog(
    catalogo TEXT, 
    item_id TEXT, 
    new_value TEXT
) 
RETURNS TEXT AS $$
DECLARE
    catalog TEXT;
    c_id TEXT;
    c_data TEXT;
    result_count INT;

    catalogos TEXT[] := ARRAY['Alojamiento', 'Desarrollo', 'Entorno', 'Lenguaje', 
                     'Aplicacion', 'Pais', 'Proveedor', 'Responsable', 'Tipo Servidor',
                     'Esquema de Continuidad', 'Estrategias de Recuperación Infra',
                     'Estrategias de Recuperación Datos', 'Tiempo de Instalación (Servidor)',
                     'Tiempo de Instalación (Aplicación)', 'Joya de la Corona'];

    tables TEXT[] := ARRAY['cis_alojamiento', 'cis_desarrollo', 'cis_entorno_ci', 
                  'cis_lenguaje', 'cis_nombre_aplicacion', 'cis_pais_servidor',
                  'cis_proveedor', 'cis_responsable_aplicacion', 'cis_tipo_servidor',
                  'cis_esquema', 'cis_estrategias_infra', 'cis_estrategias_datos',
                  'cis_tiempo_infra_servidor', 'cis_tiempo_infra_aplicacion', 'cis_joya'];

    col_id TEXT[] := ARRAY['ca_id', 'cd_id', 'cec_id', 'cl_id', 'cna_id', 
                  'cps_id', 'cp_id', 'cra_id', 'cts_id', 'ce_id', 
                  'cei_id', 'ced_id', 'ctis_id', 'ctia_id', 'cj_id'];

    col_data TEXT[] := ARRAY['ca_tipo_alojamiento', 'cd_desarrollo', 'cec_tipo', 
                    'cl_lenguaje', 'cna_aplicacion', 'cps_servidor', 
                    'cp_proveedor', 'cra_mesa', 'cts_tipo_servidor', 'ce_esquema',
                    'cei_estrategias', 'ced_estrategias', 'ctis_tiempo', 'ctia_tiempo', 'cj_joya'];

BEGIN
    -- Identificar el índice del catálogo
    FOR i IN 1..array_length(catalogos, 1) LOOP
        IF catalogos[i] = catalogo THEN
            catalog := tables[i];
            c_id := col_id[i];
            c_data := col_data[i];
            EXIT;
        END IF;
    END LOOP;

    -- Verificar si el nuevo valor ya existe
    EXECUTE format('SELECT COUNT(*) FROM %I WHERE %I = $1', catalog, c_data) INTO result_count USING new_value;
    
    IF result_count > 0 THEN
        RETURN 'ERROR: El dato ya existe en el catálogo.';
    END IF;

    -- Actualizar el valor
    EXECUTE format('UPDATE %I SET %I = $1 WHERE %I = $2', catalog, c_data, c_id) USING new_value, item_id;

    RETURN 'Se editó el registro correctamente!';
END;
$$ LANGUAGE plpgsql;

@cmdb.route('/cmdb/edit_catalog', methods=['POST'])
@require_api_key
def editCatalog():
    if request.method == 'POST':
        try:
            catalogo = request.form.get('cat').replace('"', '')
            id = request.form.get('id').replace('"', '')
            value = request.form.get('value').replace('"', '')

            # Conectar a la base de datos y ejecutar la función
            connection = psycopg2.connect(user=db_User, password=db_Pass, host=db_Host, port=db_Port, database="cmdb_integracion")
            cursor = connection.cursor()
            cursor.callproc('update_catalog', (catalogo, id, value))
            result = cursor.fetchone()[0]
            
            connection.commit()

        except Exception as e:
            logging.error(f"[ERROR]: Algo ha salido mal al intentar editar: {str(e)}")
            return jsonify({"error": "Ha ocurrido un error al editar el catálogo."}), 500

        finally:
            if connection:
                cursor.close()
                connection.close()

        return jsonify({"message": result})








        La ruta de la API que modificamos es /cmdb/edit_catalog, y espera recibir una solicitud POST con los siguientes parámetros:

id: el identificador del elemento a modificar.
value: el nuevo valor que se asignará.
cat: el nombre del catálogo.
#################################################################################################################################################################################

