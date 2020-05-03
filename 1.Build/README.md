# README.md

En este directorio se encuentran los archivos que permiten crear una imagen de Docker y en la cual se encuentra desplegada la aplicación que se usa como ejemplo en este tutorial.

* `Dockerfile` es el archivo usado por el comando `docker build ...` para crear la imagen de Docker.

> Para este tutorial la imagen se creó de la siguiente manera `docker build -t andresdfx/flask-monitor . `.
> Posteriormente se subió a Docker Hub, `docker push andresdfx/flask-monitor`.

* `flask-task.py` Contiene la aplicación escrita en Python "Getings task Done".
* `flask-monitor.py` Contiene la aplicación escrita en Python para el monitoreo de recursos del sistema.
