#!/usr/bin/env python
#
# El siguiente programa permite obtener, via web services, algunos valores
# referentes al estado de un servidor con sistema operativo Linux.
#
# El codigo presenta algunas partes ya codificadas y que le serviran a usted:
#
# 1- Probar los servicios que ya estan implementados y verlos en operacion
# 2- Como guia para desarrollar sus propios web services.
#
# NOTA: Dentro de este codigo se ejecutan algunos comandos de la linea de
# comandos. IMPORTANTE: No usar las funciones 'os.system' o 'os.spawn' ya que
# son funciones que pueden llevar a vulnerabilidades dentro del codigo.
# REF: https://raspberrypi.stackexchange.com/questions/17017/how-do-i-run-a-command-line-command-in-a-python-script
#
# Usar la libreria 'subprocess' de Python.
#
# Author: Julian Andres Castaño
# Date: 02/05/2020
#

# Librerias que se requieren para correr la aplicacion
from flask import Flask, jsonify, abort, make_response, request
import subprocess

# Se crea un objeto de tipo Flask llamado 'app'
app = Flask(__name__)

#
# A continuacion se ejemplificaran algunos 'end points' del web service que
# representa a un servidor.
#
# ---------------------------------------------------------------------------
#
# +------------+
# | EJEMPLO 01 |
# +------------+ |
#   +------------+
#
# Metodo usado para determinar el uso de memoria usando el aplicativo 'vmstat'
#
# Posibles metodos de acceso
#
# curl http://localhost:5000/mem/swpd
# curl http://localhost:5000/mem/free
# curl http://localhost:5000/mem/buff
# curl http://localhost:5000/mem/cache
#
# NOTA
# Observe que para obtener el dato de memoria requerido por el usuario se llevo
# a cabo la ejecucion del programa 'vmstat'. 'vmstat' ofrece informacion
# precisa y en tiempo real del sistema. En este enlace usted podra encontrar mas
# detalles respecto a la herramienta:
#
# https://access.redhat.com/solutions/1160343
#
# Lo que se ha hecho con metodos de Python es ejecutar este comando equivalente
# por la linea de comandos:
#
# vmstat | tail -n 1 | tr -s ' ' | cut -d ' ' -f value
#
# Donde 'value' puede ser '4', '5', '6' o '7'.
#
@app.route('/mem/<string:param>', methods=['GET'])
def mem(param):
    if (param == "swpd"):
        value = "4"
    elif (param == "free"):
        value = "5"
    elif (param == "buff"):
        value = "6"
    elif (param == "cache"):
        value = "7"
    else:
        return make_response(jsonify({'error': 'Possible values swpd, free, buff, cache'}), 404)
    vmstat = subprocess.Popen(['vmstat'], stdout=subprocess.PIPE)
    tail = subprocess.Popen(['tail', '-n', '1'],
                            stdin=vmstat.stdout, stdout=subprocess.PIPE)
    tr = subprocess.Popen(
        ['tr', '-s', ' '], stdin=tail.stdout, stdout=subprocess.PIPE)

    output = subprocess.check_output(
        ['cut', '-d', ' ', '-f', value], stdin=tr.stdout)
    return jsonify({'mem %s' % param: output})

#
# +------------+
# | EJEMPLO 02 |-+
# +------------+ |
#   +------------+
#
# El mismo metodo anterior pero usando el metodo 'POST' del protocolo HTTP.
#
# Para probar este 'end point'  se puede invocar el siguiente comando:
#
# curl -X POST -H "Content-type: application/json" -d '{"mem": "cache" }' http://localhost:5000/mem
#
#
@app.route('/mem', methods=['POST'])
def memp():
    if not request.json or not 'mem' in request.json:
        abort(404)
    return mem(request.json['mem'])
#
# +------------+
# | EJEMPLO 03 |
# +------------+ |
#   +------------+
#
# Este metodo se usa para determinar que personas estan conectadas a un servidor
# usando el comando 'who'. Si usted no sabe como funciona el comando 'who', por
# favor abra una terminal y ejecute 'who'.
#
# Este codigo muestra como en Python se puede acceder al resultado de ejecutar
# el comando 'who' y presentar el resultado en formato 'json'.
#
# Observe, sin embargo, que este comando es mucho mas que solo correr el comando
# 'who', lo que se esta ejecutando realmente es:
#
# 'who | cut -d ' ' -f 1 | uniq'
#
# Ahora, ejecute el comando anterior en una terminal.
#
# La forma como debe consumirse este servicio desde terminal es:
#
# curl http://localhost:5000/who
#
#
@app.route('/who', methods=['GET'])
def who():
    who = subprocess.Popen(['who'], stdout=subprocess.PIPE)
    cut = subprocess.Popen(['cut', '-d', ' ', '-f', '1'],
                           stdin=who.stdout, stdout=subprocess.PIPE)
    output = subprocess.check_output(('uniq'), stdin=cut.stdout)
    return jsonify({'users': output})

