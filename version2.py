from flask import request, jsonify, Blueprint, make_response
from flask_cors import CORS
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
import logging
from app.models.sharepoin_cmdb import SharepointCMDB
from app.routes.utils import getCatalogosSharePoint, require_api_key, ldap_login
from app.environment.environment import *
import psycopg2
import decimal
import pymssql
import json
from concurrent.futures import ThreadPoolExecutor
# Ignore warnings SSL
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)

cmdb = Blueprint('cmdb', __name__, url_prefix='/argoapiv2')
if ambiente == "prod":
    # Lista de URLs permitidas
    allowed_origins = [
        "https://argos:8080",
        "http://localhost:4200"
    ]
if ambiente == "lab":
    allowed_origins = [
        "https://argoslab:54080",
        "http://localhost:4200"
    ]
CORS(cmdb, resources={r"/*": {"origins": allowed_origins}})

# Función para obtener una conexión a la base de datos SQL Server


def connect_db_sql_server(srv_name, db_name, usr_name, passw, port_num, as_dict=False, host='', conn_properties=None, autocommit=False, tds_version='7.1'):
    try:
        return pymssql.connect(
            server=srv_name,
            database=db_name,
            user=usr_name,
            password=passw,
            timeout=60,
            login_timeout=60,
            charset='UTF-8',
            as_dict=as_dict,
            host=host,
            appname=None,
            port=port_num,
            conn_properties=conn_properties,
            autocommit=autocommit,
            tds_version=tds_version
        )
    except Exception as e:
        logging.error(
            f"[ERROR] Realizando conexión al servidor de base de datos {srv_name}: {str(e)}")
        return None

# Función para obtener datos de SQL Server


def exec_script_sql_server(script, connectdb):
    connection = connectdb
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f"""{script}""")
            column_names = [desc[0] for desc in cursor.description]
            data = []
            for row in cursor.fetchall():
                row_dict = {}
                for i in range(len(column_names)):
                    # Verifica si la columna es de tipo decimal.
                    if isinstance(row[i], decimal.Decimal):
                        # Convierte el valor decimal a un número de punto flotante (float).
                        row_dict[column_names[i]] = float(row[i])
                    else:
                        row_dict[column_names[i]] = row[i]
                data.append(row_dict)
            connection.close()
            return data
        except Exception as e:
            logging.error(
                f"[ERROR]: No se pudo obtener la información de la base de datos: {str(e)}")
            return f"[ERROR]: No se pudo obtener la información de la base de datos: {str(e)}"
    else:
        return "Error de conexión a la base de datos"


@cmdb.route('/cmdb', methods=['GET'])
@require_api_key
def get_records():
    connection = None
    records = []
    try:
        connection = psycopg2.connect(user=db_User,
                                      password=db_Pass,
                                      host=db_Host,
                                      port=db_Port,
                                      database="cmdb_integracion")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM cis_registros ORDER BY cr_fecha DESC;")
        for row in cursor.fetchall():
            registro = SharepointCMDB(row[0], row[1], row[2], row[3], row[4], row[5],
                                      row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14],
                                      row[15], row[16], row[17], row[18], row[19], row[20])
            records.append(registro.__dict__)
    except Error as e:
        logging.error(
            f"[ERROR]: Algo ha salido mal al intentar obtener los registros.: {e.pgerror}")
    finally:
        if connection:
            cursor.close()
            connection.close()
    return jsonify(records)


@cmdb.route('/cmdb/get_catalogos', methods=['GET'])
@require_api_key
def get_catalogos():
    catalogos = None
    try:
        catalogos = getCatalogosSharePoint()
        if catalogos is None:
            return jsonify({'error': 'Algo salio mal al consultar catalogos'}), 500
    except Error as e:
        logging.error(
            f"[ERROR]: Algo ha salido mal al intentar obtener los catalogos.: {e.pgerror}")
    return catalogos.__dict__


@cmdb.route('/cmdb/create', methods=['POST'])
@require_api_key
def create_record():
    try:
        data = request.get_json()
        creador = data['creador'].replace('"', '')
        new_record = (data['servidor'], data['ip'], data['tipo_servidor'], data['entorno_ci'], data['pais'], data['aplicacion'],
                      data['lenguaje'], data['proveedor'], data['desarrollo'], data['responsable'], data['rep'], data['alojamiento'], data['esquema_de_continuidad'], data['estrategias_de_recuperacion_infra'], data['estrategias_de_recuperacion_datos'], data['tiempo_de_instalacion_servidor'], data['tiempo_de_instalacion_aplicacion'], data['joya_de_la_corona'], creador)
        sql = """
                INSERT INTO cis_registros(cr_servidor, cr_direccion_ip, cr_tipo_servidor, cr_entorno_ci, cr_pais, cr_aplicacion, cr_lenguaje, cr_proveedor, cr_desarrollo, cr_mesa_responsable, cr_rep, cr_alojamiento, cr_esquema_de_continuidad, cr_estrategias_de_recuperacion_infra, cr_estrategias_de_recuperacion_datos, cr_tiempo_de_instalacion_servidor, cr_tiempo_de_instalacion_aplicacion, cr_joya_de_la_corona, cr_creador, cr_fecha)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())
                """
        connection = psycopg2.connect(user=db_User,
                                      password=db_Pass,
                                      host=db_Host,
                                      port=db_Port,
                                      database="cmdb_integracion")
        cursor = connection.cursor()
        cursor.execute(sql, new_record)
        connection.commit()
        return make_response('', 201)
    except Error as e:
        logging.error(
            f"[ERROR]: Algo ha salido mal al intentar guardar: {e.pgerror}")
    finally:
        if connection:
            cursor.close()
            connection.close()
    return make_response({'status': 'FAILED', 'message': 'Algo ha salido mal al guardar registro.'}, 500)

