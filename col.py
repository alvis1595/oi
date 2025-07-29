#!/usr/bin/python
# -*- coding: utf-8 -*-

# Documentación para Ansible Galaxy y help() en Ansible
DOCUMENTATION = r'''
---
module: crear_archivo
short_description: Crea o actualiza un archivo en el host
description:
  - Este módulo permite crear o actualizar un archivo en el host remoto.
  - Si el archivo ya existe, reemplaza su contenido solo si es diferente.
options:
  path:
    description:
      - Ruta absoluta del archivo a crear.
    required: true
    type: str
  content:
    description:
      - Contenido que se escribirá en el archivo.
    required: true
    type: str
  mode:
    description:
      - Permisos del archivo (formato octal, ejemplo 0644).
    required: false
    type: str
    default: '0644'
  owner:
    description:
      - Dueño del archivo.
    required: false
    type: str
    default: null
  group:
    description:
      - Grupo propietario del archivo.
    required: false
    type: str
    default: null
author:
  - Alvis Sánchez
'''

EXAMPLES = r'''
- name: Crear archivo con mi módulo
  alvis.archivos.crear_archivo:
    path: /tmp/ejemplo.txt
    content: "Este archivo fue creado con programación"
    mode: '0644'
    owner: root
    group: root
'''

RETURN = r'''
changed:
  description: Indica si el archivo fue creado o modificado.
  type: bool
  returned: always
msg:
  description: Mensaje del resultado de la operación.
  type: str
  returned: always
'''

import os
import stat
import pwd
import grp
from ansible.module_utils.basic import AnsibleModule

def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(type='str', required=True),
            content=dict(type='str', required=True),
            mode=dict(type='str', default='0644'),
            owner=dict(type='str', required=False, default=None),
            group=dict(type='str', required=False, default=None),
        ),
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']
    mode = module.params['mode']
    owner = module.params['owner']
    group = module.params['group']

    changed = False

    try:
        # Verificar si el archivo ya existe y comparar contenido
        if os.path.exists(path):
            with open(path, 'r') as f:
                existing_content = f.read()
            if existing_content != content:
                changed = True
        else:
            changed = True

        if module.check_mode:
            module.exit_json(changed=changed, msg="Check mode: no se realizaron cambios.")

        if changed:
            # Crear/actualizar archivo
            with open(path, 'w') as f:
                f.write(content)

            # Cambiar permisos
            os.chmod(path, int(mode, 8))

            # Cambiar dueño y grupo si se especifica
            if owner:
                uid = pwd.getpwnam(owner).pw_uid
                gid = os.stat(path).st_gid
                os.chown(path, uid, gid)
            if group:
                gid = grp.getgrnam(group).gr_gid
                uid = os.stat(path).st_uid
                os.chown(path, uid, gid)

        module.exit_json(changed=changed, msg=f"Archivo {path} {'creado/actualizado' if changed else 'sin cambios'}.")

    except Exception as e:
        module.fail_json(msg=f"Error creando archivo: {str(e)}")

if __name__ == '__main__':
    main()