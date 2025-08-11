# CICD-webhook-en-Linux-con-Flask

**Proyecto listo para producción** de un webhook Flask que se ejecuta detrás de **Nginx** usando **Gunicorn**, con validación de firma de GitHub, ejecución de `git fetch` + `git reset` y reinicio del servicio web.

  * * *

## **1️⃣ Código Python del webhook**

Guarda esto como `webhook.py` en tu servidor: (archivo:webhook.py)

  

## **2️⃣ Servicio systemd para Gunicorn**

Crea un servicio en `/etc/systemd/system/webhook.service: (archivo: webhook.service)`

`   `

Luego habilita y arranca:

  
  

`sudo systemctl daemon-reload sudo systemctl enable webhook sudo systemctl start webhook`

* * *

## **3️⃣ Configuración Nginx**

Archivo `/etc/nginx/sites-available/webhook.conf`: (archivo: webhook.conf)

  

Habilita el sitio y recarga Nginx:

  
  

`sudo ln -s /etc/nginx/sites-available/webhook.conf /etc/nginx/sites-enabled/ sudo nginx -t sudo systemctl reload nginx`

  * * *

## **4️⃣ Configuración en GitHub**

1.  Ve a **Settings → Webhooks → Add webhook**.
    
2.  **Payload URL**
    

`http://tu-dominio.com/pull-repo`

  

1.  **Content type:** `application/json`.
    
2.  **Secret:** tu clave secreta (`WEBHOOK_SECRET`).
    
3.  Eventos: selecciona **Just the push event**.
    
4.  Guarda y prueba.
    

* * *

## **5️⃣ Flujo final**

Cuando hagas un `git push`:

1.  GitHub envía POST al endpoint `/pull-repo`.
    
2.  Flask valida que el webhook es legítimo.
    
3.  Se hace `git fetch` + `git reset --hard`.
    
4.  Se reinicia el servicio del sitio (`mi-sitio.service`).

* * *

1.  ### 🔹 ... y GitHub Actions? Lo que hace
    
    -   Permite flujos mucho más complejos (tests, builds, lint, despliegues múltiples).
        
    -   Ejecuta pasos en runners de GitHub o propios (self-hosted runners).
        
    -   Puede desplegar a múltiples entornos o nubes (AWS, Azure, GCP, etc.).
        
    -   Aporta integración con marketplace y miles de acciones prehechas.
        
    -   Pero… **requiere más configuración** y depende de un servicio externo.