##editar### modificando 1
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
        
        sql = """
            UPDATE cis_registros
            SET cr_servidor = %s, cr_direccion_ip = %s, cr_tipo_servidor = %s, 
                cr_entorno_ci = %s, cr_pais = %s, cr_aplicacion = %s, cr_lenguaje = %s, 
                cr_proveedor = %s, cr_desarrollo = %s, cr_mesa_responsable = %s, 
                cr_rep = %s, cr_alojamiento = %s, cr_esquema_de_continuidad = %s, 
                cr_estrategias_de_recuperacion_infra = %s, cr_estrategias_de_recuperacion_datos = %s, 
                cr_tiempo_de_instalacion_servidor = %s, cr_tiempo_de_instalacion_aplicacion = %s, 
                cr_joya_de_la_corona = %s
            WHERE cr_id = %s
        """
        with psycopg2.connect(user=db_User, password=db_Pass, host=db_Host, port=db_Port, database="cmdb_integracion") as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                # Validar usuario que edita
                cursor.execute("SELECT cr_creador FROM cis_registros WHERE cr_id = %s", (cr_id,))
                result = cursor.fetchone()

                if 'ccyl' not in user_groups and creador not in result.values():
                    return jsonify({"message": "ERROR: No puede modificar este registro!"}), 403

                # Actualiza la tabla cis_registro
                cursor.execute(sql, (servidor, ip, tipo_servidor, entorno_ci, pais, aplicacion, lenguaje,
                                     proveedor, desarrollo, responsable, rep, alojamiento, 
                                     esquema_de_continuidad, estrategias_de_recuperacion_infra,
                                     estrategias_de_recuperacion_datos, tiempo_de_instalacion_servidor,
                                     tiempo_de_instalacion_aplicacion, joya_de_la_corona, cr_id))
                connection.commit()

        return jsonify("Se editó el registro correctamente!")

    except (psycopg2.Error, KeyError) as e:
        logging.error(f"[ERROR]: {str(e)}")
        return jsonify({"message": "ERROR: Algo ha salido mal al intentar guardar."}), 500

###### modificadad 2#########
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

####no la modifique########
def obtener_datos_atributos_manuales():
    connection = None
    records = []
    try:
        connection = psycopg2.connect(user=db_User,
                                      password=db_Pass,
                                      host=db_Host,
                                      port=db_Port,
                                      database="cmdb_integracion")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM cis_registros ORDER BY cr_fecha DESC;")
        for row in cursor.fetchall():
            registro = SharepointCMDB(row[0], row[1], row[2], row[3], row[4], row[5],
                                      row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14],
                                      row[15], row[16], row[17], row[18], row[19], row[20])
            records.append(registro.__dict__)
    except Error as e:
        logging.error(
            f"[ERROR]: Algo ha salido mal al intentar obtener los registros.: {e.pgerror}")
    finally:
        if connection:
            cursor.close()
            connection.close()
    return records

######No modificar############
def obtener_datos_client_management_discos():
    # Conexión a SQL Server y consulta de datos
    connection = connect_db_sql_server(
        clientManage_Host, clientManage_DB, clientManage_User, clientManage_Pass, clientManage_Port)
    script = """select upper(Dev.DeviceName) as Server, 
                Dev.IPAddress, Dis.LogicalDisksSpace
                from v_cmdb_device Dev,  V_Disk_Summary Dis
                where Dev.DeviceID  = Dis.DeviceID
                and Dev.DeviceType = 'server'
                """
    data = exec_script_sql_server(script, connection)
    return data

###no modificar############
def obtener_datos_smart_reporting_db():
    # Conexión a SQL Server y consulta de datos
    connection = connect_db_sql_server(
        smartReport_Host, smartReport_DB, smartReport_User, smartReport_Pass, smartReport_Port)
    script = """
        select distinct(case when (charindex('.bgeneral.com', SystemName) > 1 ) then
        upper(substring(SystemName, 0, charindex('.bgeneral.com', SystemName )))
        when (charindex('.bgeneral'    , SystemName) > 1 ) then	lower(substring(SystemName, 0, charindex('.bgeneral', SystemName )))
        when (charindex('.localhost'   , SystemName) > 1 ) then	lower(substring(SystemName, 0, charindex('.localhost', SystemName )))
        when (charindex('.localdomain' , SystemName) > 1 ) then   lower(substring(SystemName, 0, charindex('.localdomain', SystemName )))
        when (charindex('.bgdcaddm2'   , SystemName) > 1 ) then	lower(substring(SystemName, 0, charindex('.bgdcaddm2', SystemName )))
        when (charindex('.bgdcaddm1'  , SystemName) > 1 )  then   lower(substring(SystemName, 0, charindex('.bgdcaddm1', SystemName )))
        when (charindex('.pick.some.domain'  , SystemName) > 1 )  then   lower(substring(SystemName, 0, charindex('.pick.some.domain', SystemName )))
        when (charindex('.'  , SystemName) > 1 )  then   lower(substring(SystemName, 0, charindex('.', SystemName)))
        when (charindex('.profuturo.com.pa'  , SystemName) > 1 )  then   lower(substring(SystemName, 0, charindex('.profuturo.com.pa', SystemName )))
        else upper(SystemName) end )as ServidorBD, InstanceId,
        BD = case when (charindex(':', name)  > 1) then
        substring(name, 1,charindex(':', name,1 )-1) --LEN(name))
        when name = 'SQL Server VSS Writer' then 'Microsoft SQL Server' else name end,
        max(MarketVersion) as 'MarketVersion', max(versionnumber) as 'versionnumber'
        from BMC_CORE_BMC_product where SystemName is not null
        and name = 'SQL Server VSS Writer' 
        or item =  'Relational Database Management Systems' or name like 'Oracle Database %'
        and datasetid = 'BMC.ASSET'
        group by SystemName, name, InstanceId"""
    data = exec_script_sql_server(script, connection)
    return data


