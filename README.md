## 🧞‍♂️ Genie en Acción: Demo de IA en Databricks

En un mundo donde cada vez más decisiones dependen de datos, acercar la IA a los equipos de negocio y tecnología se vuelve esencial.  
Esta demo muestra cómo usar **Genie** para crear una **App de IA funcional en menos de 10 minutos**, facilitando la adopción de IA en toda la organización.

## 🚀 Instalación y despliegue

Sigue estos pasos para instalar y correr la aplicación en tu entorno de Databricks:

### 0. Pre-requisitos

* Tener un espacio funcional de Genie, consulta:  
[**Databricks AI/BI: Marketing Campaign Effectiveness with Dashboards and Genie**](https://www.databricks.com/resources/demos/tutorials/aibi-genie-marketing-campaign-effectiveness?itm_data=demo_center)

### 1. Clona este repositorio

`git clone https://github.com/tu-org/databricks-genie-demo.git
cd databricks-genie-demo`

### 2. Sube los archivos a tu workspace de Databricks
Puedes hacerlo directamente desde la interfaz de usuario de Databricks o usando la CLI:

`databricks workspace import_dir . /Repos/<tu_usuario>/<nombre_del_repositorio> -o`

### 3. Crea una nueva App en Databricks
- Ve a la pestaña "Apps" en tu workspace.
- Haz clic en "Create App".
- Selecciona "From existing code" y elige la ruta del repositorio importado.
- Define los siguientes parámetros:
- Nombre: Genie Demo
- Entry Point: app.py

### 4. Configura las variables de entorno
Asegúrate de definir las siguientes variables de entorno en la App (app.yaml):

  - `name: DATABRICKS_HOST
    value: "https://url_de_tu_workspace"`
  - `name: DATABRICKS_TOKEN
    value: "tu_databricks_token"`
  - `name: GENIE_SPACE_ID
    value: "tu_genie_space_id"`

### 5. Ejecuta la App
Haz clic en "Run" en la App y espera unos segundos a que se despliegue.
Tu aplicación estará lista para interactuar con Genie y mostrar resultados.

### 🤝 Contribuciones
¿Te gustaría mejorar esta demo? ¡Las pull requests son bienvenidas!</br>
Abre un issue si encuentras un error o deseas proponer una nueva funcionalidad.

### 📘 Acerca de Databricks Apps
**Databricks Apps** permiten a los desarrolladores implementar aplicaciones interactivas hechas con frameworks como Dash, Streamlit, y Gradio directamente en el entorno de Databricks. Estas apps son diseñadas para ejecutarse de forma serverless, lo que facilita la escalabilidad y su administración. Además, incluyen gobernanza integrada mediante Unity Catalog, lo que garantiza que los datos sean seguros y accesibles según los permisos asignados. Estas características ayudan a simplificar el desarrollo mientras mantienen la seguridad y el control de los datos en proyectos colaborativos.

### 🤖 Acerca de Genie
**Genie** es una herramienta de inteligencia artificial desarrollada por Databricks que permite interactuar con los datos usando lenguaje natural, proporcionando insights rápidos y precisos para preguntas ad hoc. Su diseño incluye capacidades para entender conceptos empresariales y relaciones en los datos, aprender continuamente, y ajustar sus respuestas según la retroalimentación del usuario. Genie opera exclusivamente con datos gobernados a través de Unity Catalog, asegurando seguridad y precisión, y requiere poco conocimiento técnico de los usuarios finales para realizar sus consultas. Además, los expertos pueden configurar espacios específicos en Genie donde se proporcionan conjuntos de datos, instrucciones, y consultas de ejemplo para facilitar las interacciones con los datos

### 🔗 Referencias Adicionales

* [Documentación de Databricks Apps:]( https://learn.microsoft.com/en-us/azure/databricks/dev-tools/databricks-apps/)
* [Blog oficial sobre Databricks Apps:](https://www.databricks.com/blog/introducing-databricks-apps)
* [Documentación sobre AI/BI Genie:](https://learn.microsoft.com/en-us/azure/databricks/genie/)
* [Blog oficial sobre AI/BI Genie:](https://www.databricks.com/blog/onboarding-your-new-aibi-genie)


### 🌎 Comunidad Databricks en Español

- Grupo en LinkedIn [Databricks en Español- El Lakehouse](https://www.linkedin.com/groups/14082071/)

</br>

 