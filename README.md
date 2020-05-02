<div align="justify">
<h1><u> FlaskRest</u></h1>

(ToDo)

Para el tutorial completo y la generalizacion del problema [Vagrantfile](./Vagrantfile)
El estilo arquitectural RESTful es una de las arquiecturas de software orientadas a servicios más populares hoy en día. Esto se evidencia en el hecho que muchas de las plataformas centradas en la nube ofrecen su información y servicios siguiendo este estilo arquitectural.

El microframework [Flask](https://flask.palletsprojects.com/en/1.1.x/) permite el fácil desarrollo y despliegue de servicios que siguen el esquema arquitectura RESTful. Creditos al docente [josanabr](https://github.com/josanabr).

La definicion de la VM utilizada para pruebas se encuentra en el siguiente [Vagrantfile](./Vagrantfile).

---
<h2><u>Parte 1 - Monitoreo del servidor</u></h2>

En el archivo [flask-monitor.py](./1.Build/flask-monitor.py) se encuentran todos los ejercicios desarrollados. Dentro del archivo se encontrarán **EJEMPLO**s y encontrarán **EJERCICIO**s. 

---
<h3><u>Rutas</u></h3>

En este momento los siguientes recursos están disponibles para `flask-monitor.py`:

* *GET* **/index.html** devuelve en formato JSON todas las rutas del web services. 
  
* *GET* **/os** devuelve en formato JSON la salida del comando uname. Es posible pedir valores específicos mediante POST.
	* *POST* **/os/kernel**
	* *POST* **/os/release**
	* *POST* **/os/nodename**
	* *POST* **/os/kernelversion**
	* *POST* **/os/machine**
	* *POST* **/os/processor**
	* *POST* **/os/operatingsystem**
	* *POST* **/os/hardware**

* *GET* **/who** devuelve en formato JSON los usuarios conectados en ese momento
	* *POST* **/who/\<user\>** envia un JSON y devuelve si el usuario especifico `<user>` esta conectado

* *GET* **/cpu/\<type\>** devuelve en formato JSON el uso de la CPU. Posibles valores para `<type>`:
	* **us** user
	* **sy** system
	* **id** idle
	* **wa** waiting 
	* **st** tiempo consumido por máquinas virtuales

* *GET* **/mem/\<type\>** devuelve en formato JSON el uso de RAM. Posibles valores para `<type>`:
	* **swpd** swap
	* **free** free
	* **buff** buffered
	* **cache** cached 

* *POST* **/partition/** envia un JSON y devuelve el uso de la particion especifica o la lista de todas las particiones si se utiliza `all`

* *GET* **/swap/\<type\>** devuelve en formato JSON el comportamiento de SWAP. Posibles valores para `<type>`:
	* **si** memory swapped in
	* **so** memory swapped out
  
---
<h2><u>Parte 2 - API REST</u></h2>

En el archivo [flask-task.py](./1.Build/flask-task.py) se encuentra una aplicación que modela el proceso *Getting Things Done* bajo un esquema API REST. Diapositivas asociadas a este problema se encuentran [aquí](https://docs.google.com/presentation/d/13in0zrKxB3gU6OPA0-G6l0C9trTVvGhtrMD5yUUMPgs/edit?usp=sharing).

<h3><u>Rutas</u></h3>

En este momento los siguientes recursos están disponibles para `flask-task.py`:
(ToDo)

---
<h2><u>Instalacion</u></h2>

docker pull andresdfx/flask-monitor 
docker run --rm -d -p 5000:5000 andresdfx/flask-monitor
(ToDo)
usar el comando `export REMOTE="34.83.147.81:8000"`

</div>