def obtener_datos_smart_reporting_computer():
    # Conexión a SQL Server y consulta de datos
    connection = connect_db_sql_server(
        smartReport_Host, smartReport_DB, smartReport_User, smartReport_Pass, smartReport_Port)
    script = """
        select ReconciliationIdentity ,InstanceId, ServidorCS = (
        case when (charindex('.bgeneral.com', CS.name) > 1 ) then	lower(substring(CS.name, 0, charindex('.bgeneral.com', CS.name )))
        when (charindex('.bgeneral'    , CS.name) > 1 ) then	lower(substring(CS.name, 0, charindex('.bgeneral', CS.name )))
        when (charindex('.localhost'   , CS.name) > 1 ) then	lower(substring(CS.name, 0, charindex('.localhost', CS.name )))
        when (charindex('.localdomain' , CS.name) > 1 ) then   lower(substring(CS.name, 0, charindex('.localdomain', CS.name )))
        when (charindex('.bgdcaddm2'   , CS.name) > 1 ) then	lower(substring(CS.name, 0, charindex('.bgdcaddm2', CS.name )))
        when (charindex('.bgdcaddm1'  , CS.name) > 1 )  then   lower(substring(CS.name, 0, charindex('.bgdcaddm1', CS.name )))
        when (charindex('.pick.some.domain'  , CS.name) > 1 )  then   lower(substring(CS.name, 0, charindex('.pick.some.domain', CS.name )))
        when (charindex('.'  , CS.name) > 1 )  then   lower(substring(CS.name, 0, charindex('.', CS.name)))
        when (charindex('.profuturo.com.pa'  , CS.name) > 1 )  then   lower(substring(CS.name, 0, charindex('.profuturo.com.pa', CS.name )))
        else Concat(lower(CS.name), ' ') end ),
        Marca = CS.manufacturername,
        Modelo = CS.model   ,
        Memoria = CS.totalphysicalmemory,
        replace((isnull(EnvironmentSpecification,'No disponible')),'NULL','No disponible') as nombre_logico,
        --replace((isnull(Expansion,'No disponible')),'NULL','No disponible') as disco,
        replace((isnull(serialnumber,'No disponible')),'NULL','No disponible') as serie	,
        isvirtual = case when isvirtual = 1 then 'Virtual' else 'Fisico' end ,
        replace((isnull(item,'No disponible')),'NULL','No disponible') as TipoHardware,
        desarrollo = case when Domain = '1' then 'Propio'
                        when Domain = '2' then 'Tercerizado'
                        when Domain = '3' then 'Proveedor Comercial'
                        when Domain = 'bgeneral.com' then 'Proveedor Comercial'
                        else 'No Aplica' end ,
        prioridad = case when (Priority = '0')then 'Normales'
                        when (Priority = '2')then 'Importantes'
                        when (Priority = '4')then 'Críticos' end
        from bmc_core_bmc_computersystem CS where  
        CS.datasetid = 'BMC.ASSET' and (CS.markasdeleted = 0 or CS.markasdeleted is null)
        and Item = 'Server' or Item = 'Management controller'
        group by ReconciliationIdentity,InstanceId, 
        CS.name,CS.manufacturername,CS.model,CS.totalphysicalmemory, 
        EnvironmentSpecification, Expansion, serialnumber, isvirtual, Item, Domain, Priority"""
    data = exec_script_sql_server(script, connection)
    return data


def obtener_datos_smart_reporting_ip():
    # Conexión a SQL Server y consulta de datos
    connection = connect_db_sql_server(
        smartReport_Host, smartReport_DB, smartReport_User, smartReport_Pass, smartReport_Port)
    script = """
        select systemname = (case when (charindex('.bgeneral.com', SystemName) > 1 ) then
        upper(substring(SystemName, 0, charindex('.bgeneral.com', SystemName )))
        when (charindex('.bgeneral'    , SystemName) > 1 ) then	lower(substring(SystemName, 0, charindex('.bgeneral', SystemName )))
        when (charindex('.localhost'   , SystemName) > 1 ) then	lower(substring(SystemName, 0, charindex('.localhost', SystemName )))
        when (charindex('.localdomain' , SystemName) > 1 ) then   lower(substring(SystemName, 0, charindex('.localdomain', SystemName )))
        when (charindex('.bgdcaddm2'   , SystemName) > 1 ) then	lower(substring(SystemName, 0, charindex('.bgdcaddm2', SystemName )))
        when (charindex('.bgdcaddm1'  , SystemName) > 1 )  then   lower(substring(SystemName, 0, charindex('.bgdcaddm1', SystemName )))
        when (charindex('.pick.some.domain'  , SystemName) > 1 )  then   lower(substring(SystemName, 0, charindex('.pick.some.domain', SystemName )))
        when (charindex('.'  , SystemName) > 1 )  then   lower(substring(SystemName, 0, charindex('.', SystemName)))
        when (charindex('.profuturo.com.pa'  , SystemName) > 1 )  then   lower(substring(SystemName, 0, charindex('.profuturo.com.pa', SystemName )))
        else
        upper(SystemName)
        end ) ,I.RelLeadInstanceId,
        address = (select top 1 IP.address from bmc_core_bmc_ipendpoint IP
        where IP.RelLeadInstanceId = CS.InstanceId
        and IP.address  not like '172.%' and IP.address  not like '169.%')
        from bmc_core_bmc_ipendpoint i
        LEFT JOIN bmc_core_bmc_computersystem CS
        ON I.RelLeadInstanceId = CS.InstanceId
        where I.datasetid = 'BMC.ASSET'
        and I.systemname is not null
        and (I.markasdeleted = 0 or I.markasdeleted is null)
        group by I.systemname, I.RelLeadInstanceId, CS.InstanceId"""
    data = exec_script_sql_server(script, connection)
    return data


