# Política de seguridad

IntelliAgent es un proyecto académico y de portafolio. La API no tiene autenticación, así que no debe exponerse a internet sin los cambios descritos abajo.

## Cómo reportar una vulnerabilidad

- No abra un issue público ni publique el hallazgo en un canal abierto.
- Use los avisos privados de seguridad de GitHub del repositorio `deadlyrat/IntelliAgent`: pestaña Security, opción "Report a vulnerability".
- Incluya la descripción del problema, los pasos para reproducirlo, el componente afectado (archivo o endpoint) y el impacto estimado.
- No incluya credenciales reales ni datos personales en el reporte. Use valores ficticios.
- El mantenedor confirmará la recepción y dará seguimiento. Los plazos dependen de su disponibilidad.

## Versiones soportadas

El repositorio no publica versiones. Solo se mantiene la rama principal (`main`).

## Manejo de secretos

- El archivo `.env` no se versiona: el `.gitignore` lo excluye. Use `.env.example` solo como plantilla con valores ficticios.
- Las claves del modelo de lenguaje, la cuenta de correo y Trello llegan por variables de entorno. No las pegue en issues, commits ni capturas.
- Rote de inmediato cualquier credencial que se haya expuesto. Una credencial que estuvo en el historial de git se considera comprometida hasta que se rote.
- Para el correo use una contraseña de aplicación, no la contraseña de la cuenta.

## Limitaciones de seguridad conocidas

Lista neutral de puntos pendientes identificados al revisar el código. No incluye valores de credenciales y no se modificó código para corregirlos.

1. La API no tiene autenticación ni autorización. `API_KEY` solo se exige que exista al arrancar (`main.py`) y no se usa para validar peticiones. Quien llegue por red a la API puede crear, listar y borrar tareas de investigación, y disparar envíos de correo y tarjetas de Trello.
2. CORS acepta cualquier origen (`allow_origins=["*"]`) con `allow_credentials=True`. El comentario del código indica restringirlo en producción.
3. `compose.yaml` y `compose.prod.yaml` escriben en texto plano el usuario, la contraseña y el nombre de la base de datos de ejemplo. Los valores son de ejemplo y deben cambiarse antes de usar el archivo fuera de un equipo local. `.env.sample-db` define las mismas tres variables, pero Compose no lo lee.
4. El puerto 5433 de PostgreSQL y el 8080 del backend se publican en el host, también en `compose.prod.yaml`. En un servidor con IP pública quedan accesibles desde fuera salvo que un firewall lo impida.
5. La clave y el token de Trello se envían como parámetros de la URL (query string) en cada petición. Pueden quedar registrados en logs de proxies o del servicio.
6. `check_setup.py` imprime los primeros 10 caracteres de varios valores del `.env` (claves de API y token). No lo ejecute con la pantalla compartida ni guarde su salida en registros públicos.
7. La tarea en segundo plano de investigación reutiliza la sesión de base de datos de la petición HTTP. Esa sesión puede cerrarse al terminar la respuesta, por lo que su uso posterior es frágil.
8. No hay limitación de peticiones (rate limiting) ni HTTPS en la configuración incluida. Cada petición a `POST /api/research/tasks/` y `POST /api/chats/` genera llamadas al modelo de lenguaje, con costo asociado.
9. Los errores de correo y Trello se imprimen en la salida estándar y la tarea queda como `completed` aunque la entrega haya fallado.

## Recomendaciones

- Agregue autenticación a la API (por ejemplo, validar `API_KEY` en una dependencia de FastAPI) antes de publicarla.
- Limite `allow_origins` a los dominios del frontend y no combine `*` con credenciales.
- Mueva el usuario y la contraseña de la base de datos a variables de entorno y use valores propios y largos.
- No publique los puertos 5433 y 8080 en producción: deje solo el del proxy inverso con HTTPS.
- Si es posible, restrinja el acceso a la API por IP o por VPN.
- Use cuentas con permisos mínimos para el correo y el modelo de lenguaje, con límites de gasto.
