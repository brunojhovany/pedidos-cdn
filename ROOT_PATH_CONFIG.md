# Configuración de Root Path para CDN

## Problema
Cuando la aplicación CDN se ejecuta detrás de un nginx que la sirve bajo una ruta específica (por ejemplo `/cdn/admin/`), es necesario configurar un root path para que todas las URLs internas funcionen correctamente.

## Solución Implementada

### 1. Configuración de nginx
Se agregaron headers en la configuración de nginx para informar a la aplicación Flask sobre el prefijo:

```nginx
proxy_set_header X-Script-Name /cdn/admin;
proxy_set_header X-Forwarded-Prefix /cdn/admin;
```

### 2. Configuración de Flask
Se implementó:
- Variable de entorno `APPLICATION_ROOT` para configurar el prefijo
- `ProxyFix` de Werkzeug para manejar headers del proxy
- Context processor para inyectar `APPLICATION_ROOT` en las templates

### 3. Actualización de Templates
Todas las URLs hardcodeadas se actualizaron para usar la variable `APPLICATION_ROOT`:
- URLs de archivos estáticos (`/static/...` → `{{ APPLICATION_ROOT }}/static/...`)
- URLs de formularios (`/upload` → `{{ APPLICATION_ROOT }}/upload`)
- URLs de archivos CDN (`/cdn/...` → `{{ APPLICATION_ROOT }}/cdn/...`)
- URLs de acciones (eliminar, ver, descargar)

## Configuración

### Variables de Entorno
```bash
APPLICATION_ROOT=/cdn/admin  # Ruta base donde se sirve la aplicación
PUBLIC_DNS_DOMAIN=tu-dominio.com  # Dominio público para enlaces CDN
```

### Nginx del Servidor Principal
En el nginx principal que sirve la aplicación bajo `/cdn/admin/`:

```nginx
location /cdn/admin/ {
    proxy_pass http://tu-contenedor:80/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Script-Name /cdn/admin;
    proxy_set_header X-Forwarded-Prefix /cdn/admin;
}
```

## Uso
1. Configura las variables de entorno apropiadas
2. La aplicación generará automáticamente URLs correctas con el prefijo
3. Los enlaces CDN públicos incluirán el dominio y el prefijo correcto