def obtener_datos_smart_reporting_file_system():
    # Conexión a SQL Server y consulta de datos
    connection = connect_db_sql_server(
        smartReport_Host, smartReport_DB, smartReport_User, smartReport_Pass, smartReport_Port)
    script = """
        select RelLeadInstanceId,
        'ServerFS' = case when (charindex('.bgeneral.com', SystemName) > 1 ) then
        upper(substring(SystemName, 0, charindex('.bgeneral.com', SystemName )))
        when (charindex('.bgeneral'    , SystemName) > 1 ) then	lower(substring(SystemName, 0, charindex('.bgeneral', SystemName )))
        when (charindex('.localhost'   , SystemName) > 1 ) then	lower(substring(SystemName, 0, charindex('.localhost', SystemName )))
        when (charindex('.localdomain' , SystemName) > 1 ) then   lower(substring(SystemName, 0, charindex('.localdomain', SystemName )))
        when (charindex('.bgdcaddm2'   , SystemName) > 1 ) then	lower(substring(SystemName, 0, charindex('.bgdcaddm2', SystemName )))
        when (charindex('.bgdcaddm1'  , SystemName) > 1 )  then   lower(substring(SystemName, 0, charindex('.bgdcaddm1', SystemName )))
        when (charindex('.pick.some.domain'  , SystemName) > 1 )  then   lower(substring(SystemName, 0, charindex('.pick.some.domain', SystemName )))
        when (charindex('.'  , SystemName) > 1 )  then   lower(substring(SystemName, 0, charindex('.', SystemName)))
        when (charindex('.profuturo.com.pa'  , SystemName) > 1 )  then   lower(substring(SystemName, 0, charindex('.profuturo.com.pa', SystemName )))
        else
        upper(SystemName)
        end
        ,concat (sum(FileSystemSize)/1024, ' GB' )as Disco
        from BMC_CORE_BMC_LocalFileSystem 
        where 
        datasetid = 'BMC.ASSET'
        and systemname is not null
        and (markasdeleted = 0 or markasdeleted is null) 
        group by RelLeadInstanceId, systemname"""
    data = exec_script_sql_server(script, connection)
    return data


def obtener_datos_smart_reporting_cpu():
    # Conexión a SQL Server y consulta de datos
    connection = connect_db_sql_server(
        smartReport_Host, smartReport_DB, smartReport_User, smartReport_Pass, smartReport_Port)
    script = """
        select systemname = (case when (charindex('.bgeneral.com', SystemName) > 1 ) then
        upper(substring(SystemName, 0, charindex('.bgeneral.com', SystemName )))
        when (charindex('.bgeneral'    , SystemName) > 1 ) then	lower(substring(SystemName, 0, charindex('.bgeneral', SystemName )))
        when (charindex('.localhost'   , SystemName) > 1 ) then	lower(substring(SystemName, 0, charindex('.localhost', SystemName )))
        when (charindex('.localdomain' , SystemName) > 1 ) then   lower(substring(SystemName, 0, charindex('.localdomain', SystemName )))
        when (charindex('.bgdcaddm2'   , SystemName) > 1 ) then	lower(substring(SystemName, 0, charindex('.bgdcaddm2', SystemName )))
        when (charindex('.bgdcaddm1'  , SystemName) > 1 )  then   lower(substring(SystemName, 0, charindex('.bgdcaddm1', SystemName )))
        when (charindex('.pick.some.domain'  , SystemName) > 1 )  then   lower(substring(SystemName, 0, charindex('.pick.some.domain', SystemName )))
        when (charindex('.'  , SystemName) > 1 )  then   lower(substring(SystemName, 0, charindex('.', SystemName)))
        when (charindex('.profuturo.com.pa'  , SystemName) > 1 )  then   lower(substring(SystemName, 0, charindex('.profuturo.com.pa', SystemName )))
        else
        upper(SystemName)
        end ),count(name) AS CPU , model,  isnull(NumberOfCores, 0) as NumberOfCores, NumberOfLogicalProcessors, RelLeadInstanceId
        from bmc_core_bmc_processor
        where datasetid = 'BMC.ASSET'
        and systemname is not null
        and (markasdeleted = 0 or markasdeleted is null)
        group by systemname, model, NumberOfCores, NumberOfLogicalProcessors, RelLeadInstanceId"""
    data = exec_script_sql_server(script, connection)
    return data


