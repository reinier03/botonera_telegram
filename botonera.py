import telebot
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
from telebot.types import ForceReply
from telebot.types import ReplyKeyboardRemove
import threading
from time import sleep
import time
import os

bot=telebot.TeleBot("6685078171:AAErSR82jBZkpLfgFX4Y7nbEeZ6sYjs7AO8")

dic={}
hora_publicacion=[]
tiempo_de_espera_botonera=10800
ejecutar_hilo=True
try:
    foto_LastBotonera=open(f"{os.path.dirname(os.path.abspath(__file__))}/Last_Botonera.jpg", 'rb')
except:
    def recibir_foto_promo(message):
        @bot.message_handler(content_types="photo")
        def recibir_foto():
            file_name = message.document.file_name
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            try:
                foto_LastBotonera=open("Last_Botonera.jpg", 'wb')
            except:
                foto_LastBotonera=open(file_name, 'wb')
                foto_LastBotonera.write(downloaded_file)
                return foto_LastBotonera
            
    msg=bot.send_message(1413725506, "Al parecer, no hay foto de Last Botonera promo, envíame una para continuar")
    bot.register_next_step_handler(msg, recibir_foto_promo)

        
archivo_canales=open(f"{os.path.dirname(os.path.abspath(__file__))}/canales.txt", "r+")


#archivo_canales=open("D:\\Nueva Carpeta\\Programacion\\Proyectos Personales\\botonera_telegram\\canales.txt", "r+")


archivo_canales.seek(0)
lista_canales=archivo_canales.readlines()
if lista_canales==[]:
    archivo_canales.write("-1001161864648 | 1413725506\n")
