@cmdb.route('/cmdb/edit', methods=['POST'])
@require_api_key
def edit_record():
    try:
        errorcode = 0
        errormsg = ""
        data = request.get_json()
        
        # Capturar los datos de la web
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
        
        # ldap
        user_groups = ldap_login(creador, data['upwd'].replace('"', ''))

        # Coneexion 
        connection = psycopg2.connect(user=db_User,
                                       password=db_Pass,
                                       host=db_Host,
                                       port=db_Port,
                                       database="cmdb_integracion")
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        # Verificar permisos del usuario
        var = False
        for group in user_groups:
            if 'ccyl' in group:
                print('parte del grupo')
                var = True
                break
        if not var:
            # Validar si el creador puede editar el registro
            cursor.execute(f"SELECT cr_creador FROM cis_registros WHERE cr_id = {cr_id};")
            result = cursor.fetchone()
            if not result or creador not in result.values():
                errorcode = 1
                raise Exception("ERROR: No puede modificar este registro!")

        # Usar la función actualizar_registro para editar el registro
        sql = f"SELECT actualizar_cis_registro('{cr_id}', '{servidor}', '{ip}', '{tipo_servidor}', '{entorno_ci}', '{pais}', '{aplicacion}', '{lenguaje}', '{proveedor}', '{desarrollo}', '{responsable}', '{rep}', '{alojamiento}', '{esquema_de_continuidad}', '{estrategias_de_recuperacion_infra}', '{estrategias_de_recuperacion_datos}', '{tiempo_de_instalacion_servidor}', '{tiempo_de_instalacion_aplicacion}', '{joya_de_la_corona}');"

        cursor.execute(sql)
        connection.commit()

    except (Exception, Error) as e:
        if errorcode == 1:
            errormsg = jsonify("ERROR: No puede modificar este registro!")
            logging.error(f"[ERROR]: {str(e)}")  # guardo el error
        else:
            logging.error(f"[ERROR]: Algo ha salido mal al intentar guardar: {str(e)}")  # guardo el error
    finally:
        if 'cursor' in locals():  # Verifico la conexion 
            cursor.close()
        if 'connection' in locals():  # Vwo la conexion
            connection.close()
    
    if errorcode != 0:
        return errormsg
    else:
        return jsonify("Se editó el registro correctamente!")






@cmdb.route('/cmdb/add_catalog', methods=['POST'])
@require_api_key
def addCatalog():
    if request.method == 'POST':
        errorcode = 0
        errormsg = ""
        result = None
        connection = None

        # obtiene datos de la web
        value = request.form.get('value').replace('"', '') 
        catalogo = request.form.get('tabValue').replace('"', '') 

        try:

            # prueba conexion
            connection = psycopg2.connect(user=db_User,
                                          password=db_Pass,
                                          host=db_Host,
                                          port=db_Port,
                                          database="cmdb_integracion")
            cursor = connection.cursor()

            # Llamo la funcion sql
            cursor.execute("SELECT add_catalog_item(%s, %s)", (catalogo, value))
            result = cursor.fetchone()[0]  # capturo resultado de sql

            connection.commit()

        except psycopg2.DatabaseError as e:
            logging.error(f"[ERROR]: Algo ha salido mal al intentar guardar: {e.pgerror}")
# var = 
            errorcode = 1
            errormsg = f"ERROR: {e.pgerror}"  # mensaje de error
        finally:
            if connection:
                cursor.close()
                connection.close()
        
        # Devuelve el resultado en el formato esperado
        return jsonify({
            "errorcode": errorcode,
            "errormsg": errormsg,
            "result": result if result else "No se ha agregado ningún registro."
        })




@cmdb.route('/cmdb/delete_catalog', methods=['POST'])
@require_api_key
def deleteCatalog():
    if request.method == 'POST':
        connection = None
        errorcode = 0
        errormsg = ""

        # Obtener los valores enviados desde la web
        id = (request.form.get('id').replace('"',''))  # Valor a eliminar
        catalogo = (request.form.get('cat').replace('"',''))  # Nombre del catálogo

        try:
            # prueba conexion
            connection = psycopg2.connect(user=db_User,
                                          password=db_Pass,
                                          host=db_Host,
                                          port=db_Port,
                                          database="cmdb_integracion")
            cursor = connection.cursor(cursor_factory=RealDictCursor)

            # Llamar a la función SQL de PostgreSQL
            cursor.callproc('remove_catalog_item', (catalogo, id))

            # Commit
            connection.commit()

        except Error as e:
            logging.error(f"[ERROR]: Algo ha salido mal al intentar eliminar: {e.pgerror}")
            errormsg = f"ERROR: {e.pgerror}"
            errorcode = 1
        finally:
            if connection:
                cursor.close()
                connection.close()

        # hay error entonces respondo con el error
        if errorcode != 0:
            return jsonify({"error": errormsg}), 400
        # deberia mostrar el error
        else:
            return jsonify({"result": "Se eliminó el registro correctamente!"})




@cmdb.route('/cmdb/delete', methods=['POST'])
@require_api_key
def delete_record():
    try:
        errorcode = 0
        errormsg = ""
        data = request.get_json()
        creador = data['creador'].replace('"', '')  # capturo informacion de la web
        cr_id = data['cr_id']
        user_groups = ldap_login(creador, data['upwd'].replace('"',''))

 
        sql = f"SELECT eliminar_registro({cr_id});"  # Llamando a la función directamente

        connection = psycopg2.connect(user=db_User,
                                       password=db_Pass,
                                       host=db_Host,
                                       port=db_Port,
                                       database="cmdb_integracion")
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        # Verificar grupos de usuario
        var = False
        for group in user_groups:
            if 'ccyl' in group:
                print('parte del grupo')
                var = True
                break
        if not var:
            errorcode = 1
            raise Exception("No tiene permisos para eliminar")

        cursor.execute(sql)
        connection.commit()

    except (Exception, Error) as e:
        if errorcode == 1:
            errormsg = jsonify("ERROR: No tiene permisos para eliminar registros!")
            logging.error(f"[ERROR]: {str(e)}")  # Registrar el error
        else:
            logging.error(f"[ERROR]: Algo ha salido mal al intentar eliminar el registro: {str(e)}")  # guardo el error
    finally:
        if 'cursor' in locals():  # valido y muestro si el cursor existe
            cursor.close()
        if 'connection' in locals():  # Velida la conexion
            connection.close()
    if errorcode != 0:
        return errormsg
    else:
        return jsonify("Se eliminó el registro!")