def obtener_datos_smart_reporting_sistema_operativo():
    # Conexión a SQL Server y consulta de datos
    connection = connect_db_sql_server(
        smartReport_Host, smartReport_DB, smartReport_User, smartReport_Pass, smartReport_Port)
    script = """
        select srv_SO = (case when (charindex('.bgeneral.com', SystemName) > 1 ) then
        upper(substring(SystemName, 0, charindex('.bgeneral.com', SystemName )))
        when (charindex('.bgeneral'    , SystemName) > 1 ) then	lower(substring(SystemName, 0, charindex('.bgeneral', SystemName )))
        when (charindex('.localhost'   , SystemName) > 1 ) then	lower(substring(SystemName, 0, charindex('.localhost', SystemName )))
        when (charindex('.localdomain' , SystemName) > 1 ) then   lower(substring(SystemName, 0, charindex('.localdomain', SystemName )))
        when (charindex('.bgdcaddm2'   , SystemName) > 1 ) then	lower(substring(SystemName, 0, charindex('.bgdcaddm2', SystemName )))
        when (charindex('.bgdcaddm1'  , SystemName) > 1 )  then   lower(substring(SystemName, 0, charindex('.bgdcaddm1', SystemName )))
        when (charindex('.pick.some.domain'  , SystemName) > 1 )  then   lower(substring(SystemName, 0, charindex('.pick.some.domain', SystemName )))
        when (charindex('.'  , SystemName) > 1 )  then   lower(substring(SystemName, 0, charindex('.', SystemName)))
        when (charindex('.profuturo.com.pa'  , SystemName) > 1 )  then   lower(substring(SystemName, 0, charindex('.profuturo.com.pa', SystemName )))
        else
        upper(SystemName)
        end )
        , Name as 'Sistema Operativo', RelLeadInstanceId, VersionNumber as 'Versión SO'
        from bmc_core_bmc_operatingsystem
        where datasetid = 'BMC.ASSET'
        and (markasdeleted = 0 or markasdeleted is null)"""
    data = exec_script_sql_server(script, connection)
    return data

