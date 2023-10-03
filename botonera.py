import telebot
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
from telebot.types import ForceReply
import threading
from time import sleep
import time

hora_publicacion=[]
tiempo_de_espera_botonera=10800
ejecutar_hilo=True
foto_LastBotonera=open("D:\\Last_Botonera.jpg", 'rb')
archivo_canales=open("D:\\canales.txt", "r+")

bot=telebot.TeleBot("5818205719:AAF9dvuVzM6_tl4zNSL_k1af2B5NiXXba7s")

bot.set_my_commands([
    telebot.types.BotCommand("/start", "Da una introducción de cómo funciona dicho bot y para que es"),
    telebot.types.BotCommand("/mostrar", "Muestra los canales que conforman la botonera e información"),
    telebot.types.BotCommand("/ingresar", "Ingresa SU canal en la botonera junto con los demás"),
    telebot.types.BotCommand("/panel_administrador", "SÓLO disponible para mi creador ;)")
])

usuario=bot.user

def cancelar(message):
    bot.send_message(message.chat.id, "Envía /cancelar para cancelar la operación actual\nTodos tienen el derecho de arrepentirse\n\n(p≧w≦q)＼(ﾟｰﾟ＼)")

@bot.message_handler(commands=["panel_administrador"])
def cmd_comenzar(message, archivo_canales=archivo_canales, foto_LastBotonera=foto_LastBotonera):
    if message.chat.id==1413725506:
        botonera_panel=InlineKeyboardMarkup(row_width=1)
        b1=InlineKeyboardButton("Iniciar bucle de publicaciones 🙌", callback_data="Iniciar bucle")
        b2=InlineKeyboardButton("Parar el bucle de publicaciones 🖐", callback_data="Parar bucle")
        b3=InlineKeyboardButton("Agregar un canal a la lista de canales 👀", callback_data="Agregar canal")
        b4=InlineKeyboardButton("Eliminar un canal de la lista de canales 💨", callback_data="Eliminar canal")
        b5=InlineKeyboardButton("Modificar el tiempo de la botonera ⌛", callback_data="Modificar tiempo")
        botonera_panel.add(b1,b2,b3,b4,b5)


        bot.send_message(message.chat.id, "Bienvenido Reima ;) Qué planeas hacer?", reply_markup=botonera_panel)
        @bot.callback_query_handler(func=lambda x: True)
        def respuesta_callback(call, archivo_canales=archivo_canales, foto_LastBotonera=foto_LastBotonera, ejecutar_hilo=ejecutar_hilo):
            global hora_siguiente_publicacion
            archivo_canales.seek(0)
            foto_LastBotonera.seek(0)
            markup=ForceReply()
            if call.data=="Iniciar bucle":
                def hacer_publicaciones(ejecutar_hilo=ejecutar_hilo):
                    global hora_publicacion
                    while ejecutar_hilo:
                        archivo_canales.seek(0)
                        foto_LastBotonera.seek(0)
                        bot.send_message(message.chat.id, "Comenzaré a hacer las publicaciones")
                        botonera=InlineKeyboardMarkup(row_width=1)
                        #Primeramente, tengo que asegurarme que el bot tenga permisos para publicar en el canal
                        lista_canales=archivo_canales.readlines()
                        def buscar_administracion(archivo_canales=archivo_canales):
                            for e,canal in enumerate(lista_canales,start=0):
                                member=bot.get_chat_member(chat_id=canal, user_id=bot.user.id)
                                if not member.status=="administrator":
                                    del lista_canales[e]
                                    archivo_canales.seek(0)
                                    archivo_canales.writelines(lista_canales)
                                    archivo_canales.truncate()
                                    bot.send_message(1413725506, f"Se ha eliminado el canal {bot.get_chat(canal).username} por no dejarme como administrador >:(")
                                    archivo_canales.seek(0)
                                    return buscar_administracion(archivo_canales)
                        for canal in lista_canales:
                            #Si el bot tiene permisos pues agrega el canal a la botonera
                            nombre=bot.get_chat(canal).title
                            enlace=f"https://t.me/{bot.get_chat(canal).username}"
                            boton=InlineKeyboardButton(nombre, url=enlace)
                            botonera.add(boton)
                        for canal in lista_canales:
                            bot.send_photo(int(canal), foto_LastBotonera, caption="¡Si!, ¡Es eso mismo que estás pensando!\n Literalmente, <b>La Última Botonera</b> baby (☞ﾟヮﾟ)☞ ☜(ﾟヮﾟ☜)\n\n¡Oye Juan! ¿Quién hizo ese logo? ¡Quiero tatuarme eso en el c*lo!", parse_mode="html" , reply_markup=botonera)
                        archivo_canales.seek(0)
                        foto_LastBotonera.seek(0)
                        hora_publicacion.append(time.time())
                        sleep(tiempo_de_espera_botonera)
                hilo_publicaciones=threading.Thread(name="hilo_publicaciones", target=hacer_publicaciones)
                hilo_publicaciones.start()


            elif call.data=="Parar bucle":
                global hora_publicacion
                if hora_publicacion==[]:
                    return bot.send_message(message.chat.id, "Ni siquiera está activo el bucle :l\n\nPrueba otra cosa")
                    
                ejecutar_hilo=False
                hora_publicacion=[]
                return bot.send_message(message.chat.id, f"El hilo de publicaciones ha sido detenido exitosamente mi queridísimo Reima ;D\n\n<u>Hilos activos</u>:\n{threading.active_count()}", parse_mode="html")
                

            
            elif call.data=="Agregar canal":
                msg=bot.send_message(message.chat.id, "Muy bien, dime el @username del canal", reply_markup=markup)
                bot.register_next_step_handler(msg, registro_de_admin)
                def registro_de_admin(message):
                    try:
                        chat=bot.get_chat(message.text)
                    except:
                        msg=bot.send_message(message.chat.id, "El canal que ingresaste no existe, vuelve a intentar\nIngresa un @username válido")
                        bot.register_next_step_handler(msg, registro_de_admin)
                    else:
                        if bot.get_chat_member(chat.id, bot.user.id).status!="administrator":
                            bot.send_message(message.chat.id, "No soy admin en ese chat, pero bueno, ya sabrás tú lo que haces....")
                        archivo_canales.write(chat.id)
                        return bot.send_message(message.chat.id, "Agregado a la botonera")
            elif call.data=="Eliminar canal":
                msg=bot.send_message(message.chat.id, "Ahora escribe el @username del chat al que quieres eliminar", reply_markup=markup)
                bot.register_next_step_handler(msg, eliminacion_de_grupo_admin)

                def eliminacion_de_grupo_admin(message):
                    try:
                        chat=bot.get_chat(message)
                    except:
                        msg=bot.send_message(message.chat.id, "El canal no existe o lo escribiste de forma incorrecta\nVuelve a intentarlo")
                        bot.register_next_step_handler(msg, eliminacion_de_grupo_admin)

                    archivo_canales.seek(0)
                    canales=archivo_canales.readlines()
                    contador=0
                    for e,canal in enumerate(canales, start=0):
                        if canal==chat.id:
                            contador+=1
                            del canales[e]
                            archivo_canales.seek(0)
                            archivo_canales.writelines(canales)
                            archivo_canales.truncate()
                    return bot.send_message(message.chat.id, f"Ha(n) sido eliminado(s) <b>{contador}</b> chat(s) de la botonera", parse_mode="html")
            
            elif call.data=="Modificar tiempo":
                msg=bot.send_message(message.chat.id, "Cada cuánto tiempo planeas que la botonera se publique?\n\nIngresa el valor en minutos", reply_markup=markup)
                bot.register_next_step_handler(msg, tiempo_botonera)

                def tiempo_botonera(message):
                    if message.text.isdigit():
                        tiempo_de_espera_botonera=int(message.text)*60
                        bot.send_message(message.chat.id, f"La próxima vez que se enviará la botonera será a las {time.strftime('%H:%M', time.localtime(time.time()+tiempo_de_espera_botonera))}")
                        return tiempo_de_espera_botonera
                    else:
                        msg=bot.send_message(message.chat.id, "No has introducido correctamente un valor númerico en minutos para el tiempo de espera\nVuelve a intentarlo", reply_markup=markup)
                        bot.register_next_step_handler(msg, tiempo_botonera)

    else:
        bot.send_message(message.chat.id, "Lo siento mirei ;)\n\nNo eres mi creador como para mandarme ese mensaje >:D y decirme qué hacer")
        return
        
            