#
#
# +------------+
# | EJEMPLO 04 |-+
# +------------+ |
#   +------------+
#
# Web service que entrega informacion relativa a esta maquina
#
# curl http://localhost:5000/os
#
@app.route('/os', methods=['GET'])
def os():
    kernel = subprocess.check_output(['uname', '-s'])
    release = subprocess.check_output(['uname', '-r'])
    nodename = subprocess.check_output(['uname', '-n'])
    kernelv = subprocess.check_output(['uname', '-v'])
    machine = subprocess.check_output(['uname', '-m'])
    processor = subprocess.check_output(['uname', '-p'])
    os = subprocess.check_output(['uname', '-o'])
    hardware = subprocess.check_output(['uname', '-i'])
    return jsonify({'kernel': kernel,
                    'release': release,
                    'nodename': nodename,
                    'kernelversion': kernelv,
                    'machine': machine,
                    'processor': processor,
                    'operatingsystem': os,
                    'hardware': hardware})


#
#
# +---------------------+
# | FIN DE LOS EJEMPLOS |
# +---------------------+ |
#   +---------------------+
#
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
#
#
# --->    EJERCICIOS PROPUESTOS    <---
#
# +--------------+
# | EJERCICIO 01 |-+
# +--------------+ |
#   +--------------+
#
#
# Modifique este metodo de modo que cuando el usuario acceda a cualquiera de
# las rutas aqui definidas le aparezca un mensaje donde se indica los posibles
# servicios que puede consumir
#
# curl http://localhost:5000
# curl http://localhost:5000/index.htm
# curl http://localhost:5000/index.html
#
@app.route('/')
@app.route('/index.htm')
@app.route('/index.html')
def index():
    #
    # Almacene en una variable llamada 'output' un mensaje que describa
    # todos los 'web services' o 'end points' definidos en este programa
    #
    output = []

    for rule in app.url_map.iter_rules():
        output.append('%s' % rule)

    return jsonify({'available services': output})


#
# +--------------+
# | EJERCICIO 02 |-+
# +--------------+ |
#   +--------------+
#
# Este metodo permite determinar si un usuario en particular esta conectado.
# El comando usado en el shell para esta tarea es:
#
# 'who | cut -d ' ' -f 1 | grep ${USERNAME} | uniq'
#
# Vale la pena recalcar que el nombre del usuario que se desea validar si esta o
# no conectado es 'user', el 'user' que se pasa como argumento al metodo 'who'
#
# La forma como debe consumirse este servicio desde terminal es:
#
# curl http://localhost:5000/who/vagrant
#
@app.route('/who/<string:user>', methods=['GET'])
def whou(user):
    #
    # Escriba aqui su codigo. El nombre del usuario que desea buscar se
    # encuentra definido en la variable 'user'.
    #
    # Tenga en cuenta que el resultado de la ejecucion del comando debe
    # quedar en la variable 'output'
    #
    who = subprocess.Popen(['who'], stdout=subprocess.PIPE)
    cut = subprocess.Popen(['cut', '-d', ' ', '-f', '1'],stdin=who.stdout, stdout=subprocess.PIPE)
    grep = subprocess.Popen(['grep', user], stdin=cut.stdout, stdout=subprocess.PIPE)
    output = subprocess.check_output(('uniq'), stdin=grep.stdout)


    return jsonify({'loggedin': output})


#
#
# +--------------+
# | EJERCICIO 03 |-+
# +--------------+ |
#   +--------------+
#
# Desarrolle la version 'POST' del comando anterior. Es decir, que el web
# service responda ante un comando como el siguiente:
#
# curl -X POST -H "Content-type: application/json" -d '{ "user": "john" }' http://localhost:5000/who
# curl -X POST -H "Content-type: application/json" -d '{ "user": "vagrant" }' http://localhost:5000/who
#
# y determine si el usuario esta o no en el sistema
#
# RESTRICCION: Debe usar el metodo 'whou' del punto anterior en esta
# implementacion
#
# SU CODIGO AQUI
#
@app.route('/who', methods=['POST'])
def whos():
    #
    # Escriba aqui su codigo. El nombre del usuario que desea buscar se
    # encuentra definido en la variable 'user'.
    #
    # Tenga en cuenta que el resultado de la ejecucion del comando debe
    # quedar en la variable 'output'
    #

    if not request.json or not 'user' in request.json:
        abort(404)

    value = whou(request.json['user'])
    output = value.json['loggedin']

    if (output == ""):
        output = "user not exists"

    return jsonify({'exists': output})