###no tocar
@cmdb.route('/cmdb/report', methods=['GET'])
@require_api_key
def obtener_todos_los_datos():
    logging.info("[INFO] Consultando datos para generar reporte")
    LIST_SERVERS = []
    valor_por_defecto = 'No disponible'
    # Lista de tus funciones
    funciones = [obtener_datos_smart_reporting_computer, obtener_datos_smart_reporting_file_system, obtener_datos_smart_reporting_db,
                 obtener_datos_smart_reporting_cpu, obtener_datos_smart_reporting_sistema_operativo, obtener_datos_smart_reporting_ip,
                 obtener_datos_client_management_discos]

    # Usando ThreadPoolExecutor para ejecutar las funciones en paralelo
    with ThreadPoolExecutor() as executor:
        computers = executor.submit(lambda f: json.dumps(
            f(), ensure_ascii=False), funciones[0]).result()
        files_systems = executor.submit(lambda f: json.dumps(
            f(), ensure_ascii=False), funciones[1]).result()
        databases = executor.submit(lambda f: json.dumps(
            f(), ensure_ascii=False), funciones[2]).result()
        cpu = executor.submit(lambda f: json.dumps(
            f(), ensure_ascii=False), funciones[3]).result()
        so = executor.submit(lambda f: json.dumps(
            f(), ensure_ascii=False), funciones[4]).result()
        ips = executor.submit(lambda f: json.dumps(
            f(), ensure_ascii=False), funciones[5]).result()
        discos = executor.submit(lambda f: json.dumps(
            f(), ensure_ascii=False), funciones[6]).result()

    get_computers = json.loads(computers)
    get_files_systems = json.loads(files_systems)
    get_databases = json.loads(databases)
    get_cpu = json.loads(cpu)
    get_so = json.loads(so)
    get_ips = json.loads(ips)
    get_discos = json.loads(discos)
    get_at_manuales = obtener_datos_atributos_manuales()

    for values in get_computers:
        try:
            if values['ServidorCS'] is not None:
                servidor = values['ServidorCS'].upper().strip()
                mem_ram = values['Memoria'] if 'Memoria' in values else valor_por_defecto
                instance_id = values['InstanceId'] if 'InstanceId' in values else valor_por_defecto
                marca = values['Marca'] if 'Marca' in values else valor_por_defecto
                modelo = values['Modelo'] if 'Modelo' in values else valor_por_defecto
                tipo_hardware = values['TipoHardware'] if 'TipoHardware' in values else valor_por_defecto
                desarrollo = values['desarrollo'] if 'desarrollo' in values else valor_por_defecto
                isvirtual = values['isvirtual'] if 'isvirtual' in values else valor_por_defecto
                nombre_logico = values['nombre_logico'] if 'nombre_logico' in values else valor_por_defecto
                prioridad = values['prioridad'] if 'prioridad' in values else valor_por_defecto
                serie = values['serie'] if 'serie' in values else valor_por_defecto
        except Exception as err:
            msg = f"[ERROR] Obteniendo Datos Principales --> {err}"
            print(msg)
            logging.error(msg)

        def obtener_informacion_get_files_systems(servidor):
            try:
                for values in get_files_systems:
                    if servidor == values["ServerFS"] is not None and instance_id == values["RelLeadInstanceId"]:
                        disco = round(float(values['Disco'].replace(
                            ' GB', ''))) if 'Disco' in values else valor_por_defecto
                        return disco
            except Exception as err:
                msg = f"[ERROR] En get_files_systems --> {err}"
                print(msg)
                logging.error(msg)
            return valor_por_defecto

        val_get_files_systems = obtener_informacion_get_files_systems(servidor)

        def obtener_informacion_get_cpu(servidor):
            try:
                for values in get_cpu:
                    if servidor == values["systemname"] is not None and instance_id == values["RelLeadInstanceId"]:
                        cpu = int(
                            values['CPU']) if 'CPU' in values else valor_por_defecto
                        num_cores = int(
                            values['NumberOfCores']) if 'NumberOfCores' in values else valor_por_defecto
                        return cpu, num_cores
            except Exception as err:
                msg = f"[ERROR] En get_cpu --> {err}"
                print(msg)
                logging.error(msg)
            return valor_por_defecto, valor_por_defecto

        val_get_cpu = obtener_informacion_get_cpu(servidor)

        def obtener_informacion_get_so(servidor):
            try:
                for values in get_so:
                    if servidor == values["srv_SO"] is not None and instance_id == values["RelLeadInstanceId"]:
                        sistema_op = values['Sistema Operativo'] if 'Sistema Operativo' in values else valor_por_defecto
                        version_so = values['Versión SO'] if 'Versión SO' in values else valor_por_defecto
                        return sistema_op, version_so
            except Exception as err:
                msg = f"[ERROR] En get_so --> {err}"
                print(msg)
                logging.error(msg)
            return valor_por_defecto, valor_por_defecto

        val_get_so = obtener_informacion_get_so(servidor)

        def obtener_informacion_get_ips(servidor):
            try:
                for values in get_ips:
                    if servidor == values["systemname"] is not None and instance_id == values["RelLeadInstanceId"]:
                        address_ip = values['address'] if 'address' in values else valor_por_defecto
                        return address_ip
            except Exception as err:
                msg = f"[ERROR] En get_ips --> {err}"
                print(msg)
                logging.error(msg)
            return valor_por_defecto

        val_get_ips = obtener_informacion_get_ips(servidor)

        def obtener_informacion_get_discos(servidor):
            try:
                for values in get_discos:
                    if servidor == values["Server"] is not None:
                        disc_space = values['LogicalDisksSpace'] if 'LogicalDisksSpace' in values else valor_por_defecto
                        disc_ip = values['IPAddress'] if 'IPAddress' in values else valor_por_defecto
                        return disc_space, disc_ip
            except Exception as err:
                msg = f"[ERROR] En get_discos --> {err}"
                print(msg)
                logging.error(msg)
            return valor_por_defecto, valor_por_defecto
        val_get_discos = obtener_informacion_get_discos(servidor)

        def obtener_informacion_get_databases(servidor):
            try:
                for values in get_databases:
                    if servidor == values["ServidorBD"] is not None and instance_id == values["InstanceId"]:
                        market_ver_db = values['MarketVersion'] if 'MarketVersion' in values and values[
                            'MarketVersion'] is not None else valor_por_defecto
                        version_db = values['versionnumber'] if 'versionnumber' in values and values[
                            'versionnumber'] is not None else valor_por_defecto
                        return market_ver_db, version_db
            except Exception as err:
                msg = f"[ERROR] En get_databases --> {err}"
                print(msg)
                logging.error(msg)
            return valor_por_defecto, valor_por_defecto

        val_get_databases = obtener_informacion_get_databases(servidor)

        def obtener_informacion_get_at_manuales(servidor):
            try:
                for values in get_at_manuales:
                    if servidor == values["servidor"].upper().strip() is not None:
                        entorno_ci = values['entorno_ci'] if 'entorno_ci' in values and values[
                            'entorno_ci'] is not None else valor_por_defecto
                        responsable = values['responsable'] if 'responsable' in values and values[
                            'responsable'] is not None else valor_por_defecto
                        esquema_de_continuidad = values['esquema_de_continuidad'] if 'esquema_de_continuidad' in values and values[
                            'esquema_de_continuidad'] is not None else valor_por_defecto
                        estrategias_de_recuperacion_infra = values['estrategias_de_recuperacion_infra'] if 'estrategias_de_recuperacion_infra' in values and values[
                            'estrategias_de_recuperacion_infra'] is not None else valor_por_defecto
                        estrategias_de_recuperacion_datos = values['estrategias_de_recuperacion_datos'] if 'estrategias_de_recuperacion_datos' in values and values[
                            'estrategias_de_recuperacion_datos'] is not None else valor_por_defecto
                        tiempo_de_instalacion_servidor = values['tiempo_de_instalacion_servidor'] if 'tiempo_de_instalacion_servidor' in values and values[
                            'tiempo_de_instalacion_servidor'] is not None else valor_por_defecto
                        tiempo_de_instalacion_aplicacion = values['tiempo_de_instalacion_aplicacion'] if 'tiempo_de_instalacion_aplicacion' in values and values[
                            'tiempo_de_instalacion_aplicacion'] is not None else valor_por_defecto
                        joya_de_la_corona = values['joya_de_la_corona'] if 'joya_de_la_corona' in values and values[
                            'joya_de_la_corona'] is not None else valor_por_defecto
                        alojamiento = values['alojamiento'] if 'alojamiento' in values and values[
                            'alojamiento'] is not None else valor_por_defecto
                        pais = values['pais'] if 'pais' in values and values[
                            'pais'] is not None else valor_por_defecto
                        aplicacion = values['aplicacion'] if 'aplicacion' in values and values[
                            'aplicacion'] is not None else valor_por_defecto
                        lenguaje = values['lenguaje'] if 'lenguaje' in values and values[
                            'lenguaje'] is not None else valor_por_defecto
                        proveedor = values['proveedor'] if 'proveedor' in values and values[
                            'proveedor'] is not None else valor_por_defecto
                        desarrollo = values['desarrollo'] if 'desarrollo' in values and values[
                            'desarrollo'] is not None else valor_por_defecto
                        return entorno_ci, responsable, esquema_de_continuidad, estrategias_de_recuperacion_infra, estrategias_de_recuperacion_datos, tiempo_de_instalacion_servidor, tiempo_de_instalacion_aplicacion, joya_de_la_corona, alojamiento, pais, aplicacion, lenguaje, proveedor, desarrollo
            except Exception as err:
                msg = f"[ERROR] En get_at_manuales --> {err}"
                print(msg)
                logging.error(msg)
            return valor_por_defecto, valor_por_defecto, valor_por_defecto, valor_por_defecto, valor_por_defecto, valor_por_defecto, valor_por_defecto, valor_por_defecto, valor_por_defecto, valor_por_defecto, valor_por_defecto, valor_por_defecto, valor_por_defecto, valor_por_defecto,

        val_get_at_manuales = obtener_informacion_get_at_manuales(servidor)

        LIST_SERVERS.append({"Servidor": servidor,
                             "Entorno": val_get_at_manuales[0],
                             "Responsable": val_get_at_manuales[1],
                             "Esquema_de_continuidad": val_get_at_manuales[2],
                             "Estrategias_de_recuperacion_infra": val_get_at_manuales[3],
                             "Estrategias_de_recuperacion_datos": val_get_at_manuales[4],
                             "Tiempo_de_instalacion_servidor": val_get_at_manuales[5],
                             "Tiempo_de_instalacion_aplicacion": val_get_at_manuales[6],
                             "Joya_de_la_corona": val_get_at_manuales[7],
                             "Alojamiento": val_get_at_manuales[8],
                             "Pais": val_get_at_manuales[9],
                             "Aplicacion": val_get_at_manuales[10],
                             "Lenguaje": val_get_at_manuales[11],
                             "Proveedor": val_get_at_manuales[12],
                             "Desarrollo": val_get_at_manuales[13],
                             "Memoria": mem_ram,
                             "Marca": marca,
                             "Modelo": modelo,
                             "Tipo": isvirtual,
                             "Serie": serie,
                             "File_System": val_get_files_systems,
                             "CPU": val_get_cpu[0],
                             "Cores": val_get_cpu[1],
                             "SO": val_get_so[0],
                             "Version_SO": val_get_so[1],
                             "IP": val_get_ips,
                             "Discos": val_get_discos[0],
                             "BD_Market_Version": val_get_databases[0],
                             "BD_Version": val_get_databases[1]})
    logging.info("[INFO] Reporte de la CMDB generado.")
    return jsonify(LIST_SERVERS)