@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.send_message(message.chat.id, "Hola! 😁, Bienvenido a <b>Last Botonera</b> bot.\nAquí se encuentran los canales afiliados a la botonera y por ende, a <a href='https://t.me/LastHopePosting'>Last Hope</a>\n\n<u>Los comandos disponibles (por ahora) son</u>:\n/mostrar Si quiere SOLICITAR los CANALES de la Botonera e <b>Información</b> sobre la PRÓXIMA PUBLICACIÓN de esta en sus CANALES afiliados\n/ingresar Si quiere INGRESAR su CANAL EN la BOTONERA\n/start Para mostrar ESTE mensaje de ayuda\n\n<u>Nota:</u>\nSi quiere notificar algo o tiene alguna duda consulte con mi creador y guapetón propietario de Last Hope ( ͡° ͜ʖ ͡°)\n\n👉<a href='https://t.me/mistakedelalaif'>Reima</a>👈", parse_mode="html", disable_web_page_preview=True)




@bot.message_handler(commands=["ingresar"])
def cmd_ingresar(message, usuario=usuario, archivo_canales=archivo_canales):
    archivo_canales.seek(0)
    msg=bot.send_message(message.chat.id, f"A continuación:\nUne este bot ({usuario.username}) a tu canal y dale permisos de administración para que pueda publicar mensajes y continuar tu inserción a la botonera\n\nCuando lo hagas, escribe el nombre de usuario de tu canal (@username) aquí\n\n<u>Ejemplo:</u>\n@LastHopePosting", parse_mode="html")
    bot.register_next_step_handler(msg, recibir_grupo)