archivo_canales.seek(0)



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
    dic_admin={}
    dic_admin[message.from_user.id]=[]
    if message.chat.id==1413725506:
        botonera_panel=InlineKeyboardMarkup(row_width=1)
        b1=InlineKeyboardButton("Iniciar bucle de publicaciones 🙌", callback_data="Iniciar bucle")
        b2=InlineKeyboardButton("Parar el bucle de publicaciones 🖐", callback_data="Parar bucle")
        b3=InlineKeyboardButton("Agregar un canal a la lista de canales 👀", callback_data="Agregar canal")
        b4=InlineKeyboardButton("Eliminar un canal de la lista de canales 💨", callback_data="Eliminar canal")
        b5=InlineKeyboardButton("Modificar el tiempo de la botonera ⌛", callback_data="Modificar tiempo")
        b6=InlineKeyboardButton("Ver Archivo de texto de canales 🧻", callback_data="Archivo de texto") 
        botonera_panel.add(b1,b2,b3,b4,b5,b6)


        bot.send_message(message.chat.id, "Bienvenido Reima ;) Qué planeas hacer?", reply_markup=botonera_panel)
        @bot.callback_query_handler(func=lambda x: True)
        def respuesta_callback(call, foto_LastBotonera=foto_LastBotonera, ejecutar_hilo=ejecutar_hilo):
            global archivo_canales
            archivo_canales.seek(0)
            foto_LastBotonera.seek(0)
            markup=ForceReply()
            if call.data=="Iniciar bucle":
                def hacer_publicaciones(ejecutar_hilo=ejecutar_hilo):
                    global hora_publicacion
                    while ejecutar_hilo:
                        archivo_canales.seek(0)
                        foto_LastBotonera.seek(0)
                        bot.send_message(1413725506, "Publicaré la botonera ahora")
                        botonera=InlineKeyboardMarkup(row_width=1)
                        #Primeramente, tengo que asegurarme que el bot tenga permisos para publicar en el canal
                        archivo_canales.seek(0)
                        archivo_canales.seek(0)
                        lista_canales_administracion=[]
                        lista_canales_eliminar=[]
                        archivo_canales.seek(0)
                        for linea in archivo_canales:
                            canal=linea.split("|")[0].strip()
                            administrador=linea.split("|")[1].strip()
                            member=bot.get_chat_member(chat_id=canal, user_id=bot.user.id)
                            if not member.status=='administrator' or str(administrador)!=str(1413725506):
                                lista_canales_eliminar.append(linea)
                                bot.send_message(1413725506, f"Se ha eliminado el canal {bot.get_chat(canal).username} por no dejarme como administrador >:(")
                                bot.send_message(administrador, f"<u>ATENCIÓN</u>:\n Se ha eliminado el canal {bot.get_chat(canal).username} por no dejarme como administrador >:(\n\nPara ingresar de nuevo el canal en la botonera escriba /ingresar", parse_mode="html")
                            else:
                                lista_canales_administracion.append(linea)
                        for i in lista_canales_administracion:
                            archivo_canales.seek(0)
                            archivo_canales.write(f"{str(i)}")
                            archivo_canales.truncate()
                            archivo_canales.seek(0)
                            
                        del lista_canales_eliminar
                        lista_canales=archivo_canales.readlines()
                        archivo_canales.seek(0)
                        for linea in lista_canales:
                            canal=int(linea.split("|")[0].strip())
                            #Si el bot tiene permisos pues agrega el canal a la botonera
                            nombre=bot.get_chat(canal).title
                            enlace=f"https://t.me/{bot.get_chat(canal).username}"
                            boton=InlineKeyboardButton(nombre, url=enlace)
                            botonera.add(boton)
                        botonera.add(InlineKeyboardButton("(☞ﾟヮﾟ)☞ ÚNETE ☜(ﾟヮﾟ☜)", url="https://t.me/LastBotoneraBot"))
                        for linea in lista_canales:
                            canal=int(linea.split("|")[0].strip())
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
                dic[message.from_user.id]=[]
                def registro_de_admin(message):
                    global archivo_canales
                    try:
                        chat=bot.get_chat(message.text)
                        dic_admin[message.from_user.id].append(chat)
                    except:
                        msg=bot.send_message(message.chat.id, "El canal que ingresaste no existe, vuelve a intentar\nIngresa un @username válido")
                        bot.register_next_step_handler(msg, registro_de_admin)
                    else:
                        for line in archivo_canales:
                            if str(dic_admin[message.from_user.id][0].id) in str(line.split("|")[0].strip()):
                                bot.send_message(message.chat.id, "El canal ya existe en el archivo\n\nPrueba con otro")
                                return bot.send_message(message.chat.id, "Bienvenido Reima ;) Qué planeas hacer?", reply_markup=botonera_panel)
                            
                        if bot.get_chat_member(dic_admin[message.from_user.id][0].id, bot.user.id).status!="administrator":
                            bot.send_message(message.chat.id, "No soy admin en ese chat, pero bueno, ya sabrás tú lo que haces....")
                        archivo_canales.seek(0)
                        archivo_canales.read()
                        archivo_canales.write(f"{str(dic_admin[message.from_user.id][0].id)} | {str(call.from_user.id)}\n")
                        archivo_canales.seek(0)
                        bot.send_message(message.chat.id, f"El canal {dic_admin[message.from_user.id][0].username} ha sido agregado exitosamente a la botonera")
                        return bot.send_message(message.chat.id, "Bienvenido Reima ;) Qué planeas hacer?", reply_markup=botonera_panel)

                bot.register_next_step_handler(msg, registro_de_admin)
                
            elif call.data=="Eliminar canal":
                msg=bot.send_message(message.chat.id, "Ahora escribe el @username del chat al que quieres eliminar", reply_markup=markup)
                
                def eliminacion_de_grupo_admin(message):
                    dic_admin[message.from_user.id]=[]
                    try:
                        chat_admin=bot.get_chat(message.text)
                    except:
                        msg=bot.send_message(message.chat.id, "El canal no existe o lo escribiste de forma incorrecta\nVuelve a escribirlo", reply_markup=markup)
                        bot.register_next_step_handler(msg, eliminacion_de_grupo_admin)
                    dic_admin[message.from_user.id].append(chat_admin)
                    canales_eliminar_admin=[]
                    canales_mantener_admin=[]
                    archivo_canales.seek(0)
                    archivo_canales.seek(0)
                    contador=0
                    for linea in archivo_canales:
                        if str(dic_admin[message.from_user.id][0].id) in linea.split("|")[0].strip():
                            contador+=1
                            canales_eliminar_admin=[linea.split("|")[0].strip()]
                        else:
                            canales_mantener_admin.append(linea)
                    if contador==0:
                        bot.send_message(message.chat.id, "Al parecer ese canal no estaba en la lista\nNo ha sido eliminado ningún canal")
                        return bot.send_message(message.chat.id, "Bienvenido Reima ;) Qué planeas hacer?", reply_markup=botonera_panel)
                    archivo_canales.seek(0)
                    for linea in canales_mantener_admin:
                        archivo_canales.write(f"{str(linea)}")
                    archivo_canales.truncate()
                    archivo_canales.seek(0)
                    bot.send_message(message.chat.id, f"Ha sido eliminado el canal de <b>{(dic_admin[message.from_user.id][0].title)}({dic_admin[message.from_user.id][0].username})</b> de la botonera", parse_mode="html")
                    return
            
                bot.register_next_step_handler(msg, eliminacion_de_grupo_admin)

                
            elif call.data=="Modificar tiempo":
                global tiempo_de_espera_botonera
                msg=bot.send_message(message.chat.id, "Cada cuánto tiempo planeas que la botonera se publique?\n\nIngresa el valor en minutos", reply_markup=markup)
                def tiempo_botonera(message):
                    if message.text.isdigit():
                        tiempo_de_espera_botonera=int(message.text)*60
                        bot.send_message(message.chat.id, f"La próxima vez que se enviará la botonera será a las {time.strftime('%H:%M', time.localtime(time.time()+tiempo_de_espera_botonera))}")
                        return tiempo_de_espera_botonera, bot.send_message(message.chat.id, "Bienvenido Reima ;) Qué planeas hacer?", reply_markup=botonera_panel)
                    else:
                        msg=bot.send_message(message.chat.id, "No has introducido correctamente un VALOR NÚMERICO en minutos para el tiempo de espera\nVuelve a intentarlo", reply_markup=markup)
                        bot.register_next_step_handler(msg, tiempo_botonera)

                bot.register_next_step_handler(msg, tiempo_botonera)
                
            elif call.data=="Archivo de texto":
                archivo_canales.seek(0)
                texto=""
                lineas=archivo_canales.readlines()
                for linea in lineas:
                    texto+=linea
                archivo_canales.seek(0)
                bot.send_message(message.chat.id, f"<u>El contenido del archivo es</u>:\n\n{texto}", parse_mode="html")
                return

    else:
        bot.send_message(message.chat.id, "Lo siento mirei ;)\n\nNo eres mi creador como para mandarme ese mensaje >:D y decirme qué hacer")
        return
        
            

