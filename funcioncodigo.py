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


