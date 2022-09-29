from PIL import Image, ImageDraw, ImageFont

# Cargar imagen de base
base = Image.open('imgbase.png').convert('RGBA')
# Crear capa para superponer
txt = Image.new('RGBA', base.size, (255,255,255,0))
# Definir fuente
fnt = ImageFont.truetype('terminal.ttf',20)

d = ImageDraw.Draw(txt)
# Dibujar texto con transparencia
d.text((10,10),"Yeison quiroga", font=fnt, fill=(0,0,0))
# Dibujar texto sin transparencia
# d.text((10,60),"Yeison quiroga", font=fnt, fill=(255,255,255,255))
# Superponer
out = Image.alpha_composite(base,txt)
#mostrar
out.show()
# Guardar
out.save("new.png")
