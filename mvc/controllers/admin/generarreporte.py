import web
import app

render = web.template.render("mvc/views/admin/") #ruta de las vistas

class GenerarReporte: #clase Index
    def GET(self):
        return render.generar_reporte()