def recibir_grupo(message, archivo_canales=archivo_canales):
    if not message.text.startswith("@"):
        msg=bot.send_message(message.chat.id, "Recuerda que debe de ser el <b>@username</b> del canal\n<u>Ejemplo:</u>\n@LastHopePosting", parse_mode="html")
        bot.register_next_step_handler(msg, recibir_grupo)
    else:
        bot.send_message(message.chat.id, "A continuación probaré si el <b>@username</b> es correcto y tengo derechos administrativos...", parse_mode="html")
        try:
            bot.get_chat(message.text)
            bot.send_message(message.chat.id, "Muy bien, el chat existe, veamos si tengo permisos administrativos...")
            chat_id=bot.get_chat(message.text).id
            miembro=bot.get_chat_member(chat_id, usuario.id)
        except:
            markup=ForceReply()
            msg=bot.send_message(message.chat.id, "Al parecer el canal/grupo que ingresaste no es correcto, ya que NO existe tigre\n\nVuelve a mirar si el <b>@username</b> es correcto y cópialo aquí a continuación\nSi estás ABSOLUTAMENTE seguro de que es correcto, por favor contacte con el hermoso 👉<a href='https://t.me/mistakedelalaif'>Reima</a>👈", parse_mode="html", disable_web_page_preview=True, reply_markup=markup)
            bot.register_next_step_handler(msg, recibir_grupo)
        else:
            if miembro.status=="administrator":
                for i in archivo_canales:
                    if i == str(chat_id):
                        return bot.send_message(message.chat.id, "Ese canal que ingresaste ya está en la botonera Velociraptor\nNo te hagas el listo >:D Vuelve a escribir /ingresar y pueba con otro canal")
                                        
                with open("canales.txt", "w") as archivo:
                    archivo.write(str(chat_id))
                bot.send_message(message.chat.id, "PERFECTO! 🤩\n\nEl registro está completo mastodonte, añadiré tu canal a la botonera (❁´◡`❁).\n<u>Nota:</u>\nRecuerda que NO PUEDES quitar al bot de la administración o tu canal será ELIMINADO de la botonera", parse_mode="html")
                bot.send_message(message.chat.id, "Para ver tu canal en la botonera ingresa el comando /mostrar y verás como se hace la magia ;)")
            else:
                msg=bot.send_message(message.chat.id, ">:V AÚN NO ES ADMIN MMGUEVO\n\nHaz admin al bot y continuaremos el procedimiento\nnPor favor, ingrese nuevamente el <b>@username</b> del grupo/canal\n\nY ASEGÚRATE DE QUE ESTA VEZ SI SEA ADMIN (¬_¬ )", parse_mode="html", reply_markup=markup)
                bot.register_next_step_handler(msg, recibir_grupo)







