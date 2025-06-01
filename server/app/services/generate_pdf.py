
import os
from io import BytesIO
from warnings import catch_warnings

from flask import make_response
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pathlib import Path

class PdfGenerator:
    
        def __init__(self):
            self._path = Path(__file__).parent.parent / 'assets' 
            self._loadPath = Path(__file__).parent.parent 
            
        @property
        def path(self):
            return self._path
    
        @path.setter
        def path(self, value):
            self._path = value
    
       

        def create_updates_pdf(self, participantes):
        
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=A4)
            
            alturaAtual = 0
            dataBasePath = os.path.join(self.path, 'images')

            if (len(participantes) > 3):
                for participante in participantes:

                    
                    nome = participante.name
                    codigo = participante.code  

                
                    c.setFont(psfontname="Courier", size=10)
                    c.drawString(x=30, y=800-alturaAtual, text=codigo +
                                "   " + nome + "   ", mode=2)
                    alturaAtual = alturaAtual + 15

                if (alturaAtual > 600):
                    c.showPage()
                    alturaAtual = 0
                alturaAtual += 15

            for participante in participantes:
                
                nome = participante.name
                codigo = participante.code

                c.setFont(psfontname="Courier", size=10)
                c.drawString(x=17, y=800-alturaAtual, text=codigo +
                            "   " + nome, mode=2)
                c.drawString(x=17, y=780 - alturaAtual,
                            text="peso:             altura:             escolaridade:             idade:                ", mode=2)
                c.drawImage(image= os.path.join(dataBasePath,'coisasQueGosto.png'),
                            x=0, y=570-alturaAtual, width=150, height=200)
                c.drawImage(image= os.path.join(dataBasePath,'domiciliares.png'),
                            x=125, y=570-alturaAtual, width=130, height=150)
                c.drawImage(image=os.path.join(dataBasePath,'materiasFavoritas.png'),
                            x=250, y=570-alturaAtual, width=130, height=150)
                c.drawImage(image= os.path.join(dataBasePath,'Favoritas.png'),
                            x=355, y=570-alturaAtual, width=130, height=125)

                alturaAtual = alturaAtual + 270
                if (alturaAtual >= 600):
                    alturaAtual = 0
                    c.showPage()

                # Salvando o PDF
            c.save()
            buffer.seek(0)
            return buffer


        def create_cdpr_pdf(self, cdprs):

            
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=A4)

            largura, altura = A4
            dataBasePath = os.path.join(self.path, 'cdpr_model')
           
            
            for cdpr in cdprs:

                nome = cdpr.name
                codigo = cdpr.code
                age = cdpr.age

                if age == "0-2":
                    c.drawImage(image= os.path.join(dataBasePath, '0-2.jpg'),
                                x=0, y=0, width=largura, height=altura, preserveAspectRatio=True)
                elif age == "3-5":
                    c.drawImage(image= os.path.join(dataBasePath, '3-5.jpg'),
                                x=0, y=0, width=largura, height=altura, preserveAspectRatio=True)
                elif age == "6-8":
                    c.drawImage(image= os.path.join(dataBasePath, '6-8.jpg'),
                                x=0, y=0, width=largura, height=altura, preserveAspectRatio=True)
                elif age == "9-11":
                    c.drawImage(image= os.path.join(dataBasePath, '9-11.jpg'),
                                x=0, y=0, width=largura, height=altura, preserveAspectRatio=True)
                elif age == "12-14":
                    c.drawImage(image= os.path.join(dataBasePath, '12-14.jpg'),
                                x=0, y=0, width=largura, height=altura, preserveAspectRatio=True)
                elif age == "15-18":
                    c.drawImage(image= os.path.join(dataBasePath, '15-18.jpg'),
                                x=0, y=0, width=largura, height=altura, preserveAspectRatio=True)
                elif age == "19":
                    c.drawImage(image= os.path.join(dataBasePath, '19.jpg'),
                                x=0, y=0, width=largura, height=altura, preserveAspectRatio=True)
                    
                c.setFont(psfontname="Courier", size=10)
                c.drawString(x=250, y=820, text=codigo + "   " + nome + "   ", mode=2)
                
                c.showPage()

            c.save()
            buffer.seek(0)

            return buffer

        def create_letters_pdf(type, letters):
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=A4)

            largura, altura = A4
       
            # elf._code = code
            # self._name = name
            # self._letterCode = letterCode
            # self._type = type
            # self._status = status

            alturaAtual = 0
            for letter in letters:

                nome = letter.name
                participant_code = letter.code  
                letter_code = letter.letterCode
                letter_type = letter.type
                status = letter.status 

                try:
                   questions = letter.questions
                except AttributeError:
                    questions = None
            
                if (questions is not None):
                    c.setFont(psfontname="Courier", size=6)
                    c.drawString(x=30, y=800-alturaAtual, text=letter_code + 
                                "   " + participant_code + "   " + nome + "   " + letter_type +"  "+ questions + "   " + status, mode=2)
                else:
                    c.setFont(psfontname="Courier", size=6)
                    c.drawString(x=30, y=800-alturaAtual, text=letter_code + 
                                "   " + participant_code + "   " + nome + "   " + letter_type + "   " + status, mode=2)


                alturaAtual = alturaAtual + 12

                if (alturaAtual > 750):
                    c.showPage()
                    alturaAtual = 0
                alturaAtual += 15
                        
                
            c.save()
            buffer.seek(0)

            return buffer

              