### no la toque debido a que las tablas no se pueden parametrizar en postgresql

@cmdb.route('/cmdb/catalog', methods=['GET'])
@require_api_key
def catalogos():
    if request.method == 'GET':
        result = []
        result2 = []
        connection = None
        tables = ["cis_alojamiento", "cis_desarrollo", "cis_entorno_ci", 
                  "cis_lenguaje", "cis_nombre_aplicacion", "cis_pais_servidor",
                  "cis_proveedor", "cis_responsable_aplicacion", "cis_tipo_servidor",
                  "cis_esquema", "cis_estrategias_infra","cis_estrategias_datos",
                  "cis_tiempo_infra_servidor","cis_tiempo_infra_aplicacion",
                  "cis_joya"]
        try:
            for tabla in tables:
                sql = f"""
                        SELECT * FROM {tabla}
                        """
                connection = psycopg2.connect(user=db_User,
                                            password=db_Pass,
                                            host=db_Host,
                                            port=db_Port,
                                            database="cmdb_integracion")
                cursor = connection.cursor(cursor_factory=RealDictCursor)
                cursor.execute(sql)
                result = cursor.fetchall()
                result2.append(result)
            logging.info(json.dumps(result2))
        except Error as e:
            logging.error(f"[ERROR]: Algo ha salido mal: {e.pgerror}")
        finally:
            if connection:
                cursor.close()
                connection.close()
    return json.dumps(result2, ensure_ascii=False).encode('utf8')

##### modificada: 

