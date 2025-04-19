from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def generate_pdf_service(titulo, dados, buffer): 
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    margin = 30
    y = height - margin

    p.setFillColor(colors.black)
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, y - 20, titulo)
    y -= 75

    p.setFillColor(colors.black)
    p.setFont("Helvetica-Bold", 12)
    headers = ["Código", "Participante", "Nome", "Tipo", "Estado"]
    col_widths = [60, 100, 160, 80, 60]
    x = margin

    for i, header in enumerate(headers):
        p.drawString(x, y, header)
        x += col_widths[i]
    y -= 15
    p.line(margin, y, width - margin, y)
    y -= 20

    p.setFont("Helvetica", 12)

    for pessoa in dados['pessoas']:
        x = margin
        valores = [
            str(pessoa['codigo']),
            str(pessoa['codigo_participante']),
            pessoa['nome'],
            pessoa['tipo'],
            pessoa['estado']
        ]
        for i, valor in enumerate(valores):
            p.drawString(x, y, valor)
            x += col_widths[i]
        y -= 15

        if y < 50:          
            p.showPage()
            y = height - margin
            p.setFont("Helvetica-Bold", 16)
            p.drawCentredString(width / 2, y - 20, titulo)
            y -= 70
            p.setFont("Helvetica-Bold", 12)
            x = margin

            for i, header in enumerate(headers):
                p.drawString(x, y, header)
                x += col_widths[i]
                
            y -= 15
            p.line(margin, y, width - margin, y)
            y -= 20
            p.setFont("Helvetica", 11)

    p.save()
    buffer.seek(0) 