@bot.message_handler(commands=["mostrar"])
def cmd_mostrar(message, archivo_canales=archivo_canales, foto=foto_LastBotonera, tiempo_de_espera=tiempo_de_espera_botonera, hora_publicacion=hora_publicacion):
    bot.send_chat_action(message.chat.id, action="upload_photo")
    botonera=InlineKeyboardMarkup(row_width=1)
    #Primeramente, tengo que asegurarme que el bot tenga permisos para publicar en el canal
    lista_canales=archivo_canales.readlines()
    
    
    def buscar_administracion(archivo_canales=archivo_canales):
        for e,canal in enumerate(lista_canales,start=0):
            member=bot.get_chat_member(chat_id=canal, user_id=bot.user.id)
            if not member.status=="administrator":
                del lista_canales[e]
                archivo_canales.seek(0)
                archivo_canales.writelines(lista_canales)
                archivo_canales.truncate()
                bot.send_message(1413725506, f"Se ha eliminado el canal {bot.get_chat(canal).username} por no dejarme como administrador >:(")
                archivo_canales.seek(0)
                buscar_administracion(archivo_canales)
    buscar_administracion()
    for canal in lista_canales:
        #Si el bot tiene permisos pues agrega el canal a la botonera
        nombre=bot.get_chat(canal).title
        enlace=f"https://t.me/{bot.get_chat(canal).username}"
        boton=InlineKeyboardButton(nombre, url=enlace)
        botonera.add(boton)
    bot.send_photo(message.chat.id, foto, caption="¡Si!, ¡Es eso mismo que estás pensando!\n Literalmente, <b>La Última Botonera</b> baby (☞ﾟヮﾟ)☞ ☜(ﾟヮﾟ☜)\n\n¡Oye Juan! ¿Quién hizo ese logo? ¡Quiero tatuarme eso en el c*lo!", parse_mode="html" , reply_markup=botonera)
    if hora_publicacion==[]:
        return bot.send_message(message.chat.id, "Ahora mismo, no estoy publicando la botonera, quizás en un momento sí lo haré\n\nPero todo depende del baboso de <a href='https://t.me/mistakedelalaif'>Reima</a>, no de mí :(", parse_mode="html", disable_web_page_preview=True)
    else:
        hora=time.localtime(hora_publicacion[0]+tiempo_de_espera).tm_hour
        minutos=time.localtime(hora_publicacion[0]+tiempo_de_espera).tm_min
        if hora>12:
            hora=hora-12
            hora_completa=f"{hora}:{minutos} pm"
        else:
            hora_completa=hora, ":", minutos, " am"
        if len(str(minutos))==1:
                minutos=f"0{minutos}"
        bot.send_message(message.chat.id, f"<u>Aviso</u>:\nLa botonera se publicará nuevamente a las {hora_completa}", parse_mode="html")
        archivo_canales.seek(0)
        foto.seek(0)
    

@bot.message_handler(commands=['id'])
def start(message):
    bot_id = bot.user.id
    bot.reply_to(message, f"El ID del bot es: {bot_id}")



@bot.message_handler(commands=["promo"])
def start(message):
    markup=InlineKeyboardMarkup(row_width=3)
    b1=InlineKeyboardButton("🌚Únete🌝", url="http://t.me/lasthopeposting")
    b2=InlineKeyboardButton("✨Pxp✨", url="http://t.me/mistakedelalaif")
    b3=InlineKeyboardButton("🔥Grupo🔥", url="http://t.me/lasthopepost")
    markup.add(b1,b2,b3)
    mensaje="<b>¡HOLA ZORRA!</b> 😈\n\nCansad@ de ir por canales sin ver a uno que robe los Memes/Shitpost de otros canales?🥵\nCansad@ de conversaciones completamente normales sin nada que haga sangrar tus ojos?\nCansad@de que nadie entienda tus parloteos intelectuales? 🧠\nCansado de leer esto como un comercial?🌞🍷\n\n¡No te preocupes! ¡LA SOLUCIÓN acaba de LLEGAR! \nSólo únete a:\n\n<a href='http://t.me/lasthopeposting'>¡LAST HOPE!</a>\n\nPara sentir el VERDADERO salseo en esas nalgas negras😳\n\nTambién tenemos chat <s>hot con mujerzuelas</s>  😳\n\n<u>Atentamente</u>:\nTu mamá en tanga ❤️"
    archivo=open("D:\\Last_Hope.jpg", "rb")
    bot.send_photo(message.chat.id, archivo, caption=mensaje, parse_mode="html", reply_markup=markup)


@bot.message_handler(func=lambda x: True)
def mensajes_al_chat(message):
    bot.send_message(message.chat.id, "Ingresa uno de los comandos disponibles en el bot, chacal\n\nA continuación, escribe /start para mostrar mis comandos de uso\n\nNo harás nada si no escribes nada (¬_¬ )")
    return
    
bot.infinity_polling()