@bot.message_handler(commands=["start"])
def cmd_start(message):
    markup=ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Hola! 😁, Bienvenido a <b>Last Botonera</b> bot.\nAquí se encuentran los canales afiliados a la botonera y por ende, a <a href='https://t.me/LastHopePosting'>Last Hope</a>\n\n<u>Los comandos disponibles (por ahora) son</u>:\n/mostrar Si quiere SOLICITAR los CANALES de la Botonera e <b>Información</b> sobre la PRÓXIMA PUBLICACIÓN de esta en sus CANALES afiliados\n/ingresar Si quiere INGRESAR su CANAL EN la BOTONERA\n/start Para mostrar ESTE mensaje de ayuda\n\n<u>Nota:</u>\nSi quiere notificar algo o tiene alguna duda consulte con mi creador y guapetón propietario de Last Hope ( ͡° ͜ʖ ͡°)\n\n👉<a href='https://t.me/mistakedelalaif'>Reima</a>👈", parse_mode="html", disable_web_page_preview=True, reply_markup=markup)




@bot.message_handler(commands=["ingresar"])
def cmd_ingresar(message, usuario=usuario, archivo_canales=archivo_canales, dic=dic):
    archivo_canales.seek(0)
    dic[message.from_user.id]=[]
    msg=bot.send_message(message.chat.id, f"A continuación:\nUne este bot ({usuario.username}) a tu canal y dale permisos de administración para que pueda publicar mensajes y continuar tu inserción a la botonera\n\nCuando lo hagas, escribe el nombre de usuario de tu canal (@username) aquí\n\n<u>Ejemplo:</u>\n@LastHopePosting", parse_mode="html")
    bot.register_next_step_handler(msg, recibir_grupo)

