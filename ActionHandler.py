#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

class ActionHandler(object):

    def __init__(self):
        super(ActionHandler, self).__init__()
        self.informacionPersistida = {}
        self.mensajeEnviado = {}
        self.mensajeRecibido = {}

    def procesaAccion(self, modelDeDatos):
        if modelDeDatos["accion"] == "actualizar":
            identificador = modelDeDatos["identificador"]
            informacion = modelDeDatos["informacion"]
            self.informacionPersistida[identificador] = informacion
            return {"status" : "ok"}

        if modelDeDatos["accion"] == "enviar":
            return self.mandarMensaje(modelDeDatos)

        if modelDeDatos["accion"] == "listarMensajes":
            return {"status" : "ok",
                    "enviadoMsj" : self.mensajeEnviado}
                    #"obtenidoMsj" : self.mensajeRecibido}

        if modelDeDatos["accion"] == "recibir":
            return self.recibirMensajes(modelDeDatos)

        else:
            return {"status" : "ok",
                    "informacion" : self.informacionPersistida}

    def mandarMensaje(self, modelDeDatos):
        usuario = modelDeDatos["usuario"]
        mensaje = modelDeDatos["informacionMsj"]["mensaje"]
        horaFecha = modelDeDatos["informacionMsj"]["horaFecha"]
        mensajeAGuardar = {"mensaje" : mensaje, "horaFecha": horaFecha}

        if usuario in self.mensajeEnviado:
            contenedor = self.mensajeEnviado[usuario]
        else:
            contenedor = []
            self.mensajeEnviado[usuario] = contenedor

        contenedor.append(mensajeAGuardar)

        return {"status" : "ok", "enviadoMsj": self.mensajeEnviado}

    def recibirMensajes(self, modelDeDatos):
        usuario = modelDeDatos["usuario"]
        mensajesAlmacenados = self.mensajeEnviado[usuario]
        return {"status" : "ok", "recibidoMsj" : mensajesAlmacenados}

if __name__ == "__main__":

    modelDeDatosActualizar = {
        "accion" : "actualizar",
        "identificador" : "1",
        "informacion" : {
            "status" : "online",
            "usuario" : "Fanny",
            "identificador" : "192.168.1.65",
            "puerto" : 13375
        }
    }

    modelDeDatosActualizar1 = {
        "accion" : "actualizar",
        "identificador" : "2",
        "informacion" : {
            "status" : "online",
            "usuario" : "Luis",
            "identificador" : "192.168.1.65",
            "puerto" : 13378
        }
    }

    modelDeDatosListar = {
        "accion" : "listar"
    }

    enviarMensajeF = {
        "accion" : "enviar",
        "usuario" : "Fanny",
        "informacionMsj" : {
            "horaFecha" : datetime.datetime.now(),
            "mensaje" : "hola, como estas"
        }
    }

    enviarMensajeL = {
        "accion" : "enviar",
        "usuario" : "Luis",
        "informacionMsj" : {
            "horaFecha" : datetime.datetime.now(),
            "mensaje" : "muy bien y tu?"
        }
    }

    mensajesLista = {
        "accion" : "listarMensajes"
    }

    mensajesObtenerLuis = {
        "accion" : "recibir",
        "usuario" : "Luis"
    }

    mensajesObtenerFanny = {
        "accion" : "recibir",
        "usuario" : "Fanny"
    }


    actionHandler = ActionHandler()

    # Ejemplo Actualizar
    respuesta = actionHandler.procesaAccion(modelDeDatosActualizar)
    print respuesta
    respuesta1 = actionHandler.procesaAccion(modelDeDatosActualizar1)
    print respuesta1
    if respuesta["status"] == "ok":
        print "Correcto almacenamiento"
    else:
        print "Incorrecto almacenamiento"

    # Ejemplo Listar con un elemento
    respuesta_listado = actionHandler.procesaAccion(modelDeDatosListar)
    if respuesta_listado["status"] == "ok":
        informacion_listado = respuesta_listado["informacion"]
        print informacion_listado
        if len(informacion_listado) == 1 and informacion_listado["1"]["usuario"] == "Fanny":
            print "Correcto listado Fanny"
        else:
            print "Incorrecto listado Fanny"
        if len(informacion_listado) == 2 and informacion_listado["2"]["usuario"] == "Luis":
            print "Correcto listado Luis"
        else:
            print "Incorrecto listado Luis"
    else:
        print "Incorrecto listado"

    #Ejemplo Enviado
    enviado_Fanny = actionHandler.procesaAccion(enviarMensajeF)
    enviado_Luis = actionHandler.procesaAccion(enviarMensajeL)
    if enviado_Fanny["status"] == "ok" and enviado_Luis["status"] == "ok":
        print "Enviado correctamente"
    else:
        print "Fallo en el envio"


    #Ejemplo de lista de mensajes enviados
    lista_enviados = actionHandler.procesaAccion(mensajesLista)
    if lista_enviados["status"] == "ok":
        print lista_enviados["enviadoMsj"]
    else:
        print "Fallo mensaje"

    #Ejemplo Recibido
    respuesta_recibido = actionHandler.procesaAccion(mensajesObtenerFanny)
    if respuesta_recibido["status"] == "ok":
        print "Recibido"
    else:
        print "None"
