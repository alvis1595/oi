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






##########################################################################}
CREATE OR REPLACE FUNCTION public.obtener_catalogos()
 RETURNS jsonb
 LANGUAGE plpgsql
AS $function$
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
        
        -- Agregar el resultado de la tabla al JSON finalita
        resultado := resultado 
        #|| jsonb_build_object(consulta, COALESCE(fila, '[]'::jsonb));
    END LOOP;    
    return resultado;
END;
$function$
################################################################################################################
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



#############################################################################################################
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
            cursor.execute ("SELECT obtener_catalogos();")
            result = cursor.fetchone()[0]  # Obtener el resultado en formato JSON
            
            result2.append(result)
            logging.info(json.dumps(result2))
        except Error as e:
            logging.error(f"[ERROR]: Algo ha salido mal: {e.pgerror}")
        finally:
            if connection:
                cursor.close()
                connection.close()
                
    return (result2 )

############################################################################################################

[[{"ca_id": 1, "ca_tipo_alojamiento": "On premise"}, {"ca_id": 20, "ca_tipo_alojamiento": "dosmas"}], [{"cd_id": 2,
"cd_desarrollo": "Proveedor Comercial"}, {"cd_id": 3, "cd_desarrollo": "Tercerizado"}, {"cd_id": 1, "cd_desarrollo":
"Propioa"}], [{"cec_id": 1, "cec_tipo": "Produccion"}, {"cec_id": 2, "cec_tipo": "Contingencia"}, {"cec_id": 3,
"cec_tipo": "Desarrollo"}, {"cec_id": 4, "cec_tipo": "Pruebas"}], [{"cl_id": 1, "cl_lenguaje": "ASP & HTML"}, {"cl_id":
2, "cl_lenguaje": "ASP, Vbscrip, Javascript, DLL en lenjuage C"}, {"cl_id": 3, "cl_lenguaje": "ASP.net"}, {"cl_id": 4,
"cl_lenguaje": "PL SQL (Oracle)"}, {"cl_id": 7, "cl_lenguaje": "HTML, ASP"}, {"cl_id": 8, "cl_lenguaje": "Java"},
{"cl_id": 14, "cl_lenguaje": "VisualBasic 6.0"}, {"cl_id": 5, "cl_lenguaje": "CLIPPER"}, {"cl_id": 6, "cl_lenguaje":
"COTS sin personalización"}, {"cl_id": 9, "cl_lenguaje": "Java, Java Servlets,GlassFish 2.1"}, {"cl_id": 10,
"cl_lenguaje": "Java, Visual Basic, .Net, Web Services"}, {"cl_id": 11, "cl_lenguaje": "Lenguaje C"}, {"cl_id": 13,
"cl_lenguaje": "Powerbuilder 10"}, {"cl_id": 15, "cl_lenguaje": "XML, webparts, HTML"}], [{"cna_id": 1,
"cna_aplicacion": "Acceso Remoto al Negocio (Citrix)", "cna_joya": "SI"}, {"cna_id": 2, "cna_aplicacion": "Acceso Seguro
a Equipos de Comunicaciones (Tacacs+)", "cna_joya": "NO"}, {"cna_id": 3, "cna_aplicacion": "Acceso Seguro a la Red
Corporativa (ISE – Identity Services Engine)", "cna_joya": "NO"}, {"cna_id": 4, "cna_aplicacion": "Administración
Centralizada de Impresión (Inepro - DocuPro)", "cna_joya": "NO"}, {"cna_id": 7, "cna_aplicacion": "Administración de
Custodio de Valores Internacional (Pershing)", "cna_joya": "NO"}, {"cna_id": 8, "cna_aplicacion": "Administración de
Diarios Electrónicos (SADE)", "cna_joya": "NO"}, {"cna_id": 11, "cna_aplicacion": "Administración de Portafolios de
Inversión (PAM)", "cna_joya": "NO"}, {"cna_id": 12, "cna_aplicacion": "Administración de Portafolios Internacionales
(Next360)", "cna_joya": "NO"}, {"cna_id": 13, "cna_aplicacion": "Administración de Riesgo Empresarial (Mega Hopex)",
"cna_joya": "NO"}, {"cna_id": 14, "cna_aplicacion": "Administración de Super Usuarios (Cyber Ark)", "cna_joya": "NO"},
{"cna_id": 15, "cna_aplicacion": "Administración de Tarjetas de Crédito (Masterdata)", "cna_joya": "NO"}, {"cna_id":
184, "cna_aplicacion": "Internet", "cna_joya": "NO"}, {"cna_id": 16, "cna_aplicacion": "Administración de Tarjetas de
Vale General (MasterData)", "cna_joya": "NO"}, {"cna_id": 17, "cna_aplicacion": "Administración de Zonas Seguras (Jump
Server)", "cna_joya": "NO"}, {"cna_id": 18, "cna_aplicacion": "Administración del Directorio Activo (Active Directory)",
"cna_joya": "NO"}, {"cna_id": 19, "cna_aplicacion": "Administración Empresarial (Flexio)", "cna_joya": "NO"}, {"cna_id":
21, "cna_aplicacion": "Almacenamiento Histórico (EMC – ECS Elastic Cloud Storage)", "cna_joya": "NO"}, {"cna_id": 23,
"cna_aplicacion": "Análisis de Portafolio de Clientes (Equalizer)", "cna_joya": "NO"}, {"cna_id": 31, "cna_aplicacion":
"Arquitectura de Datos (Dataedo)", "cna_joya": "NO"}, {"cna_id": 35, "cna_aplicacion": "ASF - Bloqueo de Productos
(Genexus)", "cna_joya": "NO"}, {"cna_id": 36, "cna_aplicacion": "ASF - Originación de Transacciones (Genexus)",
"cna_joya": "NO"}, {"cna_id": 38, "cna_aplicacion": "ASF - Reserva de manejo de efectivo (Genexus)", "cna_joya": "NO"},
{"cna_id": 39, "cna_aplicacion": "ASF -Tesorería Liquidez (Genexus)", "cna_joya": "NO"}, {"cna_id": 41,
"cna_aplicacion": "Auditoría Continua (ACL AX Exchange)", "cna_joya": "NO"}, {"cna_id": 42, "cna_aplicacion":
"Autenticación de Clientes (Entrust)", "cna_joya": "NO"}, {"cna_id": 47, "cna_aplicacion": "Automatización Robótica de
Procesos (Blue Prism)", "cna_joya": "NO"}, {"cna_id": 48, "cna_aplicacion": "Autorizador de Transacciones (BG
Autorizador)", "cna_joya": "NO"}, {"cna_id": 50, "cna_aplicacion": "Banca en línea (Liferay)", "cna_joya": "NO"},
{"cna_id": 51, "cna_aplicacion": "Banca en Línea Costa Rica (Liferay)", "cna_joya": "NO"}, {"cna_id": 52,
"cna_aplicacion": "Banca en Línea Overseas (Desarrollo Web)", "cna_joya": "NO"}, {"cna_id": 54, "cna_aplicacion": "Banca
Móvil Costa Rica (Amazon Web Service)", "cna_joya": "NO"}, {"cna_id": 55, "cna_aplicacion": "Banca Seguros", "cna_joya":
"NO"}, {"cna_id": 56, "cna_aplicacion": "Base de Datos - Oracle MIG (Oracle)", "cna_joya": "NO"}, {"cna_id": 58,
"cna_aplicacion": "Base de Datos Histórica (MySQL)", "cna_joya": "NO"}, {"cna_id": 61, "cna_aplicacion": "Base de Datos
Histórica (MySQL) - Cuentas Ahorros", "cna_joya": "NO"}, {"cna_id": 62, "cna_aplicacion": "Base de Datos Histórica
(MySQL) - Cuentas Corrientes", "cna_joya": "NO"}, {"cna_id": 65, "cna_aplicacion": "Bolsas a Consignación (FESA)",
"cna_joya": "NO"}, {"cna_id": 68, "cna_aplicacion": "Cámara de Compensación Automática (ACH)", "cna_joya": "NO"},
{"cna_id": 69, "cna_aplicacion": "Capa de Integración de Canales Electrónicos (Datapower)", "cna_joya": "NO"},
{"cna_id": 71, "cna_aplicacion": "Centro de Atención y Servicio (Genesys)", "cna_joya": "NO"}, {"cna_id": 73,
"cna_aplicacion": "Compra y Venta de Valores (CRIMS - Charles River)", "cna_joya": "NO"}, {"cna_id": 75,
"cna_aplicacion": "Comunicaciones Unificadas (CUCM - Call Manager)1", "cna_joya": "NO"}, {"cna_id": 76,
"cna_aplicacion": "Comunicaciones Unificadas CR", "cna_joya": "NO"}, {"cna_id": 78, "cna_aplicacion": "Conecciones a
Redes (Cisco AnyConnect)", "cna_joya": "NO"}, {"cna_id": 79, "cna_aplicacion": "Conectores Genéricos Stella (Liferay)",
"cna_joya": "NO"}, {"cna_id": 82, "cna_aplicacion": "Contabilidad (Eskema Cloud)", "cna_joya": "NO"}, {"cna_id": 83,
"cna_aplicacion": "Contabilidad (Visual Eskema)", "cna_joya": "NO"}, {"cna_id": 84, "cna_aplicacion": "Control de Acceso
a Oficinas (AxtraxNg)", "cna_joya": "NO"}, {"cna_id": 85, "cna_aplicacion": "Control de Llaves Físicas (Traka Web)",
"cna_joya": "NO"}, {"cna_id": 86, "cna_aplicacion": "Control de Versiones - Código Fuente ", "cna_joya": "NO"},
{"cna_id": 88, "cna_aplicacion": "Control de visitas (Welcome)", "cna_joya": "NO"}, {"cna_id": 89, "cna_aplicacion":
"Core Bancario (Cobis)", "cna_joya": "NO"}, {"cna_id": 94, "cna_aplicacion": "Core Bancario (Cobis) - Buzón",
"cna_joya": "NO"}, {"cna_id": 95, "cna_aplicacion": "Core Bancario (Cobis) - Cámara", "cna_joya": "NO"}, {"cna_id": 96,
"cna_aplicacion": "Core Bancario (Cobis) - Cartera", "cna_joya": "NO"}, {"cna_id": 97, "cna_aplicacion": "Core Bancario
(Cobis) - Comercio Exterior", "cna_joya": "NO"}, {"cna_id": 100, "cna_aplicacion": "Core Bancario (Cobis) - Corregi",
"cna_joya": "NO"}, {"cna_id": 101, "cna_aplicacion": "Core Bancario (Cobis) - Cuentas por Pagar", "cna_joya": "NO"},
{"cna_id": 102, "cna_aplicacion": "Core Bancario (Cobis) - Entes de Control", "cna_joya": "NO"}, {"cna_id": 103,
"cna_aplicacion": "Core Bancario (Cobis) - Firmas", "cna_joya": "NO"}, {"cna_id": 104, "cna_aplicacion": "Core Bancario
(Cobis) - Garantías", "cna_joya": "NO"}, {"cna_id": 105, "cna_aplicacion": "Core Bancario (Cobis) - Gestión de Crédito",
"cna_joya": "NO"}, {"cna_id": 107, "cna_aplicacion": "Core Bancario (Cobis) - Overseas", "cna_joya": "NO"}, {"cna_id":
109, "cna_aplicacion": "Core Bancario (Cobis) - Plazo Fijo", "cna_joya": "NO"}, {"cna_id": 112, "cna_aplicacion": "Core
Bancario (Cobis) - Servicios Bancarios", "cna_joya": "NO"}, {"cna_id": 114, "cna_aplicacion": "Core Bancario (Cobis) -
Tadmin", "cna_joya": "NO"}, {"cna_id": 115, "cna_aplicacion": "Core Bancario (Cobis) - Trámites de Crédito", "cna_joya":
"NO"}, {"cna_id": 118, "cna_aplicacion": "Core de IDC en Producción (Fortinet Fortigate)", "cna_joya": "NO"}, {"cna_id":
119, "cna_aplicacion": "Correo Electrónico (Exchange)", "cna_joya": "NO"}, {"cna_id": 122, "cna_aplicacion": "Despliegue
de Aplicaciones de Stella (Docker)", "cna_joya": "NO"}, {"cna_id": 123, "cna_aplicacion": "Detección y protección contra
vulnerabilidades (Deep Security)", "cna_joya": "NO"}, {"cna_id": 124, "cna_aplicacion": "Diseños Arquitectónicos
(Autodesk)", "cna_joya": "NO"}, {"cna_id": 126, "cna_aplicacion": "E-Commerce (Desarrollo Web)", "cna_joya": "NO"},
{"cna_id": 128, "cna_aplicacion": "Enmascaramiento de Datos (Test Data Management)", "cna_joya": "NO"}, {"cna_id": 129,
"cna_aplicacion": "Entidad Registradora Pagadora del SIACAP (P2000)", "cna_joya": "NO"}, {"cna_id": 130,
"cna_aplicacion": "Equipos de Seguridad de la Información", "cna_joya": "NO"}, {"cna_id": 136, "cna_aplicacion":
"Finanzas Generales", "cna_joya": "NO"}, {"cna_id": 138, "cna_aplicacion": "Firmas Autorizadas de Colaboradores BG
(Desarrollo Web)", "cna_joya": "NO"}, {"cna_id": 139, "cna_aplicacion": "FlexDesk - Virtualización de Estaciones (VMWare
Horizon)", "cna_joya": "NO"}, {"cna_id": 143, "cna_aplicacion": "Generación de Pines para Tarjetas (ARH)", "cna_joya":
"NO"}, {"cna_id": 147, "cna_aplicacion": "General", "cna_joya": "NO"}, {"cna_id": 148, "cna_aplicacion": "General de
Seguros (Microsoft Azure)", "cna_joya": "NO"}, {"cna_id": 150, "cna_aplicacion": "Gestión automatizada de Identidades y
Accesos de Usuarios (Desarrollo Web)", "cna_joya": "NO"}, {"cna_id": 153, "cna_aplicacion": "Gestión de Casos de
Clientes (Engage)", "cna_joya": "NO"}, {"cna_id": 155, "cna_aplicacion": "Gestión de comunicaciones masivas - OMNI (IC
Banking Campaigns)", "cna_joya": "NO"}, {"cna_id": 156, "cna_aplicacion": "Gestión de Datos Empresariales (SAP Data
Services)", "cna_joya": "NO"}, {"cna_id": 158, "cna_aplicacion": "Gestión de Incidentes de Crédito (Desarrollo Web)",
"cna_joya": "NO"}, {"cna_id": 159, "cna_aplicacion": "Gestión de Riesgo de Crédito (CreditLens)", "cna_joya": "NO"},
{"cna_id": 161, "cna_aplicacion": "Gestión de servicios de TI (Jira Service Management)", "cna_joya": "NO"}, {"cna_id":
163, "cna_aplicacion": "Gestión Empresarial de Descuento Directo(GeneXus)", "cna_joya": "NO"}, {"cna_id": 165,
"cna_aplicacion": "GH - Gestión Humana (Talentia)", "cna_joya": "NO"}, {"cna_id": 166, "cna_aplicacion": "Gobierno
Digital (Merlink)", "cna_joya": "NO"}, {"cna_id": 169, "cna_aplicacion": "Herramientas DevSecOps", "cna_joya": "NO"},
{"cna_id": 170, "cna_aplicacion": "Históricos BG (Genexus)", "cna_joya": "NO"}, {"cna_id": 173, "cna_aplicacion":
"Información de Datos de Mercado (IDC)", "cna_joya": "NO"}, {"cna_id": 174, "cna_aplicacion": "Informe Único de Seguros
(INUSE)", "cna_joya": "NO"}, {"cna_id": 176, "cna_aplicacion": "Infraestructura de Comunicaciones y Redes - Centro
Operativo", "cna_joya": "NO"}, {"cna_id": 182, "cna_aplicacion": "Interfaz Cobis (Bloomberg)", "cna_joya": "NO"},
{"cna_id": 186, "cna_aplicacion": "Manejador de Tráfico de DNS (Traffic Manager)", "cna_joya": "NO"}, {"cna_id": 188,
"cna_aplicacion": "Métricas de licenciamiento (IBM License Metric Tool)", "cna_joya": "NO"}, {"cna_id": 189,
"cna_aplicacion": "Modelo de Información Gerencial (MicroStrategy)", "cna_joya": "NO"}, {"cna_id": 191,
"cna_aplicacion": "Monitoreo de Base de datos (SQL Server Monitoring Solution)", "cna_joya": "NO"}, {"cna_id": 193,
"cna_aplicacion": "Monitoreo de Desempeño de Stella (Dynatrace)", "cna_joya": "NO"}, {"cna_id": 194, "cna_aplicacion":
"Monitoreo de enlaces de comunicaciones (Cacti)", "cna_joya": "NO"}, {"cna_id": 198, "cna_aplicacion": "Monitoreo de
Sybase ASE (ASEMON)", "cna_joya": "NO"}, {"cna_id": 201, "cna_aplicacion": "Monitoreo Transaccional del Cliente CR
(Assist)", "cna_joya": "NO"}, {"cna_id": 203, "cna_aplicacion": "Monitoreo y Auditoria de Base de Datos (Imperva
SecureSphere)", "cna_joya": "NO"}, {"cna_id": 206, "cna_aplicacion": "Negociación de Bolsa de Valores El Salvador
(SEN)", "cna_joya": "NO"}, {"cna_id": 207, "cna_aplicacion": "Notificaciones de Transacciones con Tarjetas de Crédito
(LIMSP)", "cna_joya": "NO"}, {"cna_id": 209, "cna_aplicacion": "Originación de Crédito Hipotecario (ASICOM)",
"cna_joya": "NO"}, {"cna_id": 210, "cna_aplicacion": "Pago de Dividendos y Planilla ACP", "cna_joya": "NO"}, {"cna_id":
211, "cna_aplicacion": "Perímetro de Desarrollo y Pruebas", "cna_joya": "NO"}, {"cna_id": 214, "cna_aplicacion":
"Planificación y Consolidación presupuestaria (SAP - BPC)", "cna_joya": "NO"}, {"cna_id": 215, "cna_aplicacion":
"Plataforma de Gestión y Cobranza (Emerix)", "cna_joya": "NO"}, {"cna_id": 218, "cna_aplicacion": "Plataforma de Mesa de
Servicios (BMC - Remedy)", "cna_joya": "NO"}, {"cna_id": 220, "cna_aplicacion": "Plataforma de Servicio y Ventas PMA
(Peoplesoft)", "cna_joya": "NO"}, {"cna_id": 222, "cna_aplicacion": "Plataforma de Servicios y Ventas CR (Peoplesoft)",
"cna_joya": "NO"}, {"cna_id": 224, "cna_aplicacion": "Procesador de Pagos E-Commerce con Tarjetas de Crédito (BG
Unity)", "cna_joya": "NO"}, {"cna_id": 228, "cna_aplicacion": "Profuturo (Microsoft Azure)", "cna_joya": "NO"},
{"cna_id": 230, "cna_aplicacion": "Protección automatizada de datos (Cyber Recovery Solution)", "cna_joya": "NO"},
{"cna_id": 233, "cna_aplicacion": "Punto Yappy (Amazon Web Service)", "cna_joya": "NO"}, {"cna_id": 235,
"cna_aplicacion": "Red Inalámbrica Segura (Aruba Network)", "cna_joya": "NO"}, {"cna_id": 236, "cna_aplicacion":
"Referencias de Crédito APC", "cna_joya": "NO"}, {"cna_id": 239, "cna_aplicacion": "Replicador de Sybase (SAP)",
"cna_joya": "NO"}, {"cna_id": 240, "cna_aplicacion": "Reporteador de INXU Core (SAP Business Objects)", "cna_joya":
"NO"}, {"cna_id": 242, "cna_aplicacion": "Reportes de Mercado de Valores (Cognos)", "cna_joya": "NO"}, {"cna_id": 244,
"cna_aplicacion": "Respaldo de Estaciones de Usuarios (IDPA - Integrated Data Protection Appliance)", "cna_joya": "NO"},
{"cna_id": 245, "cna_aplicacion": "Respaldo de Estaciones de Usuarios CR (EMC - Avamar Business Edition)", "cna_joya":
"NO"}, {"cna_id": 249, "cna_aplicacion": "Seguridad de Acceso a la nube (McAfee - MVISION Cloud CASB)", "cna_joya":
"NO"}, {"cna_id": 250, "cna_aplicacion": "Servidor APPX - La Hipotecaria", "cna_joya": "NO"}, {"cna_id": 251,
"cna_aplicacion": "Sistema Integrador de Entidades Financieras (BGCR)", "cna_joya": "NO"}, {"cna_id": 252,
"cna_aplicacion": "Sistema Integrador de Entidades Financieras (BGCR)", "cna_joya": "NO"}, {"cna_id": 253,
"cna_aplicacion": "Sistema Operativo - AIX (IBM )", "cna_joya": "NO"}, {"cna_id": 256, "cna_aplicacion": "Sitio Alterno
de Continuidad de Negocios", "cna_joya": "NO"}, {"cna_id": 257, "cna_aplicacion": "Sitio Público Costa Rica (Microsoft
Azure)", "cna_joya": "NO"}, {"cna_id": 259, "cna_aplicacion": "Soporte Remoto ( Team Viewer)", "cna_joya": "NO"},
{"cna_id": 261, "cna_aplicacion": "Stella - ACH (Liferay)", "cna_joya": "NO"}, {"cna_id": 262, "cna_aplicacion": "Stella
- ATM (Liferay)", "cna_joya": "NO"}, {"cna_id": 264, "cna_aplicacion": "Stella - Cámara (Liferay)", "cna_joya": "NO"},
{"cna_id": 266, "cna_aplicacion": "Stella - Cobranzas (Liferay)", "cna_joya": "NO"}, {"cna_id": 267, "cna_aplicacion":
"Stella - Comercio Exterior (Liferay)", "cna_joya": "NO"}, {"cna_id": 269, "cna_aplicacion": "Stella - Cuentas por Pagar
(Liferay)", "cna_joya": "NO"}, {"cna_id": 270, "cna_aplicacion": "Stella - Garantías (Liferay)", "cna_joya": "NO"},
{"cna_id": 271, "cna_aplicacion": "Stella - Gestión de Crédito (Liferay)", "cna_joya": "NO"}, {"cna_id": 272,
"cna_aplicacion": "Stella - MIS (Liferay)", "cna_joya": "NO"}, {"cna_id": 275, "cna_aplicacion": "Stella - Programa
Estrellas (Liferay)", "cna_joya": "NO"}, {"cna_id": 276, "cna_aplicacion": "Stella - Referencias (Liferay)", "cna_joya":
"NO"}, {"cna_id": 278, "cna_aplicacion": "Stella - Terminal Administrativa (Liferay)", "cna_joya": "NO"}, {"cna_id":
279, "cna_aplicacion": "Stella - Trámite Empresarial (Liferay)", "cna_joya": "NO"}, {"cna_id": 280, "cna_aplicacion":
"Stella (Liferay)", "cna_joya": "NO"}, {"cna_id": 283, "cna_aplicacion": "Transferencias Internacionales (Swift
Alliance)", "cna_joya": "NO"}, {"cna_id": 285, "cna_aplicacion": "Ventas Digitales (Amazon Web Service)", "cna_joya":
"NO"}, {"cna_id": 288, "cna_aplicacion": "Videoconferencia (Cisco Videoconferencia)", "cna_joya": "NO"}, {"cna_id": 291,
"cna_aplicacion": "Virtualización de Servidores Microsoft (Hyper V)", "cna_joya": "NO"}, {"cna_id": 299,
"cna_aplicacion": "Gestor de contenido en Pantallas (MagicInfo)", "cna_joya": "NO"}, {"cna_id": 301, "cna_aplicacion":
"Gestión de seguridad de Infraestructuras en la nube (Tenable Cloud Security)", "cna_joya": "NO"}, {"cna_id": 5,
"cna_aplicacion": "Administración de Átomos para SIB (ADMINSIB)", "cna_joya": "NO"}, {"cna_id": 6, "cna_aplicacion":
"Administración de Auditorías (TeamMate)", "cna_joya": "NO"}, {"cna_id": 9, "cna_aplicacion": "Administración de
Estaciones (Client Management)", "cna_joya": "NO"}, {"cna_id": 10, "cna_aplicacion": "Administración de Fondos de
Pensión y Cesantías (P2000)", "cna_joya": "NO"}, {"cna_id": 20, "cna_aplicacion": "Administración Financiera (CODISA
NAF) ", "cna_joya": "NO"}, {"cna_id": 22, "cna_aplicacion": "Análisis Centralizado de Bitácoras (Elastic Stack)",
"cna_joya": "NO"}, {"cna_id": 24, "cna_aplicacion": "Análisis e Inteligencia de Datos (Tableau)", "cna_joya": "NO"},
{"cna_id": 25, "cna_aplicacion": "Análisis Financieros (Bancware - ALM)", "cna_joya": "NO"}, {"cna_id": 26,
"cna_aplicacion": "Análisis Financieros (Bancware - Data Integration)", "cna_joya": "NO"}, {"cna_id": 27,
"cna_aplicacion": "Análisis y Riesgo de Inversiones (Aladdin)", "cna_joya": "NO"}, {"cna_id": 28, "cna_aplicacion":
"Antivirus (McAfee)", "cna_joya": "NO"}, {"cna_id": 29, "cna_aplicacion": "Antivirus (Trellix MVISION ePO)", "cna_joya":
"NO"}, {"cna_id": 30, "cna_aplicacion": "Antivirus en Dispositivos Móviles (McAfee Mvision Mobile)", "cna_joya": "NO"},
{"cna_id": 32, "cna_aplicacion": "Arquitectura Empresarial (Hopex)", "cna_joya": "NO"}, {"cna_id": 33, "cna_aplicacion":
"ASF - Administración de Saldos de Cajeros Automáticos (Genexus)", "cna_joya": "NO"}, {"cna_id": 34, "cna_aplicacion":
"ASF - Aplicaciones de Soporte y Finanzas (Genexus)", "cna_joya": "NO"}, {"cna_id": 37, "cna_aplicacion": "ASF - Pagos
MEF (Genexus)", "cna_joya": "NO"}, {"cna_id": 40, "cna_aplicacion": "ATM (Servicios)", "cna_joya": "NO"}, {"cna_id": 43,
"cna_aplicacion": "Autenticación de Clientes (Transmit Security)", "cna_joya": "NO"}, {"cna_id": 44, "cna_aplicacion":
"Autenticación de Usuarios (RSA Authentication Manager)", "cna_joya": "NO"}, {"cna_id": 45, "cna_aplicacion":
"Automatización de procesos nocturnos (BMC Control M)", "cna_joya": "NO"}, {"cna_id": 46, "cna_aplicacion":
"Automatización Robótica de Mensajería (Chatbot)", "cna_joya": "NO"}, {"cna_id": 49, "cna_aplicacion": "Banca Abierta
(IBM Integration BUS)", "cna_joya": "NO"}, {"cna_id": 53, "cna_aplicacion": "Banca Móvil (Amazon Web Service)",
"cna_joya": "NO"}, {"cna_id": 57, "cna_aplicacion": "Base de Datos - SAP IQ DWH MIG (SAP)", "cna_joya": "NO"},
{"cna_id": 59, "cna_aplicacion": "Base de Datos Histórica (MySQL) - Canales", "cna_joya": "NO"}, {"cna_id": 60,
"cna_aplicacion": "Base de Datos Histórica (MySQL) - Cartera", "cna_joya": "NO"}, {"cna_id": 63, "cna_aplicacion": "Base
de Datos MySQL(Stella)", "cna_joya": "NO"}, {"cna_id": 64, "cna_aplicacion": "BG LAB - Análisis Predictivo de Datos
(Python)", "cna_joya": "NO"}, {"cna_id": 66, "cna_aplicacion": "Branch Departamentales", "cna_joya": "NO"}, {"cna_id":
67, "cna_aplicacion": "Branch Sucursales", "cna_joya": "NO"}, {"cna_id": 70, "cna_aplicacion": "Carpeta Única del
Cliente (Onbase)", "cna_joya": "NO"}, {"cna_id": 72, "cna_aplicacion": "Chat del Sitio Público (LivePerson)",
"cna_joya": "NO"}, {"cna_id": 74, "cna_aplicacion": "Comunicaciones Unificadas (CUCM - Call Manager)", "cna_joya":
"NO"}, {"cna_id": 77, "cna_aplicacion": "Conciliación Bancaria (Syc Conciliaciones)", "cna_joya": "NO"}, {"cna_id": 80,
"cna_aplicacion": "Conexión BG (Json)", "cna_joya": "NO"}, {"cna_id": 81, "cna_aplicacion": "Consolidaciones Financieras
(Holding)", "cna_joya": "NO"}, {"cna_id": 87, "cna_aplicacion": "Control de Versiones (Desarrollo Web)", "cna_joya":
"NO"}, {"cna_id": 90, "cna_aplicacion": "Core Bancario (Cobis) - Admin", "cna_joya": "NO"}, {"cna_id": 91,
"cna_aplicacion": "Core Bancario (Cobis) - Administrador de Crédito", "cna_joya": "NO"}, {"cna_id": 92,
"cna_aplicacion": "Core Bancario (Cobis) - BGCR", "cna_joya": "NO"}, {"cna_id": 93, "cna_aplicacion": "Core Bancario
(Cobis) - Branch Administrador", "cna_joya": "NO"}, {"cna_id": 98, "cna_aplicacion": "Core Bancario (Cobis) -
Contabilidad", "cna_joya": "NO"}, {"cna_id": 99, "cna_aplicacion": "Core Bancario (Cobis) - Core Server", "cna_joya":
"NO"}, {"cna_id": 106, "cna_aplicacion": "Core Bancario (Cobis) - Kernel", "cna_joya": "NO"}, {"cna_id": 108,
"cna_aplicacion": "Core Bancario (Cobis) - Personalización", "cna_joya": "NO"}, {"cna_id": 110, "cna_aplicacion": "Core
Bancario (Cobis) - Referencia de Crédito", "cna_joya": "NO"}, {"cna_id": 111, "cna_aplicacion": "Core Bancario (Cobis) -
Seguridad", "cna_joya": "NO"}, {"cna_id": 113, "cna_aplicacion": "Core Bancario (Cobis) - SP", "cna_joya": "NO"},
{"cna_id": 116, "cna_aplicacion": "Core Bancario (Cobis) - TS", "cna_joya": "NO"}, {"cna_id": 117, "cna_aplicacion":
"Core Bancario (Cobis) - Visa Estrella", "cna_joya": "NO"}, {"cna_id": 120, "cna_aplicacion": "Creación Digital de
Clientes (Amazon Web Service)", "cna_joya": "NO"}, {"cna_id": 121, "cna_aplicacion": "Custodia y Administración de
Valores de LatinClear (Sicus)", "cna_joya": "NO"}, {"cna_id": 125, "cna_aplicacion": "Distribución de Tarjetas de
Crédito (Onbase)", "cna_joya": "NO"}, {"cna_id": 127, "cna_aplicacion": "Empresa General de Inversiones (Microsoft
Azure)", "cna_joya": "NO"}, {"cna_id": 131, "cna_aplicacion": "Escaneo de Vulnerabilidades (Nessus Vulnerability Scanner
)", "cna_joya": "NO"}, {"cna_id": 132, "cna_aplicacion": "Facturación electrónica DGI (WebPos)", "cna_joya": "NO"},
{"cna_id": 133, "cna_aplicacion": "File Server (Microsoft)", "cna_joya": "NO"}, {"cna_id": 134, "cna_aplicacion":
"Filtro de Correo Electrónico (MailMarshal)", "cna_joya": "NO"}, {"cna_id": 135, "cna_aplicacion": "Filtro de Navegación
de Internet (Forcepoint)", "cna_joya": "NO"}, {"cna_id": 137, "cna_aplicacion": "Firma electrónica automatizada
(Signbox)", "cna_joya": "NO"}, {"cna_id": 140, "cna_aplicacion": "Flujos de Consumo AID (Onbase)", "cna_joya": "NO"},
{"cna_id": 141, "cna_aplicacion": "Flujos e Imágenes (Onbase)", "cna_joya": "NO"}, {"cna_id": 142, "cna_aplicacion":
"Fundación Sus Buenos Vecinos (Microsoft Azure)", "cna_joya": "NO"}, {"cna_id": 144, "cna_aplicacion": "Generación de
Reportes FATCA y CRS (Avantica)", "cna_joya": "NO"}, {"cna_id": 145, "cna_aplicacion": "Generación y envío de Informes
SUGEF (Gnosis)", "cna_joya": "NO"}, {"cna_id": 146, "cna_aplicacion": "Generador de Documentos (Ecrion)", "cna_joya":
"NO"}, {"cna_id": 149, "cna_aplicacion": "Gestión Administrativa (Spyral)", "cna_joya": "NO"}, {"cna_id": 151,
"cna_aplicacion": "Gestión Automatizada de Parches (Patch Manager Plus)", "cna_joya": "NO"}, {"cna_id": 152,
"cna_aplicacion": "Gestión de Aprendizaje (NetDimension - Learning)", "cna_joya": "NO"}, {"cna_id": 154,
"cna_aplicacion": "Gestión de Cobros (Recovery)", "cna_joya": "NO"}, {"cna_id": 157, "cna_aplicacion": "Gestión de DNS
Externo (BIND DNS Server)", "cna_joya": "NO"}, {"cna_id": 160, "cna_aplicacion": "Gestión de Seguros (INXU Core)",
"cna_joya": "NO"}, {"cna_id": 162, "cna_aplicacion": "Gestión Documental de Clientes (Onbase)", "cna_joya": "NO"},
{"cna_id": 164, "cna_aplicacion": "Gestor de Contenido en Pantallas (Navori QL)", "cna_joya": "NO"}, {"cna_id": 167,
"cna_aplicacion": "Grabación de llamadas Telefónicas (Nice Call)", "cna_joya": "NO"}, {"cna_id": 168, "cna_aplicacion":
"Grabación de Llamadas Telefónicas (Redbox)", "cna_joya": "NO"}, {"cna_id": 171, "cna_aplicacion": "Históricos de
Correos Sensitivos (Barracuda)", "cna_joya": "NO"}, {"cna_id": 172, "cna_aplicacion": "IBM Datapower Gateway Stella
(Liferay)", "cna_joya": "NO"}, {"cna_id": 175, "cna_aplicacion": "Infraestructura de Almacenamiento (V7000)",
"cna_joya": "NO"}, {"cna_id": 177, "cna_aplicacion": "Infraestructura de Identity Services Engine ( ISE) - Centro
Operativo", "cna_joya": "NO"}, {"cna_id": 178, "cna_aplicacion": "Infraestructura en la Nube (Microsoft Azure)",
"cna_joya": "NO"}, {"cna_id": 179, "cna_aplicacion": "Integración de Cámara de Compensación Automática ACH (Montran
Gateway)", "cna_joya": "NO"}, {"cna_id": 180, "cna_aplicacion": "Intercambio Digital Seguro (EFT Server)", "cna_joya":
"NO"}, {"cna_id": 181, "cna_aplicacion": "Intercambio y Transferencia Masiva (Sterling File Gateway)", "cna_joya":
"NO"}, {"cna_id": 183, "cna_aplicacion": "Interfaz de Portafolios de Inversión Administrados (Black Rock)", "cna_joya":
"NO"}, {"cna_id": 185, "cna_aplicacion": "Kernel Core Bancario (Cobis)", "cna_joya": "NO"}, {"cna_id": 187,
"cna_aplicacion": "MAPTOOL (Microsoft Assessment and Planning Toolkit)", "cna_joya": "NO"}, {"cna_id": 190,
"cna_aplicacion": "Modelo de Información Gerencial Profuturo (QlikView)", "cna_joya": "NO"}, {"cna_id": 192,
"cna_aplicacion": "Monitoreo de Desempeño de Banca en Línea (Dynatrace)", "cna_joya": "NO"}, {"cna_id": 195,
"cna_aplicacion": "Monitoreo de Información y Administración de Eventos (SIEM)", "cna_joya": "NO"}, {"cna_id": 196,
"cna_aplicacion": "Monitoreo de Infraestructuras de TI (Zabbix)", "cna_joya": "NO"}, {"cna_id": 197, "cna_aplicacion":
"Monitoreo de Redes (Orion)", "cna_joya": "NO"}, {"cna_id": 199, "cna_aplicacion": "Monitoreo de Transferencias del
Cliente (Safewatch)", "cna_joya": "NO"}, {"cna_id": 200, "cna_aplicacion": "Monitoreo para Reducción de Eventos (Ares)",
"cna_joya": "NO"}, {"cna_id": 202, "cna_aplicacion": "Monitoreo Transaccional del Cliente PMA (Assist)", "cna_joya":
"NO"}, {"cna_id": 204, "cna_aplicacion": "Motor de Reglas (IBM ODM)", "cna_joya": "NO"}, {"cna_id": 205,
"cna_aplicacion": "Navisworks Freedom (Autodesk)", "cna_joya": "NO"}, {"cna_id": 208, "cna_aplicacion": "Ofimática en la
Nube (Microsoft 365)", "cna_joya": "NO"}, {"cna_id": 212, "cna_aplicacion": "Perímetro de Producción (Fortinet
Management and Analytics)", "cna_joya": "NO"}, {"cna_id": 213, "cna_aplicacion": "Planes de Contingencia", "cna_joya":
"NO"}, {"cna_id": 216, "cna_aplicacion": "Plataforma de Integración (ACE - App Connect Enterprise)", "cna_joya": "NO"},
{"cna_id": 217, "cna_aplicacion": "Plataforma de Integración (Cobis TS)", "cna_joya": "NO"}, {"cna_id": 219,
"cna_aplicacion": "Plataforma de Prevención de fraude (Monitor Plus)", "cna_joya": "NO"}, {"cna_id": 221,
"cna_aplicacion": "Plataforma de Servicios Electrónicos (PEL)", "cna_joya": "NO"}, {"cna_id": 223, "cna_aplicacion":
"Prevención y Detección de Intrusos (Instrusion Prevention System)", "cna_joya": "NO"}, {"cna_id": 225,
"cna_aplicacion": "Procesador de Servicios (Cobis SP)", "cna_joya": "NO"}, {"cna_id": 226, "cna_aplicacion": "Procesador
de Transacciones de Tarjetas (ATH)", "cna_joya": "NO"}, {"cna_id": 227, "cna_aplicacion": "Procesamiento y Devolución de
Cheques (Aperta)", "cna_joya": "NO"}, {"cna_id": 229, "cna_aplicacion": "Programación de Procesos Batch (Groovy)",
"cna_joya": "NO"}, {"cna_id": 231, "cna_aplicacion": "Protección contra ataques de negación de servicios (DDoS)",
"cna_joya": "NO"}, {"cna_id": 232, "cna_aplicacion": "Pruebas Automatizadas (Rational)", "cna_joya": "NO"}, {"cna_id":
234, "cna_aplicacion": "Red de Almacenamiento Directores MDS (Cisco)", "cna_joya": "NO"}, {"cna_id": 237,
"cna_aplicacion": "Relojes de Marcación (Kronos)", "cna_joya": "NO"}, {"cna_id": 238, "cna_aplicacion": "Replicador de
Base de Datos (SQL - Oracle)", "cna_joya": "NO"}, {"cna_id": 241, "cna_aplicacion": "Reporteador de Visual Eskema
(QlikView)", "cna_joya": "NO"}, {"cna_id": 243, "cna_aplicacion": "Respaldo de Estaciones de Usuarios (EMC - Avamar
Business Edition)", "cna_joya": "NO"}, {"cna_id": 246, "cna_aplicacion": "Respaldo de Servidores (EMC - Avamar Rain)",
"cna_joya": "NO"}, {"cna_id": 247, "cna_aplicacion": "Revista En Exclusiva (Microsoft Azure)", "cna_joya": "NO"},
{"cna_id": 248, "cna_aplicacion": "Salones de Reuniones Virtuales (Cisco WebEx)", "cna_joya": "NO"}, {"cna_id": 254,
"cna_aplicacion": "Sistema Operativo - Red Hat (Red Hat)", "cna_joya": "NO"}, {"cna_id": 255, "cna_aplicacion": "Sistema
Operativo - Solaris (Oracle)", "cna_joya": "NO"}, {"cna_id": 258, "cna_aplicacion": "Sitio Público Panamá (Microsoft
Azure)", "cna_joya": "NO"}, {"cna_id": 260, "cna_aplicacion": "Spyral - Gestión Administrativa", "cna_joya": "NO"},
{"cna_id": 263, "cna_aplicacion": "Stella - Banca Virtual (Liferay)", "cna_joya": "NO"}, {"cna_id": 265,
"cna_aplicacion": "Stella - Cartera (Liferay)", "cna_joya": "NO"}, {"cna_id": 268, "cna_aplicacion": "Stella - Control
de incidentes (Liferay)", "cna_joya": "NO"}, {"cna_id": 273, "cna_aplicacion": "Stella - Operaciones de Inversiones
Banca Patrimonial (Liferay)", "cna_joya": "NO"}, {"cna_id": 274, "cna_aplicacion": "Stella - Plazo Fijo (Liferay)",
"cna_joya": "NO"}, {"cna_id": 277, "cna_aplicacion": "Stella - Servicios Bancarios (Liferay)", "cna_joya": "NO"},
{"cna_id": 281, "cna_aplicacion": "Suite BG", "cna_joya": "NO"}, {"cna_id": 282, "cna_aplicacion": "Transacciones
Electrónicas de Bolsa de Valores Pmá (Nasdaq)", "cna_joya": "NO"}, {"cna_id": 284, "cna_aplicacion": "Vale General
(Microsoft Azure)", "cna_joya": "NO"}, {"cna_id": 286, "cna_aplicacion": "Verificación de precios de acciones (Bloomberg
Gateway)", "cna_joya": "NO"}, {"cna_id": 287, "cna_aplicacion": "Veritas Netbackup", "cna_joya": "NO"}, {"cna_id": 289,
"cna_aplicacion": "Virtualización de Servidores (Red Hat)", "cna_joya": "NO"}, {"cna_id": 290, "cna_aplicacion":
"Virtualización de Servidores (VMWare)", "cna_joya": "NO"}, {"cna_id": 292, "cna_aplicacion": "Windows Deployment
Services", "cna_joya": "NO"}, {"cna_id": 293, "cna_aplicacion": "Yappy (Amazon Web Service)", "cna_joya": "NO"},
{"cna_id": 294, "cna_aplicacion": "Yappy + (Amazon Web Service)", "cna_joya": "NO"}, {"cna_id": 295, "cna_aplicacion":
"Yappy web (Microsoft Azure)", "cna_joya": "NO"}, {"cna_id": 296, "cna_aplicacion": "Stella - Administrador Comercio
Exterior (Liferay)", "cna_joya": "NO"}, {"cna_id": 297, "cna_aplicacion": "Red de distribución de contenidos en la nube
(Azure Front Door)", "cna_joya": "NO"}, {"cna_id": 298, "cna_aplicacion": "Gestión de pagos a proveedores (Confirming)",
"cna_joya": "NO"}, {"cna_id": 300, "cna_aplicacion": "Infraestructura", "cna_joya": "NO"}, {"cna_id": 302,
"cna_aplicacion": "Gestión de token para tarjetas (HST Pay Admin - APIs)", "cna_joya": "NO"}], [{"cps_id": 1,
"cps_servidor": "Panamá"}, {"cps_id": 2, "cps_servidor": "Costa Rica"}, {"cps_id": 3, "cps_servidor": "BG Valores"},
{"cps_id": 4, "cps_servidor": "General de Seguros"}, {"cps_id": 5, "cps_servidor": "Profuturo"}, {"cps_id": 6,
"cps_servidor": "Regionales"}, {"cps_id": 7, "cps_servidor": "Vale General"}, {"cps_id": 8, "cps_servidor": "Fundacion
sus Buenos Vecinos"}, {"cps_id": 9, "cps_servidor": "Yappy"}], [{"cp_id": 2, "cp_proveedor": "Airwatch"}, {"cp_id": 3,
"cp_proveedor": "Aperta"}, {"cp_id": 4, "cp_proveedor": "Arango Software"}, {"cp_id": 8, "cp_proveedor": "Banco
General"}, {"cp_id": 9, "cp_proveedor": "Bloomberg"}, {"cp_id": 10, "cp_proveedor": "Blue Prism"}, {"cp_id": 12,
"cp_proveedor": "Cable & Wireles Business"}, {"cp_id": 19, "cp_proveedor": "Compulab"}, {"cp_id": 20, "cp_proveedor":
"DeSimplex"}, {"cp_id": 21, "cp_proveedor": "Dvelop"}, {"cp_id": 22, "cp_proveedor": "Dynatrace"}, {"cp_id": 25,
"cp_proveedor": "EMC"}, {"cp_id": 28, "cp_proveedor": "Equalizer"}, {"cp_id": 32, "cp_proveedor": "First Data"},
{"cp_id": 33, "cp_proveedor": "GATI"}, {"cp_id": 34, "cp_proveedor": "GBM"}, {"cp_id": 35, "cp_proveedor": "Genesys"},
{"cp_id": 36, "cp_proveedor": "Global Advisory Solutions"}, {"cp_id": 37, "cp_proveedor": "Grupo Babel"}, {"cp_id": 43,
"cp_proveedor": "Infocorpgroup"}, {"cp_id": 45, "cp_proveedor": "Intelector / Global Scape"}, {"cp_id": 48,
"cp_proveedor": "Latinia"}, {"cp_id": 49, "cp_proveedor": "Liferay"}, {"cp_id": 50, "cp_proveedor": "Magicinfo"},
{"cp_id": 52, "cp_proveedor": "microstrategy"}, {"cp_id": 55, "cp_proveedor": "Monitise"}, {"cp_id": 56, "cp_proveedor":
"Montran"}, {"cp_id": 62, "cp_proveedor": "PEL"}, {"cp_id": 64, "cp_proveedor": "Princeton Financials"}, {"cp_id": 65,
"cp_proveedor": "Prodic"}, {"cp_id": 69, "cp_proveedor": "Redbox"}, {"cp_id": 72, "cp_proveedor": "SIDE - BCG"},
{"cp_id": 73, "cp_proveedor": "SISAP"}, {"cp_id": 74, "cp_proveedor": "Sofnet"}, {"cp_id": 75, "cp_proveedor": "Soft
Office"}, {"cp_id": 77, "cp_proveedor": "Solawinds"}, {"cp_id": 78, "cp_proveedor": "Solutions"}, {"cp_id": 80,
"cp_proveedor": "SSA Sistemas"}, {"cp_id": 81, "cp_proveedor": "SSTI"}, {"cp_id": 82, "cp_proveedor": "Sungard"},
{"cp_id": 83, "cp_proveedor": "SuperIntendencia de Bancos"}, {"cp_id": 86, "cp_proveedor": "Teamviewer"}, {"cp_id": 91,
"cp_proveedor": "ByondiT"}, {"cp_id": 94, "cp_proveedor": "State Street"}, {"cp_id": 97, "cp_proveedor": "Microsoft"},
{"cp_id": 99, "cp_proveedor": "Apache Software Foundation"}, {"cp_id": 100, "cp_proveedor": "HermecSolutions"},
{"cp_id": 101, "cp_proveedor": "filezila"}, {"cp_id": 103, "cp_proveedor": "JO Solutions"}, {"cp_id": 108,
"cp_proveedor": "Pensanómica"}, {"cp_id": 110, "cp_proveedor": "Soluciones Interactivas S.A."}, {"cp_id": 113,
"cp_proveedor": "Asistencia Tecnológica en Sistemas Panamá. S.A."}, {"cp_id": 115, "cp_proveedor": "Soain Panamá,
S.A."}, {"cp_id": 116, "cp_proveedor": "Soluciones Empresariales DSJT"}, {"cp_id": 119, "cp_proveedor":
"(Seleccionar)"}, {"cp_id": 124, "cp_proveedor": "LIFERAY LATIN AMERICA LTDA."}, {"cp_id": 126, "cp_proveedor": "Seaban
Holding, S. A."}, {"cp_id": 128, "cp_proveedor": "SSA Sistemas"}, {"cp_id": 130, "cp_proveedor": "CODEPTY, S.A."},
{"cp_id": 132, "cp_proveedor": "Sistemas de Costa Rica Sisco, S.A."}, {"cp_id": 133, "cp_proveedor": "Nexion
Solutions"}, {"cp_id": 135, "cp_proveedor": "Alborada Solutions Corp"}, {"cp_id": 137, "cp_proveedor": "BPS GROUP LA"},
{"cp_id": 139, "cp_proveedor": "Business & Solutions Consulting, S.A."}, {"cp_id": 141, "cp_proveedor": "Amazon Web
Services"}, {"cp_id": 142, "cp_proveedor": "New access"}, {"cp_id": 144, "cp_proveedor": "Grupo iisa"}, {"cp_id": 146,
"cp_proveedor": "Qlik"}, {"cp_id": 1, "cp_proveedor": "ADR Tecnologies"}, {"cp_id": 5, "cp_proveedor": "ASICOM"},
{"cp_id": 6, "cp_proveedor": "AVANTICA"}, {"cp_id": 7, "cp_proveedor": "AVANTICA Technologies, S.A."}, {"cp_id": 11,
"cp_proveedor": "BOOTH Studio"}, {"cp_id": 13, "cp_proveedor": "Charles Rivers"}, {"cp_id": 14, "cp_proveedor":
"Chocair"}, {"cp_id": 15, "cp_proveedor": "Cibernética"}, {"cp_id": 16, "cp_proveedor": "Cibernética, S.A."}, {"cp_id":
17, "cp_proveedor": "Cobis Corp."}, {"cp_id": 18, "cp_proveedor": "CODEPTY"}, {"cp_id": 23, "cp_proveedor": "Ecrion"},
{"cp_id": 24, "cp_proveedor": "Elastic"}, {"cp_id": 26, "cp_proveedor": "Entrust"}, {"cp_id": 27, "cp_proveedor": "EPM
Works"}, {"cp_id": 29, "cp_proveedor": "Excibit"}, {"cp_id": 30, "cp_proveedor": "Experian"}, {"cp_id": 31,
"cp_proveedor": "FESA"}, {"cp_id": 38, "cp_proveedor": "Grupo Leo"}, {"cp_id": 39, "cp_proveedor": "Grupo Tekins"},
{"cp_id": 40, "cp_proveedor": "GSI"}, {"cp_id": 41, "cp_proveedor": "Hyland Software"}, {"cp_id": 42, "cp_proveedor":
"Inflectra"}, {"cp_id": 44, "cp_proveedor": "INGESIS"}, {"cp_id": 46, "cp_proveedor": "Kbits"}, {"cp_id": 47,
"cp_proveedor": "LAT Capital Software"}, {"cp_id": 51, "cp_proveedor": "MEGA International (Persys)"}, {"cp_id": 53,
"cp_proveedor": "Microsoft Azure"}, {"cp_id": 54, "cp_proveedor": "Microstrategy"}, {"cp_id": 57, "cp_proveedor":
"Moodys"}, {"cp_id": 58, "cp_proveedor": "No disponible"}, {"cp_id": 59, "cp_proveedor": "Oracle Corp"}, {"cp_id": 60,
"cp_proveedor": "Orbe"}, {"cp_id": 61, "cp_proveedor": "Pandata Services / EMC"}, {"cp_id": 63, "cp_proveedor": "Plus
TI"}, {"cp_id": 66, "cp_proveedor": "PROSOFT"}, {"cp_id": 67, "cp_proveedor": "Radiol, S.A"}, {"cp_id": 68,
"cp_proveedor": "Red Hat"}, {"cp_id": 70, "cp_proveedor": "RICOH"}, {"cp_id": 71, "cp_proveedor": "Riscco"}, {"cp_id":
76, "cp_proveedor": "SolarWinds"}, {"cp_id": 79, "cp_proveedor": "Sonitel y Cable & Wireles Business"}, {"cp_id": 84,
"cp_proveedor": "SWIFT"}, {"cp_id": 85, "cp_proveedor": "Syc Consulting"}, {"cp_id": 87, "cp_proveedor": "TECNASA"},
{"cp_id": 88, "cp_proveedor": "TECNASA, Sistemas Expertos"}, {"cp_id": 89, "cp_proveedor": "Telered"}, {"cp_id": 90,
"cp_proveedor": "XperSoft"}, {"cp_id": 92, "cp_proveedor": "GLOADSO"}, {"cp_id": 93, "cp_proveedor": "OYDIA ITSEC S.A"},
{"cp_id": 95, "cp_proveedor": "BD/PEL"}, {"cp_id": 96, "cp_proveedor": "Bit4Id"}, {"cp_id": 98, "cp_proveedor": "Blue
Tide"}, {"cp_id": 102, "cp_proveedor": "Central de Alarmas"}, {"cp_id": 104, "cp_proveedor": "JO Solutions"}, {"cp_id":
105, "cp_proveedor": "Net Consulting"}, {"cp_id": 106, "cp_proveedor": "Revtec"}, {"cp_id": 107, "cp_proveedor":
"Soluciones Segura"}, {"cp_id": 109, "cp_proveedor": "Black Rock - Invesment management company"}, {"cp_id": 111,
"cp_proveedor": "IT ADVISOR"}, {"cp_id": 112, "cp_proveedor": "Smart Bussiness Solutions"}, {"cp_id": 114,
"cp_proveedor": "Business Partner Technologies"}, {"cp_id": 117, "cp_proveedor": "Prosoft Services, S. A."}, {"cp_id":
118, "cp_proveedor": "Infosgroup - GC de Panamá, S.A"}, {"cp_id": 120, "cp_proveedor": "Choucair Cardenas Testing
S.A."}, {"cp_id": 121, "cp_proveedor": "C Y S Consultores Empresariales"}, {"cp_id": 122, "cp_proveedor": "Cobiscorp
Panamá, S.A"}, {"cp_id": 123, "cp_proveedor": "Ernst & Young"}, {"cp_id": 125, "cp_proveedor": "Isthmian Technologies,
INC."}, {"cp_id": 127, "cp_proveedor": "Corporación Consultec TI"}, {"cp_id": 129, "cp_proveedor": "PRANICAL"},
{"cp_id": 131, "cp_proveedor": "CONSULTEC"}, {"cp_id": 134, "cp_proveedor": "EPM Works"}, {"cp_id": 136, "cp_proveedor":
"BUPARTECH, S.A"}, {"cp_id": 138, "cp_proveedor": "Cable & Wireless Panamá"}, {"cp_id": 140, "cp_proveedor": "MST"},
{"cp_id": 143, "cp_proveedor": "SEFISA"}, {"cp_id": 145, "cp_proveedor": "Frontera Security"}, {"cp_id": 147,
"cp_proveedor": "IISA ONLINE"}], [{"cra_id": 1, "cra_mesa": "Plataformas de Infraestructura"}, {"cra_id": 2, "cra_mesa":
"App Ops Plataformas Centrales"}, {"cra_id": 3, "cra_mesa": "App Ops Plataformas de Apoyo"}, {"cra_id": 4, "cra_mesa":
"COSTA RICA"}, {"cra_id": 5, "cra_mesa": "CPCI"}, {"cra_id": 8, "cra_mesa": "SRE Cobis"}, {"cra_id": 9, "cra_mesa": "SRE
Stella"}, {"cra_id": 6, "cra_mesa": "Plataformas de Infraestructura Cloud"}, {"cra_id": 7, "cra_mesa": "SRE Canales"},
{"cra_id": 10, "cra_mesa": "Telematica"}], [{"cts_id": 1, "cts_tipo_servidor": "Propio"}, {"cts_id": 2,
"cts_tipo_servidor": "Alquilado"}], [{"ce_id": 1, "ce_esquema": "Esquema total"}, {"ce_id": 2, "ce_esquema": "Esquema
parcial"}, {"ce_id": 3, "ce_esquema": "Sin esquema"}], [{"cei_id": 1, "cei_estrategias": "Alta disponibilidad"},
{"cei_id": 2, "cei_estrategias": "Activo – Activo"}, {"cei_id": 3, "cei_estrategias": "Activo – Activo Distribuido"},
{"cei_id": 4, "cei_estrategias": "Activo – Activo Balanceado"}, {"cei_id": 5, "cei_estrategias": "Activo – Pasivo"},
{"cei_id": 6, "cei_estrategias": "Activo – Pasivo Compartido"}, {"cei_id": 8, "cei_estrategias": "Recuperación en
sitio"}, {"cei_id": 7, "cei_estrategias": "Pasivo (Stand by)"}], [{"ced_id": 1, "ced_estrategias": "Replicación en
línea"}, {"ced_id": 2, "ced_estrategias": "Replicación diferida"}, {"ced_id": 3, "ced_estrategias": "Replicación
distribuida"}, {"ced_id": 4, "ced_estrategias": "Respaldo/Restauración"}, {"ced_id": 5, "ced_estrategias": "Respaldo a
disco"}, {"ced_id": 6, "ced_estrategias": "Respaldo a caja"}, {"ced_id": 8, "ced_estrategias": "Sin respaldos"},
{"ced_id": 7, "ced_estrategias": "Solo respaldo"}], [{"ctis_id": 1, "ctis_tiempo": "Windows Virtual sin DB 2.5 días"},
{"ctis_id": 2, "ctis_tiempo": "Windows Virtual con DB 3.5 días"}, {"ctis_id": 3, "ctis_tiempo": "Red Hat sin BD 2
días"}, {"ctis_id": 4, "ctis_tiempo": "Red Hat con BD 3 días"}, {"ctis_id": 6, "ctis_tiempo": "Solaris con BD 1
semana"}, {"ctis_id": 8, "ctis_tiempo": "Cent OS 3 días"}, {"ctis_id": 9, "ctis_tiempo": "Oracle Linux con DB 3 días"},
{"ctis_id": 10, "ctis_tiempo": "Oracle Linux Sin DB 2 días"}, {"ctis_id": 5, "ctis_tiempo": "Solaris sin BD 3 días"},
{"ctis_id": 7, "ctis_tiempo": "Servidores Físicos (pasiva) 45-60 días (compra e instalación)"}, {"ctis_id": 11,
"ctis_tiempo": "AIX con DB 3 días"}, {"ctis_id": 12, "ctis_tiempo": "AIX sin DB 2 días"}], [{"ctia_id": 1,
"ctia_tiempo": "0-2hrs"}, {"ctia_id": 2, "ctia_tiempo": "2-4hrs"}, {"ctia_id": 3, "ctia_tiempo": "4-6hrs"}, {"ctia_id":
4, "ctia_tiempo": "6-8hrs"}, {"ctia_id": 5, "ctia_tiempo": "8-10hrs"}, {"ctia_id": 8, "ctia_tiempo": "18-20hrs"},
{"ctia_id": 9, "ctia_tiempo": "20-22hrs"}, {"ctia_id": 10, "ctia_tiempo": "22-24hrs"}, {"ctia_id": 11, "ctia_tiempo":
"Más de 24 horas"}, {"ctia_id": 6, "ctia_tiempo": "12-14hrs"}, {"ctia_id": 7, "ctia_tiempo": "16-18hrs"}], [{"cj_id": 1,
"cj_joya": "SI"}, {"cj_id": 2, "cj_joya": "NO"}]]

#############################################################################################################
[
    [
        {
            "cis_alojamiento": [
                {
                    "ca_id": 1,
                    "ca_tipo_alojamiento": "On premise"
                },
                {
                    "ca_id": 20,
                    "ca_tipo_alojamiento": "dosmas"
                }
            ]
        },
        {
            "cis_desarrollo": [
                {
                    "cd_desarrollo": "Proveedor Comercial",
                    "cd_id": 2
                },
                {
                    "cd_desarrollo": "Tercerizado",
                    "cd_id": 3
                },
                {
                    "cd_desarrollo": "Propioa",
                    "cd_id": 1
                }
            ]
        },
        {
            "cis_entorno_ci": [
                {
                    "cec_id": 1,
                    "cec_tipo": "Produccion"
                },
                {
                    "cec_id": 2,
                    "cec_tipo": "Contingencia"
                },
                {
                    "cec_id": 3,
                    "cec_tipo": "Desarrollo"
                },
                {
                    "cec_id": 4,
                    "cec_tipo": "Pruebas"
                }
            ]
        },
        {
            "cis_lenguaje": [
                {
                    "cl_id": 1,
                    "cl_lenguaje": "ASP & HTML"
                },
                {
                    "cl_id": 2,
                    "cl_lenguaje": "ASP, Vbscrip, Javascript, DLL en lenjuage C"
                },
                {
                    "cl_id": 3,
                    "cl_lenguaje": "ASP.net"
                },
                {
                    "cl_id": 4,
                    "cl_lenguaje": "PL SQL (Oracle)"
                },
                {
                    "cl_id": 7,
                    "cl_lenguaje": "HTML, ASP"
                },
                {
                    "cl_id": 8,
                    "cl_lenguaje": "Java"
                },
                {
                    "cl_id": 14,
                    "cl_lenguaje": "VisualBasic 6.0"
                },
                {
                    "cl_id": 5,
                    "cl_lenguaje": "CLIPPER"
                },
                {
                    "cl_id": 6,
                    "cl_lenguaje": "COTS sin personalización"
                },
                {
                    "cl_id": 9,
                    "cl_lenguaje": "Java, Java Servlets,GlassFish 2.1"
                },
                {
                    "cl_id": 10,
                    "cl_lenguaje": "Java, Visual Basic, .Net, Web Services"
                },
                {
                    "cl_id": 11,
                    "cl_lenguaje": "Lenguaje C"
                },
                {
                    "cl_id": 13,
                    "cl_lenguaje": "Powerbuilder 10"
                },
                {
                    "cl_id": 15,
                    "cl_lenguaje": "XML, webparts, HTML"
                }
            ]
        },
        {
            "cis_nombre_aplicacion": [
                {
                    "cna_aplicacion": "Acceso Remoto al Negocio (Citrix)",
                    "cna_id": 1,
                    "cna_joya": "SI"
                },
                {
                    "cna_aplicacion": "Acceso Seguro a Equipos de Comunicaciones (Tacacs+)",
                    "cna_id": 2,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Acceso Seguro a la Red Corporativa (ISE – Identity Services Engine)",
                    "cna_id": 3,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Administración Centralizada de Impresión (Inepro - DocuPro)",
                    "cna_id": 4,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Administración de Custodio de Valores Internacional (Pershing)",
                    "cna_id": 7,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Administración de Diarios Electrónicos (SADE)",
                    "cna_id": 8,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Administración de Portafolios de Inversión (PAM)",
                    "cna_id": 11,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Administración de Portafolios Internacionales (Next360)",
                    "cna_id": 12,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Administración de Riesgo Empresarial (Mega Hopex)",
                    "cna_id": 13,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Administración de Super Usuarios (Cyber Ark)",
                    "cna_id": 14,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Administración de Tarjetas de Crédito (Masterdata)",
                    "cna_id": 15,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Internet",
                    "cna_id": 184,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Administración de Tarjetas de Vale General (MasterData)",
                    "cna_id": 16,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Administración de Zonas Seguras (Jump Server)",
                    "cna_id": 17,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Administración del Directorio Activo (Active Directory)",
                    "cna_id": 18,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Administración Empresarial (Flexio)",
                    "cna_id": 19,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Almacenamiento Histórico (EMC – ECS Elastic Cloud Storage)",
                    "cna_id": 21,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Análisis de Portafolio de Clientes (Equalizer)",
                    "cna_id": 23,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Arquitectura de Datos (Dataedo)",
                    "cna_id": 31,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "ASF - Bloqueo de Productos (Genexus)",
                    "cna_id": 35,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "ASF - Originación de Transacciones (Genexus)",
                    "cna_id": 36,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "ASF - Reserva de manejo de efectivo (Genexus)",
                    "cna_id": 38,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "ASF -Tesorería Liquidez (Genexus)",
                    "cna_id": 39,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Auditoría Continua (ACL AX Exchange)",
                    "cna_id": 41,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Autenticación de Clientes (Entrust)",
                    "cna_id": 42,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Automatización Robótica de Procesos (Blue Prism)",
                    "cna_id": 47,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Autorizador de Transacciones (BG Autorizador)",
                    "cna_id": 48,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Banca en línea (Liferay)",
                    "cna_id": 50,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Banca en Línea Costa Rica (Liferay)",
                    "cna_id": 51,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Banca en Línea Overseas (Desarrollo Web)",
                    "cna_id": 52,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Banca Móvil Costa Rica (Amazon Web Service)",
                    "cna_id": 54,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Banca Seguros",
                    "cna_id": 55,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Base de Datos - Oracle MIG (Oracle)",
                    "cna_id": 56,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Base de Datos Histórica (MySQL)",
                    "cna_id": 58,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Base de Datos Histórica (MySQL) - Cuentas Ahorros",
                    "cna_id": 61,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Base de Datos Histórica (MySQL) - Cuentas Corrientes",
                    "cna_id": 62,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Bolsas a Consignación (FESA)",
                    "cna_id": 65,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Cámara de Compensación Automática (ACH)",
                    "cna_id": 68,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Capa de Integración de Canales Electrónicos (Datapower)",
                    "cna_id": 69,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Centro de Atención y Servicio (Genesys)",
                    "cna_id": 71,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Compra y Venta de Valores (CRIMS - Charles River)",
                    "cna_id": 73,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Comunicaciones Unificadas (CUCM - Call Manager)1",
                    "cna_id": 75,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Comunicaciones Unificadas CR",
                    "cna_id": 76,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Conecciones a Redes (Cisco AnyConnect)",
                    "cna_id": 78,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Conectores Genéricos Stella (Liferay)",
                    "cna_id": 79,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Contabilidad (Eskema Cloud)",
                    "cna_id": 82,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Contabilidad (Visual Eskema)",
                    "cna_id": 83,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Control de Acceso a Oficinas (AxtraxNg)",
                    "cna_id": 84,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Control de Llaves Físicas (Traka Web)",
                    "cna_id": 85,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Control de Versiones - Código Fuente ",
                    "cna_id": 86,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Control de visitas (Welcome)",
                    "cna_id": 88,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis)",
                    "cna_id": 89,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - Buzón",
                    "cna_id": 94,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - Cámara",
                    "cna_id": 95,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - Cartera",
                    "cna_id": 96,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - Comercio Exterior",
                    "cna_id": 97,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - Corregi",
                    "cna_id": 100,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - Cuentas por Pagar",
                    "cna_id": 101,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - Entes de Control",
                    "cna_id": 102,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - Firmas",
                    "cna_id": 103,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - Garantías",
                    "cna_id": 104,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - Gestión de Crédito",
                    "cna_id": 105,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - Overseas",
                    "cna_id": 107,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - Plazo Fijo",
                    "cna_id": 109,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - Servicios Bancarios",
                    "cna_id": 112,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - Tadmin",
                    "cna_id": 114,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - Trámites de Crédito",
                    "cna_id": 115,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core de IDC en Producción (Fortinet Fortigate)",
                    "cna_id": 118,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Correo Electrónico (Exchange)",
                    "cna_id": 119,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Despliegue de Aplicaciones de Stella (Docker)",
                    "cna_id": 122,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Detección y protección contra vulnerabilidades (Deep Security)",
                    "cna_id": 123,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Diseños Arquitectónicos (Autodesk)",
                    "cna_id": 124,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "E-Commerce (Desarrollo Web)",
                    "cna_id": 126,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Enmascaramiento de Datos (Test Data Management)",
                    "cna_id": 128,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Entidad Registradora Pagadora del SIACAP (P2000)",
                    "cna_id": 129,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Equipos de Seguridad de la Información",
                    "cna_id": 130,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Finanzas Generales",
                    "cna_id": 136,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Firmas Autorizadas de Colaboradores BG (Desarrollo Web)",
                    "cna_id": 138,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "FlexDesk - Virtualización de Estaciones (VMWare Horizon)",
                    "cna_id": 139,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Generación de Pines para Tarjetas (ARH)",
                    "cna_id": 143,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "General",
                    "cna_id": 147,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "General de Seguros (Microsoft Azure)",
                    "cna_id": 148,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Gestión automatizada de Identidades y Accesos de Usuarios (Desarrollo Web)",
                    "cna_id": 150,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Gestión de Casos de Clientes (Engage)",
                    "cna_id": 153,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Gestión de comunicaciones masivas - OMNI (IC Banking Campaigns)",
                    "cna_id": 155,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Gestión de Datos Empresariales (SAP Data Services)",
                    "cna_id": 156,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Gestión de Incidentes de Crédito (Desarrollo Web)",
                    "cna_id": 158,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Gestión de Riesgo de Crédito (CreditLens)",
                    "cna_id": 159,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Gestión de servicios de TI (Jira Service Management)",
                    "cna_id": 161,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Gestión Empresarial de Descuento Directo(GeneXus)",
                    "cna_id": 163,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "GH - Gestión Humana (Talentia)",
                    "cna_id": 165,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Gobierno Digital (Merlink)",
                    "cna_id": 166,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Herramientas DevSecOps",
                    "cna_id": 169,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Históricos BG (Genexus)",
                    "cna_id": 170,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Información de Datos de Mercado (IDC)",
                    "cna_id": 173,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Informe Único de Seguros (INUSE)",
                    "cna_id": 174,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Infraestructura de Comunicaciones y Redes - Centro Operativo",
                    "cna_id": 176,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Interfaz Cobis (Bloomberg)",
                    "cna_id": 182,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Manejador de Tráfico de DNS (Traffic Manager)",
                    "cna_id": 186,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Métricas de licenciamiento (IBM License Metric Tool)",
                    "cna_id": 188,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Modelo de Información Gerencial (MicroStrategy)",
                    "cna_id": 189,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Monitoreo de Base de datos (SQL Server Monitoring Solution)",
                    "cna_id": 191,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Monitoreo de Desempeño de Stella (Dynatrace)",
                    "cna_id": 193,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Monitoreo de enlaces de comunicaciones (Cacti)",
                    "cna_id": 194,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Monitoreo de Sybase ASE (ASEMON)",
                    "cna_id": 198,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Monitoreo Transaccional del Cliente CR (Assist)",
                    "cna_id": 201,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Monitoreo y Auditoria de Base de Datos (Imperva SecureSphere)",
                    "cna_id": 203,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Negociación de Bolsa de Valores El Salvador (SEN)",
                    "cna_id": 206,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Notificaciones de Transacciones con Tarjetas de Crédito (LIMSP)",
                    "cna_id": 207,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Originación de Crédito Hipotecario (ASICOM)",
                    "cna_id": 209,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Pago de Dividendos y Planilla ACP",
                    "cna_id": 210,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Perímetro de Desarrollo y Pruebas",
                    "cna_id": 211,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Planificación y Consolidación presupuestaria (SAP - BPC)",
                    "cna_id": 214,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Plataforma de Gestión y Cobranza (Emerix)",
                    "cna_id": 215,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Plataforma de Mesa de Servicios (BMC - Remedy)",
                    "cna_id": 218,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Plataforma de Servicio y Ventas PMA (Peoplesoft)",
                    "cna_id": 220,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Plataforma de Servicios y Ventas CR (Peoplesoft)",
                    "cna_id": 222,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Procesador de Pagos E-Commerce con Tarjetas de Crédito (BG Unity)",
                    "cna_id": 224,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Profuturo (Microsoft Azure)",
                    "cna_id": 228,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Protección automatizada de datos (Cyber Recovery Solution)",
                    "cna_id": 230,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Punto Yappy (Amazon Web Service)",
                    "cna_id": 233,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Red Inalámbrica Segura (Aruba Network)",
                    "cna_id": 235,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Referencias de Crédito APC",
                    "cna_id": 236,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Replicador de Sybase (SAP)",
                    "cna_id": 239,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Reporteador de INXU Core (SAP Business Objects)",
                    "cna_id": 240,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Reportes de Mercado de Valores (Cognos)",
                    "cna_id": 242,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Respaldo de Estaciones de Usuarios (IDPA - Integrated Data Protection Appliance)",
                    "cna_id": 244,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Respaldo de Estaciones de Usuarios CR (EMC - Avamar Business Edition)",
                    "cna_id": 245,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Seguridad de Acceso a la nube (McAfee - MVISION Cloud CASB)",
                    "cna_id": 249,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Servidor APPX - La Hipotecaria",
                    "cna_id": 250,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Sistema Integrador de Entidades Financieras (BGCR)",
                    "cna_id": 251,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Sistema Integrador de Entidades Financieras (BGCR)",
                    "cna_id": 252,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Sistema Operativo - AIX (IBM )",
                    "cna_id": 253,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Sitio Alterno de Continuidad de Negocios",
                    "cna_id": 256,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Sitio Público Costa Rica (Microsoft Azure)",
                    "cna_id": 257,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Soporte Remoto ( Team Viewer)",
                    "cna_id": 259,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Stella - ACH (Liferay)",
                    "cna_id": 261,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Stella - ATM (Liferay)",
                    "cna_id": 262,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Stella - Cámara (Liferay)",
                    "cna_id": 264,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Stella - Cobranzas (Liferay)",
                    "cna_id": 266,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Stella - Comercio Exterior (Liferay)",
                    "cna_id": 267,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Stella - Cuentas por Pagar (Liferay)",
                    "cna_id": 269,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Stella - Garantías (Liferay)",
                    "cna_id": 270,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Stella - Gestión de Crédito (Liferay)",
                    "cna_id": 271,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Stella - MIS (Liferay)",
                    "cna_id": 272,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Stella - Programa Estrellas (Liferay)",
                    "cna_id": 275,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Stella - Referencias (Liferay)",
                    "cna_id": 276,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Stella - Terminal Administrativa (Liferay)",
                    "cna_id": 278,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Stella - Trámite Empresarial (Liferay)",
                    "cna_id": 279,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Stella (Liferay)",
                    "cna_id": 280,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Transferencias Internacionales (Swift Alliance)",
                    "cna_id": 283,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Ventas Digitales (Amazon Web Service)",
                    "cna_id": 285,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Videoconferencia (Cisco Videoconferencia)",
                    "cna_id": 288,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Virtualización de Servidores Microsoft (Hyper V)",
                    "cna_id": 291,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Gestor de contenido en Pantallas (MagicInfo)",
                    "cna_id": 299,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Gestión de seguridad de Infraestructuras en la nube (Tenable Cloud Security)",
                    "cna_id": 301,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Administración de Átomos para SIB (ADMINSIB)",
                    "cna_id": 5,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Administración de Auditorías (TeamMate)",
                    "cna_id": 6,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Administración de Estaciones (Client Management)",
                    "cna_id": 9,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Administración de Fondos de Pensión y Cesantías (P2000)",
                    "cna_id": 10,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Administración Financiera (CODISA NAF) ",
                    "cna_id": 20,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Análisis Centralizado de Bitácoras (Elastic Stack)",
                    "cna_id": 22,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Análisis e Inteligencia de Datos (Tableau)",
                    "cna_id": 24,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Análisis Financieros (Bancware - ALM)",
                    "cna_id": 25,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Análisis Financieros (Bancware - Data Integration)",
                    "cna_id": 26,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Análisis y Riesgo de Inversiones (Aladdin)",
                    "cna_id": 27,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Antivirus (McAfee)",
                    "cna_id": 28,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Antivirus (Trellix MVISION ePO)",
                    "cna_id": 29,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Antivirus en Dispositivos Móviles (McAfee Mvision Mobile)",
                    "cna_id": 30,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Arquitectura Empresarial (Hopex)",
                    "cna_id": 32,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "ASF - Administración de Saldos de Cajeros Automáticos (Genexus)",
                    "cna_id": 33,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "ASF - Aplicaciones de Soporte y Finanzas (Genexus)",
                    "cna_id": 34,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "ASF - Pagos MEF (Genexus)",
                    "cna_id": 37,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "ATM (Servicios)",
                    "cna_id": 40,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Autenticación de Clientes (Transmit Security)",
                    "cna_id": 43,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Autenticación de Usuarios (RSA Authentication Manager)",
                    "cna_id": 44,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Automatización de procesos nocturnos (BMC Control M)",
                    "cna_id": 45,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Automatización Robótica de Mensajería (Chatbot)",
                    "cna_id": 46,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Banca Abierta (IBM Integration BUS)",
                    "cna_id": 49,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Banca Móvil (Amazon Web Service)",
                    "cna_id": 53,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Base de Datos - SAP IQ DWH MIG (SAP)",
                    "cna_id": 57,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Base de Datos Histórica (MySQL) - Canales",
                    "cna_id": 59,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Base de Datos Histórica (MySQL) - Cartera",
                    "cna_id": 60,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Base de Datos MySQL(Stella)",
                    "cna_id": 63,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "BG LAB - Análisis Predictivo de Datos (Python)",
                    "cna_id": 64,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Branch Departamentales",
                    "cna_id": 66,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Branch Sucursales",
                    "cna_id": 67,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Carpeta Única del Cliente (Onbase)",
                    "cna_id": 70,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Chat del Sitio Público (LivePerson)",
                    "cna_id": 72,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Comunicaciones Unificadas (CUCM - Call Manager)",
                    "cna_id": 74,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Conciliación Bancaria (Syc Conciliaciones)",
                    "cna_id": 77,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Conexión BG (Json)",
                    "cna_id": 80,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Consolidaciones Financieras (Holding)",
                    "cna_id": 81,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Control de Versiones (Desarrollo Web)",
                    "cna_id": 87,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - Admin",
                    "cna_id": 90,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - Administrador de Crédito",
                    "cna_id": 91,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - BGCR",
                    "cna_id": 92,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - Branch Administrador",
                    "cna_id": 93,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - Contabilidad",
                    "cna_id": 98,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - Core Server",
                    "cna_id": 99,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - Kernel",
                    "cna_id": 106,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - Personalización",
                    "cna_id": 108,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - Referencia de Crédito",
                    "cna_id": 110,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - Seguridad",
                    "cna_id": 111,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - SP",
                    "cna_id": 113,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - TS",
                    "cna_id": 116,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Core Bancario (Cobis) - Visa Estrella",
                    "cna_id": 117,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Creación Digital de Clientes (Amazon Web Service)",
                    "cna_id": 120,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Custodia y Administración de Valores de LatinClear (Sicus)",
                    "cna_id": 121,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Distribución de Tarjetas de Crédito (Onbase)",
                    "cna_id": 125,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Empresa General de Inversiones (Microsoft Azure)",
                    "cna_id": 127,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Escaneo de Vulnerabilidades (Nessus Vulnerability Scanner )",
                    "cna_id": 131,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Facturación electrónica DGI (WebPos)",
                    "cna_id": 132,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "File Server (Microsoft)",
                    "cna_id": 133,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Filtro de Correo Electrónico (MailMarshal)",
                    "cna_id": 134,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Filtro de Navegación de Internet (Forcepoint)",
                    "cna_id": 135,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Firma electrónica automatizada (Signbox)",
                    "cna_id": 137,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Flujos de Consumo AID (Onbase)",
                    "cna_id": 140,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Flujos e Imágenes (Onbase)",
                    "cna_id": 141,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Fundación Sus Buenos Vecinos (Microsoft Azure)",
                    "cna_id": 142,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Generación de Reportes FATCA y CRS (Avantica)",
                    "cna_id": 144,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Generación y envío de Informes SUGEF (Gnosis)",
                    "cna_id": 145,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Generador de Documentos (Ecrion)",
                    "cna_id": 146,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Gestión Administrativa (Spyral)",
                    "cna_id": 149,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Gestión Automatizada de Parches (Patch Manager Plus)",
                    "cna_id": 151,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Gestión de Aprendizaje (NetDimension - Learning)",
                    "cna_id": 152,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Gestión de Cobros (Recovery)",
                    "cna_id": 154,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Gestión de DNS Externo (BIND DNS Server)",
                    "cna_id": 157,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Gestión de Seguros (INXU Core)",
                    "cna_id": 160,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Gestión Documental de Clientes (Onbase)",
                    "cna_id": 162,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Gestor de Contenido en Pantallas (Navori QL)",
                    "cna_id": 164,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Grabación de llamadas Telefónicas (Nice Call)",
                    "cna_id": 167,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Grabación de Llamadas Telefónicas (Redbox)",
                    "cna_id": 168,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Históricos de Correos Sensitivos (Barracuda)",
                    "cna_id": 171,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "IBM Datapower Gateway Stella (Liferay)",
                    "cna_id": 172,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Infraestructura de Almacenamiento (V7000)",
                    "cna_id": 175,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Infraestructura de Identity Services Engine ( ISE) - Centro Operativo",
                    "cna_id": 177,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Infraestructura en la Nube (Microsoft Azure)",
                    "cna_id": 178,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Integración de Cámara de Compensación Automática ACH (Montran Gateway)",
                    "cna_id": 179,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Intercambio Digital Seguro (EFT Server)",
                    "cna_id": 180,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Intercambio y Transferencia Masiva (Sterling File Gateway)",
                    "cna_id": 181,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Interfaz de Portafolios de Inversión Administrados (Black Rock)",
                    "cna_id": 183,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Kernel Core Bancario (Cobis)",
                    "cna_id": 185,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "MAPTOOL (Microsoft Assessment and Planning Toolkit)",
                    "cna_id": 187,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Modelo de Información Gerencial Profuturo (QlikView)",
                    "cna_id": 190,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Monitoreo de Desempeño de Banca en Línea (Dynatrace)",
                    "cna_id": 192,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Monitoreo de Información y Administración de Eventos (SIEM)",
                    "cna_id": 195,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Monitoreo de Infraestructuras de TI (Zabbix)",
                    "cna_id": 196,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Monitoreo de Redes (Orion)",
                    "cna_id": 197,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Monitoreo de Transferencias del Cliente (Safewatch)",
                    "cna_id": 199,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Monitoreo para Reducción de Eventos (Ares)",
                    "cna_id": 200,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Monitoreo Transaccional del Cliente PMA (Assist)",
                    "cna_id": 202,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Motor de Reglas (IBM ODM)",
                    "cna_id": 204,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Navisworks Freedom (Autodesk)",
                    "cna_id": 205,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Ofimática en la Nube (Microsoft 365)",
                    "cna_id": 208,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Perímetro de Producción (Fortinet Management and Analytics)",
                    "cna_id": 212,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Planes de Contingencia",
                    "cna_id": 213,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Plataforma de Integración (ACE - App Connect Enterprise)",
                    "cna_id": 216,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Plataforma de Integración (Cobis TS)",
                    "cna_id": 217,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Plataforma de Prevención de fraude (Monitor Plus)",
                    "cna_id": 219,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Plataforma de Servicios Electrónicos (PEL)",
                    "cna_id": 221,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Prevención y Detección de Intrusos (Instrusion Prevention System)",
                    "cna_id": 223,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Procesador de Servicios (Cobis SP)",
                    "cna_id": 225,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Procesador de Transacciones de Tarjetas (ATH)",
                    "cna_id": 226,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Procesamiento y Devolución de Cheques (Aperta)",
                    "cna_id": 227,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Programación de Procesos Batch (Groovy)",
                    "cna_id": 229,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Protección contra ataques de negación de servicios (DDoS)",
                    "cna_id": 231,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Pruebas Automatizadas (Rational)",
                    "cna_id": 232,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Red de Almacenamiento Directores MDS (Cisco)",
                    "cna_id": 234,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Relojes de Marcación (Kronos)",
                    "cna_id": 237,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Replicador de Base de Datos (SQL - Oracle)",
                    "cna_id": 238,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Reporteador de Visual Eskema (QlikView)",
                    "cna_id": 241,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Respaldo de Estaciones de Usuarios (EMC - Avamar Business Edition)",
                    "cna_id": 243,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Respaldo de Servidores (EMC - Avamar Rain)",
                    "cna_id": 246,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Revista En Exclusiva (Microsoft Azure)",
                    "cna_id": 247,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Salones de Reuniones Virtuales (Cisco WebEx)",
                    "cna_id": 248,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Sistema Operativo - Red Hat (Red Hat)",
                    "cna_id": 254,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Sistema Operativo - Solaris (Oracle)",
                    "cna_id": 255,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Sitio Público Panamá (Microsoft Azure)",
                    "cna_id": 258,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Spyral - Gestión Administrativa",
                    "cna_id": 260,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Stella - Banca Virtual (Liferay)",
                    "cna_id": 263,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Stella - Cartera (Liferay)",
                    "cna_id": 265,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Stella - Control de incidentes (Liferay)",
                    "cna_id": 268,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Stella - Operaciones de Inversiones Banca Patrimonial (Liferay)",
                    "cna_id": 273,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Stella - Plazo Fijo (Liferay)",
                    "cna_id": 274,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Stella - Servicios Bancarios (Liferay)",
                    "cna_id": 277,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Suite BG",
                    "cna_id": 281,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Transacciones Electrónicas de Bolsa de Valores Pmá (Nasdaq)",
                    "cna_id": 282,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Vale General (Microsoft Azure)",
                    "cna_id": 284,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Verificación de precios de acciones (Bloomberg Gateway)",
                    "cna_id": 286,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Veritas Netbackup",
                    "cna_id": 287,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Virtualización de Servidores (Red Hat)",
                    "cna_id": 289,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Virtualización de Servidores (VMWare)",
                    "cna_id": 290,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Windows Deployment Services",
                    "cna_id": 292,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Yappy (Amazon Web Service)",
                    "cna_id": 293,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Yappy + (Amazon Web Service)",
                    "cna_id": 294,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Yappy web (Microsoft Azure)",
                    "cna_id": 295,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Stella - Administrador Comercio Exterior (Liferay)",
                    "cna_id": 296,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Red de distribución de contenidos en la nube (Azure Front Door)",
                    "cna_id": 297,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Gestión de pagos a proveedores (Confirming)",
                    "cna_id": 298,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Infraestructura",
                    "cna_id": 300,
                    "cna_joya": "NO"
                },
                {
                    "cna_aplicacion": "Gestión de token para tarjetas (HST Pay Admin - APIs)",
                    "cna_id": 302,
                    "cna_joya": "NO"
                }
            ]
        },
        {
            "cis_pais_servidor": [
                {
                    "cps_id": 1,
                    "cps_servidor": "Panamá"
                },
                {
                    "cps_id": 2,
                    "cps_servidor": "Costa Rica"
                },
                {
                    "cps_id": 3,
                    "cps_servidor": "BG Valores"
                },
                {
                    "cps_id": 4,
                    "cps_servidor": "General de Seguros"
                },
                {
                    "cps_id": 5,
                    "cps_servidor": "Profuturo"
                },
                {
                    "cps_id": 6,
                    "cps_servidor": "Regionales"
                },
                {
                    "cps_id": 7,
                    "cps_servidor": "Vale General"
                },
                {
                    "cps_id": 8,
                    "cps_servidor": "Fundacion sus Buenos Vecinos"
                },
                {
                    "cps_id": 9,
                    "cps_servidor": "Yappy"
                }
            ]
        },
        {
            "cis_proveedor": [
                {
                    "cp_id": 2,
                    "cp_proveedor": "Airwatch"
                },
                {
                    "cp_id": 3,
                    "cp_proveedor": "Aperta"
                },
                {
                    "cp_id": 4,
                    "cp_proveedor": "Arango Software"
                },
                {
                    "cp_id": 8,
                    "cp_proveedor": "Banco General"
                },
                {
                    "cp_id": 9,
                    "cp_proveedor": "Bloomberg"
                },
                {
                    "cp_id": 10,
                    "cp_proveedor": "Blue Prism"
                },
                {
                    "cp_id": 12,
                    "cp_proveedor": "Cable & Wireles Business"
                },
                {
                    "cp_id": 19,
                    "cp_proveedor": "Compulab"
                },
                {
                    "cp_id": 20,
                    "cp_proveedor": "DeSimplex"
                },
                {
                    "cp_id": 21,
                    "cp_proveedor": "Dvelop"
                },
                {
                    "cp_id": 22,
                    "cp_proveedor": "Dynatrace"
                },
                {
                    "cp_id": 25,
                    "cp_proveedor": "EMC"
                },
                {
                    "cp_id": 28,
                    "cp_proveedor": "Equalizer"
                },
                {
                    "cp_id": 32,
                    "cp_proveedor": "First Data"
                },
                {
                    "cp_id": 33,
                    "cp_proveedor": "GATI"
                },
                {
                    "cp_id": 34,
                    "cp_proveedor": "GBM"
                },
                {
                    "cp_id": 35,
                    "cp_proveedor": "Genesys"
                },
                {
                    "cp_id": 36,
                    "cp_proveedor": "Global Advisory Solutions"
                },
                {
                    "cp_id": 37,
                    "cp_proveedor": "Grupo Babel"
                },
                {
                    "cp_id": 43,
                    "cp_proveedor": "Infocorpgroup"
                },
                {
                    "cp_id": 45,
                    "cp_proveedor": "Intelector / Global Scape"
                },
                {
                    "cp_id": 48,
                    "cp_proveedor": "Latinia"
                },
                {
                    "cp_id": 49,
                    "cp_proveedor": "Liferay"
                },
                {
                    "cp_id": 50,
                    "cp_proveedor": "Magicinfo"
                },
                {
                    "cp_id": 52,
                    "cp_proveedor": "microstrategy"
                },
                {
                    "cp_id": 55,
                    "cp_proveedor": "Monitise"
                },
                {
                    "cp_id": 56,
                    "cp_proveedor": "Montran"
                },
                {
                    "cp_id": 62,
                    "cp_proveedor": "PEL"
                },
                {
                    "cp_id": 64,
                    "cp_proveedor": "Princeton Financials"
                },
                {
                    "cp_id": 65,
                    "cp_proveedor": "Prodic"
                },
                {
                    "cp_id": 69,
                    "cp_proveedor": "Redbox"
                },
                {
                    "cp_id": 72,
                    "cp_proveedor": "SIDE - BCG"
                },
                {
                    "cp_id": 73,
                    "cp_proveedor": "SISAP"
                },
                {
                    "cp_id": 74,
                    "cp_proveedor": "Sofnet"
                },
                {
                    "cp_id": 75,
                    "cp_proveedor": "Soft Office"
                },
                {
                    "cp_id": 77,
                    "cp_proveedor": "Solawinds"
                },
                {
                    "cp_id": 78,
                    "cp_proveedor": "Solutions"
                },
                {
                    "cp_id": 80,
                    "cp_proveedor": "SSA Sistemas"
                },
                {
                    "cp_id": 81,
                    "cp_proveedor": "SSTI"
                },
                {
                    "cp_id": 82,
                    "cp_proveedor": "Sungard"
                },
                {
                    "cp_id": 83,
                    "cp_proveedor": "SuperIntendencia de Bancos"
                },
                {
                    "cp_id": 86,
                    "cp_proveedor": "Teamviewer"
                },
                {
                    "cp_id": 91,
                    "cp_proveedor": "ByondiT"
                },
                {
                    "cp_id": 94,
                    "cp_proveedor": "State Street"
                },
                {
                    "cp_id": 97,
                    "cp_proveedor": "Microsoft"
                },
                {
                    "cp_id": 99,
                    "cp_proveedor": "Apache Software Foundation"
                },
                {
                    "cp_id": 100,
                    "cp_proveedor": "HermecSolutions"
                },
                {
                    "cp_id": 101,
                    "cp_proveedor": "filezila"
                },
                {
                    "cp_id": 103,
                    "cp_proveedor": "JO Solutions"
                },
                {
                    "cp_id": 108,
                    "cp_proveedor": "Pensanómica"
                },
                {
                    "cp_id": 110,
                    "cp_proveedor": "Soluciones Interactivas S.A."
                },
                {
                    "cp_id": 113,
                    "cp_proveedor": "Asistencia Tecnológica en Sistemas Panamá. S.A."
                },
                {
                    "cp_id": 115,
                    "cp_proveedor": "Soain Panamá, S.A."
                },
                {
                    "cp_id": 116,
                    "cp_proveedor": "Soluciones Empresariales DSJT"
                },
                {
                    "cp_id": 119,
                    "cp_proveedor": "(Seleccionar)"
                },
                {
                    "cp_id": 124,
                    "cp_proveedor": "LIFERAY LATIN AMERICA LTDA."
                },
                {
                    "cp_id": 126,
                    "cp_proveedor": "Seaban Holding, S. A."
                },
                {
                    "cp_id": 128,
                    "cp_proveedor": "SSA Sistemas"
                },
                {
                    "cp_id": 130,
                    "cp_proveedor": "CODEPTY, S.A."
                },
                {
                    "cp_id": 132,
                    "cp_proveedor": "Sistemas de Costa Rica Sisco, S.A."
                },
                {
                    "cp_id": 133,
                    "cp_proveedor": "Nexion Solutions"
                },
                {
                    "cp_id": 135,
                    "cp_proveedor": "Alborada Solutions Corp"
                },
                {
                    "cp_id": 137,
                    "cp_proveedor": "BPS GROUP LA"
                },
                {
                    "cp_id": 139,
                    "cp_proveedor": "Business & Solutions Consulting, S.A."
                },
                {
                    "cp_id": 141,
                    "cp_proveedor": "Amazon Web Services"
                },
                {
                    "cp_id": 142,
                    "cp_proveedor": "New access"
                },
                {
                    "cp_id": 144,
                    "cp_proveedor": "Grupo iisa"
                },
                {
                    "cp_id": 146,
                    "cp_proveedor": "Qlik"
                },
                {
                    "cp_id": 1,
                    "cp_proveedor": "ADR Tecnologies"
                },
                {
                    "cp_id": 5,
                    "cp_proveedor": "ASICOM"
                },
                {
                    "cp_id": 6,
                    "cp_proveedor": "AVANTICA"
                },
                {
                    "cp_id": 7,
                    "cp_proveedor": "AVANTICA Technologies, S.A."
                },
                {
                    "cp_id": 11,
                    "cp_proveedor": "BOOTH Studio"
                },
                {
                    "cp_id": 13,
                    "cp_proveedor": "Charles Rivers"
                },
                {
                    "cp_id": 14,
                    "cp_proveedor": "Chocair"
                },
                {
                    "cp_id": 15,
                    "cp_proveedor": "Cibernética"
                },
                {
                    "cp_id": 16,
                    "cp_proveedor": "Cibernética, S.A."
                },
                {
                    "cp_id": 17,
                    "cp_proveedor": "Cobis Corp."
                },
                {
                    "cp_id": 18,
                    "cp_proveedor": "CODEPTY"
                },
                {
                    "cp_id": 23,
                    "cp_proveedor": "Ecrion"
                },
                {
                    "cp_id": 24,
                    "cp_proveedor": "Elastic"
                },
                {
                    "cp_id": 26,
                    "cp_proveedor": "Entrust"
                },
                {
                    "cp_id": 27,
                    "cp_proveedor": "EPM Works"
                },
                {
                    "cp_id": 29,
                    "cp_proveedor": "Excibit"
                },
                {
                    "cp_id": 30,
                    "cp_proveedor": "Experian"
                },
                {
                    "cp_id": 31,
                    "cp_proveedor": "FESA"
                },
                {
                    "cp_id": 38,
                    "cp_proveedor": "Grupo Leo"
                },
                {
                    "cp_id": 39,
                    "cp_proveedor": "Grupo Tekins"
                },
                {
                    "cp_id": 40,
                    "cp_proveedor": "GSI"
                },
                {
                    "cp_id": 41,
                    "cp_proveedor": "Hyland Software"
                },
                {
                    "cp_id": 42,
                    "cp_proveedor": "Inflectra"
                },
                {
                    "cp_id": 44,
                    "cp_proveedor": "INGESIS"
                },
                {
                    "cp_id": 46,
                    "cp_proveedor": "Kbits"
                },
                {
                    "cp_id": 47,
                    "cp_proveedor": "LAT Capital Software"
                },
                {
                    "cp_id": 51,
                    "cp_proveedor": "MEGA International (Persys)"
                },
                {
                    "cp_id": 53,
                    "cp_proveedor": "Microsoft Azure"
                },
                {
                    "cp_id": 54,
                    "cp_proveedor": "Microstrategy"
                },
                {
                    "cp_id": 57,
                    "cp_proveedor": "Moodys"
                },
                {
                    "cp_id": 58,
                    "cp_proveedor": "No disponible"
                },
                {
                    "cp_id": 59,
                    "cp_proveedor": "Oracle Corp"
                },
                {
                    "cp_id": 60,
                    "cp_proveedor": "Orbe"
                },
                {
                    "cp_id": 61,
                    "cp_proveedor": "Pandata Services / EMC"
                },
                {
                    "cp_id": 63,
                    "cp_proveedor": "Plus TI"
                },
                {
                    "cp_id": 66,
                    "cp_proveedor": "PROSOFT"
                },
                {
                    "cp_id": 67,
                    "cp_proveedor": "Radiol, S.A"
                },
                {
                    "cp_id": 68,
                    "cp_proveedor": "Red Hat"
                },
                {
                    "cp_id": 70,
                    "cp_proveedor": "RICOH"
                },
                {
                    "cp_id": 71,
                    "cp_proveedor": "Riscco"
                },
                {
                    "cp_id": 76,
                    "cp_proveedor": "SolarWinds"
                },
                {
                    "cp_id": 79,
                    "cp_proveedor": "Sonitel y Cable & Wireles Business"
                },
                {
                    "cp_id": 84,
                    "cp_proveedor": "SWIFT"
                },
                {
                    "cp_id": 85,
                    "cp_proveedor": "Syc Consulting"
                },
                {
                    "cp_id": 87,
                    "cp_proveedor": "TECNASA"
                },
                {
                    "cp_id": 88,
                    "cp_proveedor": "TECNASA, Sistemas Expertos"
                },
                {
                    "cp_id": 89,
                    "cp_proveedor": "Telered"
                },
                {
                    "cp_id": 90,
                    "cp_proveedor": "XperSoft"
                },
                {
                    "cp_id": 92,
                    "cp_proveedor": "GLOADSO"
                },
                {
                    "cp_id": 93,
                    "cp_proveedor": "OYDIA ITSEC S.A"
                },
                {
                    "cp_id": 95,
                    "cp_proveedor": "BD/PEL"
                },
                {
                    "cp_id": 96,
                    "cp_proveedor": "Bit4Id"
                },
                {
                    "cp_id": 98,
                    "cp_proveedor": "Blue Tide"
                },
                {
                    "cp_id": 102,
                    "cp_proveedor": "Central de Alarmas"
                },
                {
                    "cp_id": 104,
                    "cp_proveedor": "JO Solutions"
                },
                {
                    "cp_id": 105,
                    "cp_proveedor": "Net Consulting"
                },
                {
                    "cp_id": 106,
                    "cp_proveedor": "Revtec"
                },
                {
                    "cp_id": 107,
                    "cp_proveedor": "Soluciones Segura"
                },
                {
                    "cp_id": 109,
                    "cp_proveedor": "Black Rock - Invesment management company"
                },
                {
                    "cp_id": 111,
                    "cp_proveedor": "IT ADVISOR"
                },
                {
                    "cp_id": 112,
                    "cp_proveedor": "Smart Bussiness Solutions"
                },
                {
                    "cp_id": 114,
                    "cp_proveedor": "Business Partner Technologies"
                },
                {
                    "cp_id": 117,
                    "cp_proveedor": "Prosoft Services, S. A."
                },
                {
                    "cp_id": 118,
                    "cp_proveedor": "Infosgroup - GC de Panamá, S.A"
                },
                {
                    "cp_id": 120,
                    "cp_proveedor": "Choucair Cardenas Testing S.A."
                },
                {
                    "cp_id": 121,
                    "cp_proveedor": "C Y S Consultores Empresariales"
                },
                {
                    "cp_id": 122,
                    "cp_proveedor": "Cobiscorp Panamá, S.A"
                },
                {
                    "cp_id": 123,
                    "cp_proveedor": "Ernst & Young"
                },
                {
                    "cp_id": 125,
                    "cp_proveedor": "Isthmian Technologies, INC."
                },
                {
                    "cp_id": 127,
                    "cp_proveedor": "Corporación Consultec TI"
                },
                {
                    "cp_id": 129,
                    "cp_proveedor": "PRANICAL"
                },
                {
                    "cp_id": 131,
                    "cp_proveedor": "CONSULTEC"
                },
                {
                    "cp_id": 134,
                    "cp_proveedor": "EPM Works"
                },
                {
                    "cp_id": 136,
                    "cp_proveedor": "BUPARTECH, S.A"
                },
                {
                    "cp_id": 138,
                    "cp_proveedor": "Cable & Wireless Panamá"
                },
                {
                    "cp_id": 140,
                    "cp_proveedor": "MST"
                },
                {
                    "cp_id": 143,
                    "cp_proveedor": "SEFISA"
                },
                {
                    "cp_id": 145,
                    "cp_proveedor": "Frontera Security"
                },
                {
                    "cp_id": 147,
                    "cp_proveedor": "IISA ONLINE"
                }
            ]
        },
        {
            "cis_responsable_aplicacion": [
                {
                    "cra_id": 1,
                    "cra_mesa": "Plataformas de  Infraestructura"
                },
                {
                    "cra_id": 2,
                    "cra_mesa": "App Ops Plataformas Centrales"
                },
                {
                    "cra_id": 3,
                    "cra_mesa": "App Ops Plataformas de Apoyo"
                },
                {
                    "cra_id": 4,
                    "cra_mesa": "COSTA RICA"
                },
                {
                    "cra_id": 5,
                    "cra_mesa": "CPCI"
                },
                {
                    "cra_id": 8,
                    "cra_mesa": "SRE Cobis"
                },
                {
                    "cra_id": 9,
                    "cra_mesa": "SRE Stella"
                },
                {
                    "cra_id": 6,
                    "cra_mesa": "Plataformas de Infraestructura Cloud"
                },
                {
                    "cra_id": 7,
                    "cra_mesa": "SRE Canales"
                },
                {
                    "cra_id": 10,
                    "cra_mesa": "Telematica"
                }
            ]
        },
        {
            "cis_tipo_servidor": [
                {
                    "cts_id": 1,
                    "cts_tipo_servidor": "Propio"
                },
                {
                    "cts_id": 2,
                    "cts_tipo_servidor": "Alquilado"
                }
            ]
        },
        {
            "cis_esquema": [
                {
                    "ce_esquema": "Esquema total",
                    "ce_id": 1
                },
                {
                    "ce_esquema": "Esquema parcial",
                    "ce_id": 2
                },
                {
                    "ce_esquema": "Sin esquema",
                    "ce_id": 3
                }
            ]
        },
        {
            "cis_estrategias_infra": [
                {
                    "cei_estrategias": "Alta disponibilidad",
                    "cei_id": 1
                },
                {
                    "cei_estrategias": "Activo – Activo",
                    "cei_id": 2
                },
                {
                    "cei_estrategias": "Activo – Activo Distribuido",
                    "cei_id": 3
                },
                {
                    "cei_estrategias": "Activo – Activo Balanceado",
                    "cei_id": 4
                },
                {
                    "cei_estrategias": "Activo – Pasivo",
                    "cei_id": 5
                },
                {
                    "cei_estrategias": "Activo – Pasivo Compartido",
                    "cei_id": 6
                },
                {
                    "cei_estrategias": "Recuperación en sitio",
                    "cei_id": 8
                },
                {
                    "cei_estrategias": "Pasivo (Stand by)",
                    "cei_id": 7
                }
            ]
        },
        {
            "cis_estrategias_datos": [
                {
                    "ced_estrategias": "Replicación en línea",
                    "ced_id": 1
                },
                {
                    "ced_estrategias": "Replicación diferida",
                    "ced_id": 2
                },
                {
                    "ced_estrategias": "Replicación distribuida",
                    "ced_id": 3
                },
                {
                    "ced_estrategias": "Respaldo/Restauración",
                    "ced_id": 4
                },
                {
                    "ced_estrategias": "Respaldo a disco",
                    "ced_id": 5
                },
                {
                    "ced_estrategias": "Respaldo a caja",
                    "ced_id": 6
                },
                {
                    "ced_estrategias": "Sin respaldos",
                    "ced_id": 8
                },
                {
                    "ced_estrategias": "Solo respaldo",
                    "ced_id": 7
                }
            ]
        },
        {
            "cis_tiempo_infra_servidor": [
                {
                    "ctis_id": 1,
                    "ctis_tiempo": "Windows Virtual sin DB 2.5 días"
                },
                {
                    "ctis_id": 2,
                    "ctis_tiempo": "Windows Virtual con DB 3.5 días"
                },
                {
                    "ctis_id": 3,
                    "ctis_tiempo": "Red Hat sin BD 2 días"
                },
                {
                    "ctis_id": 4,
                    "ctis_tiempo": "Red Hat con BD 3 días"
                },
                {
                    "ctis_id": 6,
                    "ctis_tiempo": "Solaris con BD 1 semana"
                },
                {
                    "ctis_id": 8,
                    "ctis_tiempo": "Cent OS 3 días"
                },
                {
                    "ctis_id": 9,
                    "ctis_tiempo": "Oracle Linux con DB 3 días"
                },
                {
                    "ctis_id": 10,
                    "ctis_tiempo": "Oracle Linux Sin DB 2 días"
                },
                {
                    "ctis_id": 5,
                    "ctis_tiempo": "Solaris sin BD 3 días"
                },
                {
                    "ctis_id": 7,
                    "ctis_tiempo": "Servidores Físicos (pasiva) 45-60 días (compra e instalación)"
                },
                {
                    "ctis_id": 11,
                    "ctis_tiempo": "AIX con DB 3 días"
                },
                {
                    "ctis_id": 12,
                    "ctis_tiempo": "AIX sin DB 2 días"
                }
            ]
        },
        {
            "cis_tiempo_infra_aplicacion": [
                {
                    "ctia_id": 1,
                    "ctia_tiempo": "0-2hrs"
                },
                {
                    "ctia_id": 2,
                    "ctia_tiempo": "2-4hrs"
                },
                {
                    "ctia_id": 3,
                    "ctia_tiempo": "4-6hrs"
                },
                {
                    "ctia_id": 4,
                    "ctia_tiempo": "6-8hrs"
                },
                {
                    "ctia_id": 5,
                    "ctia_tiempo": "8-10hrs"
                },
                {
                    "ctia_id": 8,
                    "ctia_tiempo": "18-20hrs"
                },
                {
                    "ctia_id": 9,
                    "ctia_tiempo": "20-22hrs"
                },
                {
                    "ctia_id": 10,
                    "ctia_tiempo": "22-24hrs"
                },
                {
                    "ctia_id": 11,
                    "ctia_tiempo": "Más de 24 horas"
                },
                {
                    "ctia_id": 6,
                    "ctia_tiempo": "12-14hrs"
                },
                {
                    "ctia_id": 7,
                    "ctia_tiempo": "16-18hrs"
                }
            ]
        },
        {
            "cis_joya": [
                {
                    "cj_id": 1,
                    "cj_joya": "SI"
                },
                {
                    "cj_id": 2,
                    "cj_joya": "NO"
                }
            ]
        }
    ]
]

###########################################################################################################