@cmdb.route('/cmdb/add_catalog', methods=['POST'])
@require_api_key
def addCatalog():
    if request.method == 'POST':
        errorcode = 0
        errormsg = ""
        result = []
        connection = None
        value = (request.form.get('value').replace('"','')) 
        catalogo = (request.form.get('tabValue').replace('"','')) 
        catalogos = ["Alojamiento", "Desarrollo", "Entorno", "Lenguaje", 
                    "Aplicacion", "Pais", "Proveedor", "Responsable", "Tipo Servidor",
                    "Esquema de Continuidad","Estrategias de Recuperación Infra",
                    "Estrategias de Recuperación Datos",
                    "Tiempo de Instalación (Servidor)",
                    "Tiempo de Instalación (Aplicación)","Joya de la Corona"]
        tables = ["cis_alojamiento", "cis_desarrollo", "cis_entorno_ci", 
                  "cis_lenguaje", "cis_nombre_aplicacion", "cis_pais_servidor",
                  "cis_proveedor", "cis_responsable_aplicacion", "cis_tipo_servidor",
                  "cis_esquema", "cis_estrategias_infra","cis_estrategias_datos",
                  "cis_tiempo_infra_servidor","cis_tiempo_infra_aplicacion",
                  "cis_joya"]
        col_data = ["ca_tipo_alojamiento", "cd_desarrollo", "cec_tipo", 
                  "cl_lenguaje", "cna_aplicacion", "cps_servidor", 
                  "cp_proveedor", "cra_mesa", "cts_tipo_servidor", "ce_esquema",
                  "cei_estrategias","ced_estrategias","ctis_tiempo","ctia_tiempo","cj_joya"
                  ]
        
        try:
            # Validar el catalogo ingresado
            if catalogo not in catalogos:
                raise ValueError("Catálogo no válido.")

            i = catalogos.index(catalogo)
            catalog = tables[i]
            c_data = col_data[i]

            connection = psycopg2.connect(user=db_User,
                                          password=db_Pass,
                                          host=db_Host,
                                          port=db_Port,
                                          database="cmdb_integracion")
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            
            # Consulta para verificar si el valor ya existe
            check = f"SELECT {c_data} FROM {catalog} WHERE {c_data} = %s"
            cursor.execute(check, (value,))
            result = cursor.fetchall()
            
            if result:
                errorcode = 1
                raise Exception("El valor ya existe en el catálogo.")
            
            # Inserción segura con valores parametrizados
            sql = f"INSERT INTO {catalog}({c_data}) VALUES (%s)"
            cursor.execute(sql, (value,))
            connection.commit()

        except psycopg2.DatabaseError as e:
            logging.error(f"[ERROR]: Error de base de datos: {e}")
            errormsg = jsonify(f"ERROR: No se pudo insertar el registro: {e}")
        except Exception as e:
            logging.error(f"[ERROR]: {e}")
            errormsg = jsonify(f"ERROR: {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()

        if errorcode != 0:
            return errormsg
        else: 
            return jsonify("¡Registro agregado correctamente!")

### solo se modifico la consulta sql
@cmdb.route('/cmdb/edit_catalog', methods=['POST'])
@require_api_key
def editCatalog():
    if request.method == 'POST':
        errorcode = 0
        errormsg = ""
        result = []
        connection = None
        id = (request.form.get('id').replace('"','')) 
        value = (request.form.get('value').replace('"','')) 
        catalogo = (request.form.get('cat').replace('"','')) 
        catalogos = ["Alojamiento", "Desarrollo", "Entorno", "Lenguaje", 
                    "Aplicacion", "Pais", "Proveedor", "Responsable", "Tipo Servidor",
                    "Esquema de Continuidad","Estrategias de Recuperación Infra",
                    "Estrategias de Recuperación Datos",
                    "Tiempo de Instalación (Servidor)",
                    "Tiempo de Instalación (Aplicación)","Joya de la Corona"]
        tables = ["cis_alojamiento", "cis_desarrollo", "cis_entorno_ci", 
                  "cis_lenguaje", "cis_nombre_aplicacion", "cis_pais_servidor",
                  "cis_proveedor", "cis_responsable_aplicacion", "cis_tipo_servidor",
                  "cis_esquema", "cis_estrategias_infra","cis_estrategias_datos",
                  "cis_tiempo_infra_servidor","cis_tiempo_infra_aplicacion",
                  "cis_joya"]
        col_id = ["ca_id", "cd_id", "cec_id", "cl_id", "cna_id", 
                  "cps_id", "cp_id", "cra_id", "cts_id", "ce_id"
                  , "cei_id", "ced_id", "ctis_id", "ctia_id", "cj_id"]
        col_data = ["ca_tipo_alojamiento", "cd_desarrollo", "cec_tipo", 
                  "cl_lenguaje", "cna_aplicacion", "cps_servidor", 
                  "cp_proveedor", "cra_mesa", "cts_tipo_servidor", "ce_esquema",
                  "cei_estrategias","ced_estrategias","ctis_tiempo","ctia_tiempo","cj_joya"]
        
        for i, cat in enumerate(catalogos):
            if cat == catalogo:
                catalog = tables[i]
                c_id = col_id[i]
                c_data = col_data[i]
                break
        try:
            sql = f"""
                    UPDATE {catalog}
                    SET {c_data} = %s
                    WHERE {c_id} = %s
                    """
            check = f"""
                    SELECT {c_data}
                    FROM {catalog}
                    WHERE {c_data} = %s
                    """
            connection = psycopg2.connect(user=db_User,
                                        password=db_Pass,
                                        host=db_Host,
                                        port=db_Port,
                                        database="cmdb_integracion")
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            # Valida que el dato no exista en la tabla
            cursor.execute(check)
            result = cursor.fetchall()
            if result != []:
                errorcode = 1
                raise Error
            # Actualiza la tabla
            cursor.execute(sql)
            connection.commit()
        except Error as e:
            if errorcode == 1:
                errormsg = jsonify("ERROR: El dato ya existe en el catalogo.")
                logging.info("ERROR: 1")
            else:
                logging.error(f"[ERROR]: Algo ha salido mal al intentar editar: {e.pgerror}")
        finally:
            if connection:
                cursor.close()
                connection.close()
    if errorcode != 0:
        return (errormsg)
    else: 
        return jsonify("Se edito el registro correctamente!")

#Se mofica completamente:

@cmdb.route('/cmdb/delete_catalog', methods=['POST'])
@require_api_key
def deleteCatalog():
    if request.method == 'POST':
        connection = None
    # Obtener valores del formulario
    id = request.form.get('id')
    catalogo = request.form.get('cat')

    if not id or not catalogo:
        return jsonify({"error": "Faltan parámetros"}), 400

    # Diccionario que mapea los catálogos a tablas y columnas
    catalog_map = {
        "Alojamiento": {"table": "cis_alojamiento", "id_col": "ca_id"},
        "Desarrollo": {"table": "cis_desarrollo", "id_col": "cd_id"},
        "Entorno": {"table": "cis_entorno_ci", "id_col": "cec_id"},
        # Agregar el resto de los catalogos aquí
    }

    # Validar que el catálogo exista
    catalog_info = catalog_map.get(catalogo)
    if not catalog_info:
        return jsonify({"error": "Catálogo no válido"}), 400

    table = catalog_info["table"]
    id_col = catalog_info["id_col"]

    try:
        sql = f"DELETE FROM {table} WHERE {id_col} = %s"

        # Conexión a la base de datos
        connection = psycopg2.connect(user=db_User,
                                      password=db_Pass,
                                      host=db_Host,
                                      port=db_Port,
                                      database="cmdb_integracion")
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        # Ejecutar la consulta SQL con parámetros
        cursor.execute(sql, (id,))
        connection.commit()

        # Verificar si se eliminó algún registro
        if cursor.rowcount == 0:
            return jsonify({"error": "No se encontró el registro"}), 404

    except psycopg2.DatabaseError as e:
        logging.error(f"[ERROR]: Algo ha salido mal al intentar eliminar: {str(e)}")
        return jsonify({"error": "Error en la base de datos"}), 500

    finally:
        if connection:
            cursor.close()
            connection.close()

    return jsonify({"message": "Se eliminó el registro correctamente!"}), 200