#
# +--------------+
# | EJERCICIO 04 |-+
# +--------------+ |
#   +--------------+
#
# Este metodo es usado para determinar el uso de la CPU. Para ello se utiliza
# el comando 'vmstat'. Abra una terminal y ejecute dicho comando.
#
# Si quiere saber mas detalles de este comando, desde la terminal, ejecute el
# comando 'man vmstat' o visite https://linux.die.net/man/8/vmstat
#
# Una vez se ejecuta el comando, este arroja varios valores que segun su
# posicion representan porcentajes del total del tiempo de la CPU:
#
# 14: tiempo invertido en la ejecucion de codigo que no es del kernel
# 15: tiempo invertido en la ejecucion de codigo del kernel
# 16: tiempo inactivo
# 17: tiempo invertido en la espera de operaciones de IO
# 18: tiempo que se toma desde una maquina virtual
#
# El comando que se usa aqui para sacar los valores es
#
# vmstat | tail -n +3 | tr -s ' ' | cut -d ' ' -f n
#
# donde n puede ser: 14, 15, 16, 17 o 18
#
# La forma como se invoca este web service puede ser
#
# curl http://localhost:5000/cpu/us (valor 14)
# curl http://localhost:5000/cpu/sy (valor 15)
# curl http://localhost:5000/cpu/id (valor 16)
# curl http://localhost:5000/cpu/wa (valor 17)
# curl http://localhost:5000/cpu/st (valor 18)
#
# Entones, la variable 'param' puede tener el valor 'us', 'sy', 'id', 'wa' o 'st'
#
# IMPORTANTE
#
# Si el valor en 'param' no es ninguno de los valores anteriores enviar un
# mensaje de error.
#
@app.route('/cpu/<string:param>', methods=['GET'])
def cpuwa(param):

    #
    # Escriba aqui su codigo. El tipo de valor de la CPU que se quiere
    # acceder se encuentra definido en la variable 'param'.
    #

    if (param == "us"):
        value = "14"
    elif (param == "sy"):
        value = "15"
    elif (param == "id"):
        value = "16"
    elif (param == "wa"):
        value = "17"
    elif (param == "st"):
        value = "18"
    else:
        return make_response(jsonify({'error': 'Possible values us, sy, id, wa, st'}), 404)

    vmstat = subprocess.Popen(['vmstat'], stdout=subprocess.PIPE)
    tail = subprocess.Popen(['tail', '-n', '+3'], stdin=vmstat.stdout, stdout=subprocess.PIPE)
    tr = subprocess.Popen(['tr', '-s', ' '], stdin=tail.stdout, stdout=subprocess.PIPE)
    output = subprocess.check_output(['cut', '-d', ' ', '-f', value], stdin=tr.stdout)
    
    return jsonify({'vmstat %s' % param: output})


#
#
# +--------------+
# | EJERCICIO 05 |-+
# +--------------+ |
#   +--------------+
#
# El 'EJEMPLO 04' muestra diferentes datos respecto al SO del servidor
#
# Escriba un 'end point' que se pueda acceder via el metodo 'POST' y que
# se invoque via curl de la siguiente forma
#
# curl -X POST -H "Content-type: application/json" -d '{"feature": valor }' http://localhost:5000/os
#
# donde 'valor' puede tomar los siguientes valores
#
# - kernel
# - release
# - nodename
# - kernelversion
# - machine
# - processor
# - operatingsystem
# - hardware
#
# Use el comando 'uname -a' para encontrar los valores que puede solicitar el
# usuario.
#
# Si el usuario digita este comando:
#
# curl -X POST -H "Content-type: application/json" -d '{ "feature": "kernel" }' http://localhost:5000/os
#
# La respuesta debe ser en formato JSON y algo como lo siguiente:
#
# {
#   "kernel": "Linux\n"
# }
#
# Si la caracteristica indicada no se encuentra disponible presente el
# correspondiente mensaje de error
#
# SU CODIGO AQUI
@app.route('/os', methods=['POST'])
def uname():
    try:
      if not request.json or not 'feature' in request.json:
          abort(404)

      jsonComplete = os()
      value = request.json['feature']
      query = jsonComplete.json[value]
      return jsonify({value: query})
        
    except KeyError:
      return jsonify({'error': "The route not exists"})

