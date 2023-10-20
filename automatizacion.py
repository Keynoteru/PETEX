import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

# Datos ficticios de producción de pozos
datos_de_produccion = [
    {
        "pozo": "Pozo A",
        "fecha": "2023-10-01",
        "petroleo": 1000,  # Barriles de petróleo
        "gas": 500,       # Miles de pies cúbicos de gas
        "agua": 200       # Barriles de agua
    },
    {
        "pozo": "Pozo A",
        "fecha": "2023-10-02",
        "petroleo": 1100,
        "gas": 550,
        "agua": 220
    },
    {
        "pozo": "Pozo B",
        "fecha": "2023-10-01",
        "petroleo": 900,
        "gas": 450,
        "agua": 180
    },
    {
        "pozo": "Pozo B",
        "fecha": "2023-10-02",
        "petroleo": 950,
        "gas": 475,
        "agua": 190
    }
]

# Crear gráfico de producción
fig, ax = plt.subplots()
ax.plot([registro["fecha"] for registro in datos_de_produccion], [registro["petroleo"] for registro in datos_de_produccion], label='Petróleo')
ax.plot([registro["fecha"] for registro in datos_de_produccion], [registro["gas"] for registro in datos_de_produccion], label='Gas')
ax.plot([registro["fecha"] for registro in datos_de_produccion], [registro["agua"] for registro in datos_de_produccion], label='Agua')
ax.set_xlabel('Fecha')
ax.set_ylabel('Producción')
ax.set_title('Producción Diaria de Pozos')
ax.legend()

# Guardar gráfico como imagen
plt.savefig('produccion_diaria.png')

# Crear informe PDF
c = canvas.Canvas('informe_diario.pdf', pagesize=letter)
c.drawString(100, 750, "Informe de Producción Diaria")
c.drawImage('produccion_diaria.png', 100, 400, width=400, height=200)
c.showPage()
c.save()

# Envío de correo electrónico
from_email = "santiagorosalesgomez@gmail.com"
to_email = "expectra10yt@gmail.com"
subject = "Informe de Producción Diaria"
message = "Adjunto se encuentra el informe de producción diaria de los pozos."

msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = to_email
msg['Subject'] = subject
msg.attach(MIMEText(message, 'plain'))

with open("informe_diario.pdf", "rb") as file:
    attach = MIMEApplication(file.read(),_subtype="pdf")
    attach.add_header('Content-Disposition','attachment',filename=str("informe_diario.pdf"))
    msg.attach(attach)

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(from_email, "Mcklopedia48")
server.sendmail(from_email, to_email, msg.as_string())
server.quit()

# Eliminar archivos temporales
os.remove("produccion_diaria.png")
os.remove("informe_diario.pdf")
