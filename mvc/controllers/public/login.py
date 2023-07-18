import web
import app
import json
import firebase_config as token
import pyrebase

render = web.template.render("mvc/views/public/")

class Login: #clase Index
    def GET (self): 
        try:  
            mensaje = None 
            return render.login(mensaje)
        except Exception as error: # error
            mensaje = None
            print("Error Login.GET: {}".format(error))
            return render.login(mensaje) 
        
    def POST(self): 
        try: 
            mensaje = None
            firebase = pyrebase.initialize_app(token.firebaseConfig) 
            auth = firebase.auth() 
            db = firebase.database()
            formulario = web.input() 
            email = formulario.email 
            password= formulario.password
            user = auth.sign_in_with_email_and_password(email, password) 
            local_id =  (user ['localId'])
            web.setcookie('localid', local_id)
            busqueda =  db.child("data").child("usuarios").child(user['localId']).get()
            if busqueda.val()['nivel'] == 'administrador':
                if busqueda.val()['status'] == "inactivo":  
                    return render.login(mensaje)
                else:
                    return web.seeother("/admin/lista-pozos")
            elif busqueda.val()['nivel'] == "operador":
                if busqueda.val()['status'] == "inactivo": 
                    return render.login(mensaje)
                else:
                    return web.seeother("/operador/lista-pozos")
            elif busqueda.val()['nivel'] == "informatica":
                    return web.seeother("/informatica/agregar-usuario")
                    
        except Exception as error: # Error en formato JSON
            formato = json.loads(error.args[1])
            error = formato['error'] 
            mensaje = error['mensaje']
            if mensaje == "invalid_password" :
                return render.login(mensaje) 
            print("Error login.POST: {}".format(mensaje)) 