#
#
# +--------------+
# | EJERCICIO 06 |-+
# +--------------+ |
#   +--------------+
#
# Defina un 'end point' de modo que el usuario pueda llevar a cabo la
# siguiente consulta:
#
# curl -X POST -H "Content-type: application/json" -d '{ "partition": "" }' http://localhost:5000/partition
#
# Y el metodo haga lo siguiente:
#
# Si "partition" == "": entonces que entregue en formato JSON todas las
# particiones que tiene el sistema. El comando 'df -h' las muestras. El web
# service deberia entregar algo como:
# {
#  "partition": "udev\n/dev/sda1\ntmpfs\n"
# }
#
# Si "partition" == "/dev/sda1": el metodo retornara el espacio ocupado en dicha
# particion. Ejemplo:
#
# curl -X POST -H "Content-type: application/json" -d '{ "partition": "/dev/sda1" }' http://localhost:5000/partition
#
# {
#  "partition": "13%"
# }
#
# Si la partition dada por el usuario no se encuentra entonces enviar un
# mensaje de error como corresponde
#
# {
#  "error": "partition not found"
# }
#
# SU CODIGO AQUI
#
@app.route('/partition', methods=['POST'])
def partition():


    if not request.json or not 'partition' in request.json:
          abort(404)

     
    value = request.json['partition']

    #Proceso principal
    df = subprocess.Popen(['df', '-h'], stdout=subprocess.PIPE)

    if (value == ""):
      
      sed = subprocess.Popen(['sed', '1d'], stdin=df.stdout, stdout=subprocess.PIPE)
      awk = subprocess.check_output(['awk', '{print $1}'], stdin=sed.stdout)
      return jsonify({"all partitions": awk.split("\n")})

    else:
      grep = subprocess.Popen(['grep', '-n', value], stdin=df.stdout, stdout=subprocess.PIPE)
      awk = subprocess.check_output(['awk', '{print $5}'], stdin=grep.stdout)
      
      if (awk != ""):
         return jsonify({'percentage partition %s' % value: awk})

      else:
         return jsonify({"error": "partition not found"})
  

#
# +--------------+
# | EJERCICIO 07 |-+
# +--------------+ |
#   +--------------+
#
# Defina un 'end point' en el cual el usuario puede ejecutar el siguiente comando:
#
# curl -X POST -H "Content-type: application/json" -d '{ "processes": valor }' http://localhost:5000/processes
#
# Si "valor" == "all": muestra todos los procsos que actualmente corren en el
# sistema

# curl -X POST -H "Content-type: application/json" -d '{ "processes": "all" }' http://localhost:5000/processes
# Si "valor" == "user": donde "user" es un usuario valido entonces devuelve el
# numero de procesos en ejecucion por ese usuario
#

# curl -X POST -H "Content-type: application/json" -d '{ "processes": "vagrant" }' http://localhost:5000/processes
# SU CODIGO AQUI
#

@app.route('/processes', methods=['POST'])
def processes():

    if not request.json or not 'processes' in request.json:
        abort(404)

    value = request.json['processes']
    output = []

    if (value == "all"):
        ps = subprocess.Popen(['ps', '-ef'], stdout=subprocess.PIPE)
        sed = subprocess.Popen(['sed', '1d'], stdin=ps.stdout, stdout=subprocess.PIPE)
        awk = subprocess.check_output(['awk', '{print $8}'], stdin=sed.stdout)
        output = awk.split("\n")
        return jsonify({"all processes": output})

    else:
        ps = subprocess.Popen(['ps', '-u', value], stdout=subprocess.PIPE)
        sed = subprocess.Popen(['sed', '1d'], stdin=ps.stdout, stdout=subprocess.PIPE)
        awk = subprocess.check_output(['awk', '{print $4}'], stdin=sed.stdout)
        output = awk.split("\n")

        if (awk != ""):
            return jsonify({'processes for user % s' % value: output})

        else:
            return jsonify({"error": "user not found"})
  

#
# EXTRA: Método utilizado para determinar el comportamiento de SWAP.
# El comando usado es 'vmstat'
#
@app.route('/swap/<string:param>', methods=['GET'])
def swap(param):
	vmstat = subprocess.Popen(['vmstat'], stdout=subprocess.PIPE)
	tail = subprocess.Popen(['tail', '-n', '+3'],
	                        stdin=vmstat.stdout, stdout=subprocess.PIPE)
	tr = subprocess.Popen(
	    ['tr', '-s', ' '], stdin=tail.stdout, stdout=subprocess.PIPE)
	if (param == "si"):
	    value = "8"
	elif (param == "so"):
	    value = "9"
	else:
	    return make_response(jsonify({'error': 'Possible values si, so'}), 404)

	output = subprocess.check_output(
	    ['cut', '-d', ' ', '-f', value], stdin=tr.stdout)
	return jsonify({'swap %s' % param: output})

#
# Este es el punto donde arranca la ejecucion del programa
#
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