def recibir_grupo(message, archivo_canales=archivo_canales):
    if not message.text.startswith("@"):
        msg=bot.send_message(message.chat.id, "Recuerda que debe de ser el <b>@username</b> del canal\n<u>Ejemplo:</u>\n@LastHopePosting\n\n<u><b>Nota IMPORTANTE</u></b>:\nDebe de tener el @ delante del nombre o no lo reconoceré :)", parse_mode="html")
        bot.register_next_step_handler(msg, recibir_grupo)
    else:
        bot.send_message(message.chat.id, "A continuación probaré si el <b>@username</b> es correcto y tengo derechos administrativos...", parse_mode="html")
        try:
            chat_id=bot.get_chat(message.text).id
            dic[message.from_user.id].append(chat_id)
            miembro=bot.get_chat_member(chat_id, usuario.id)
            dic[message.from_user.id].append(miembro)
            dic[message.from_user.id].append(message.from_user.id)
        except:
            markup=ForceReply()
            msg=bot.send_message(message.chat.id, "Al parecer el canal/grupo que ingresaste no es correcto, ya que NO existe tigre\n\nVuelve a mirar si el <b>@username</b> es correcto y cópialo aquí a continuación\nSi estás ABSOLUTAMENTE seguro de que es correcto, por favor contacte con el hermoso 👉<a href='https://t.me/mistakedelalaif'>Reima</a>👈", parse_mode="html", disable_web_page_preview=True, reply_markup=markup)
            bot.register_next_step_handler(msg, recibir_grupo)
        else:
            if dic[message.from_user.id][1].status=="administrator":
                for i in archivo_canales:
                    canal=i.split("|")[0].strip()
                    if canal == str(dic[message.from_user.id][0]):
                        return bot.send_message(message.chat.id, "Ese canal que ingresaste ya está en la botonera Velociraptor\nNo te hagas el listo >:D Vuelve a escribir /ingresar y pueba con otro canal")
                archivo_canales.read()                 
                archivo_canales.write(f"{str(dic[message.from_user.id][0])} | {str(dic[message.from_user.id][2])}\n")
                bot.send_message(message.chat.id, "PERFECTO! 🤩\n\nEl registro está completo mastodonte, añadiré tu canal a la botonera e igualmente AÑADIRÉ tu nombre de usuario por si ocurre algún problema a futuro con el bot y notificarte (❁´◡`❁).\n<u>Nota:</u>\nRecuerda que NO PUEDES quitar al bot de la administración o tu canal será ELIMINADO de la botonera", parse_mode="html")
                bot.send_message(message.chat.id, "Para ver tu canal en la botonera ingresa el comando /mostrar y verás como se hace la magia ;)")
            else:
                msg=bot.send_message(message.chat.id, ">:V AÚN NO ES ADMIN MMGUEVO\n\nHaz admin al bot y continuaremos el procedimiento\nnPor favor, ingrese nuevamente el <b>@username</b> del grupo/canal\n\nY ASEGÚRATE DE QUE ESTA VEZ SI SEA ADMIN (¬_¬ )", parse_mode="html", reply_markup=markup)
                bot.register_next_step_handler(msg, recibir_grupo)





#-------------------Funcion MOSTRAR--------------------

@bot.message_handler(commands=["mostrar"])
def cmd_mostrar(message, archivo_canales=archivo_canales, foto=foto_LastBotonera, tiempo_de_espera=tiempo_de_espera_botonera, hora_publicacion=hora_publicacion):
    archivo_canales.seek(0)
    foto_LastBotonera.seek(0)
    bot.send_chat_action(message.chat.id, action="upload_photo")
    botonera=InlineKeyboardMarkup(row_width=1)
    #Primeramente, tengo que asegurarme que el bot tenga permisos para publicar en el canal
    lista_canales=archivo_canales.readlines()
    archivo_canales.seek(0)
    lista_canales_administracion=[]
    lista_canales_eliminar=[]
    for e,linea in enumerate(lista_canales,start=0):
        canal=int(linea.split("|")[0].strip())
        administrador=int(linea.split("|")[1].strip())
        member=bot.get_chat_member(chat_id=canal, user_id=bot.user.id)
        if not member.status=="administrator" or administrador!=1413725506:
            lista_canales_eliminar.append(lista_canales[e])
            bot.send_message(1413725506, f"Se ha eliminado el canal {bot.get_chat(canal).username} por no dejarme como administrador >:(")
            bot.send_message(administrador, f"<u>ATENCIÓN</u>:\n Se ha eliminado el canal {bot.get_chat(canal).username} por no dejarme como administrador >:(\n\nPara ingresar de nuevo el canal en la botonera escriba /ingresar", parse_mode="html")
        else:
            lista_canales_administracion.append(lista_canales[e])
    archivo_canales.seek(0)
    for i in lista_canales_administracion:
        archivo_canales.write(f"{str(i)}")
    del lista_canales_eliminar
    archivo_canales.truncate()
    archivo_canales.seek(0)
    lista_canales=archivo_canales.readlines()
    archivo_canales.seek(0)
    for linea in lista_canales:
        canal=int(linea.split("|")[0])
        #Si el bot tiene permisos pues agrega el canal a la botonera
        nombre=bot.get_chat(canal).title
        enlace=f"https://t.me/{bot.get_chat(canal).username}"
        boton=InlineKeyboardButton(nombre, url=enlace)
        botonera.add(boton)
    botonera.add(InlineKeyboardButton("(☞ﾟヮﾟ)☞ ÚNETE ☜(ﾟヮﾟ☜)", url="https://t.me/LastBotoneraBot"))
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
            hora_completa=f"{hora}:{minutos} am"
        if len(str(minutos))==1:
                minutos=f"0{minutos}"
        bot.send_message(message.chat.id, f"<u>Aviso</u>:\nLa botonera se publicará nuevamente a las {hora_completa}", parse_mode="html")
        archivo_canales.seek(0)
        foto.seek(0)
    

@bot.message_handler(commands=['id'])
def start(message):
    bot.reply_to(message, f"El ID del bot es: {bot.user.id}")
    bot.reply_to(message, f"El ID del Reima es: {message.from_user.id}")
    bot.reply_to(message, f"El ID de Last Hope es: {bot.get_chat('@LastHopePosting').id}")
    bot.reply_to(message, f"El ID del chat es: {message.chat.id}")



@bot.message_handler(commands=["promo"])
def start(message):
    markup=InlineKeyboardMarkup(row_width=3)
    b1=InlineKeyboardButton("🌚Únete🌝", url="http://t.me/lasthopeposting")
    b2=InlineKeyboardButton("✨Pxp✨", url="http://t.me/mistakedelalaif")
    b3=InlineKeyboardButton("🔥Grupo🔥", url="http://t.me/lasthopepost")
    markup.add(b1,b2,b3)
    mensaje="<b>¡HOLA ZORRA!</b> 😈\n\nCansad@ de ir por canales sin ver a uno que robe los Memes/Shitpost de otros canales?🥵\nCansad@ de conversaciones completamente normales sin nada que haga sangrar tus ojos?\nCansad@de que nadie entienda tus parloteos intelectuales? 🧠\nCansado de leer esto como un comercial?🌞🍷\n\n¡No te preocupes! ¡LA SOLUCIÓN acaba de LLEGAR! \nSólo únete a:\n\n<a href='http://t.me/lasthopeposting'>¡LAST HOPE!</a>\n\nPara sentir el VERDADERO salseo en esas nalgas negras😳\n\nTambién tenemos chat <s>hot con mujerzuelas</s>  😳\n\n<u>Atentamente</u>:\nTu mamá en tanga ❤️"
    archivo=open(f"{os.path.dirname(os.path.abspath(__file__))}Last_Hope.jpg", "rb")
    bot.send_photo(message.chat.id, archivo, caption=mensaje, parse_mode="html", reply_markup=markup)


@bot.message_handler(func=lambda x: True)
def mensajes_al_chat(message):
    bot.send_message(message.chat.id, "Ingresa uno de los comandos disponibles en el bot, chacal\n\nA continuación, escribe /start para mostrar mis comandos de uso\n\nNo harás nada si no escribes nada (¬_¬ )")
    return

def archivo_texto(archivo_canales=archivo_canales):
    archivo_canales.seek(0)

    texto=""
    lineas=archivo_canales.readlines()
    for linea in lineas:
        texto+=linea
    archivo_canales.seek(0)
    bot.send_message(1413725506, f"<u>El contenido del archivo es</u>:\n\n{texto}", parse_mode="html")

    
    
bot.infinity_polling()