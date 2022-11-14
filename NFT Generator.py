#import random and pillow modules
import random
from PIL import Image
from openpyxl import load_workbook
#set the seed *DO NOT TOUCH*
random.seed(1)
#filename
Filename = 'Algofact #'
#excel document
workbook = load_workbook(filename="Algostats.xlsx")
sheet = workbook.active
#make folder
import os
mypath = "Generated"
if not os.path.isdir(mypath):
   os.makedirs(mypath)

def generateMatrix():
    #create canvas varialbe
    canvas = []
    filled = 0
    #set first layers of the image
    #7 bits to represent a 14x14 grid
    canvas.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    canvas.append([0,0,0,0,0,0,0])
    #working canvas 10 pixels downwards
    for x in range(10):
        #first 2 are always 0,0 to make a border
        temp = [0,0]
        #range 5 for working 5x10 area
        for y in range(5):
            #if the seeded random number is less than 0.5, place a 0
            if (random.random() <= 0.5):
                temp.append(0)
            #if the seeded random number is more than 0.5, place a 1
            else:
                temp.append(1)
                filled = filled + 1
        canvas.append(temp)
    #place bottom two layers of matrix as 0's
    canvas.append([0,0,0,0,0,0,0])
    canvas.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0])

    #place 2's next to the ones
    #check above and below every cell
    for x in range(1,13):
        for y in range(7):
            #check cells below and above
            if (canvas[x][y] == 0) & ((canvas[x+1][y] == 1) | (canvas[x-1][y] == 1)):
                canvas[x][y] = 2
            
    #check left and right of every cell
    for x in range(14):
        for y in range(1,7):
            if (canvas[x][y] == 0) & (canvas[x][y-1] == 1):
                canvas[x][y] = 2
        for y in range(6):
            if (canvas[x][y] == 0) & (canvas[x][y+1] == 1):
                canvas[x][y] = 2
    #flip image
    for x in range(1,13):
        canvas[x].append(canvas[x][6])
        canvas[x].append(canvas[x][5])
        canvas[x].append(canvas[x][4])
        canvas[x].append(canvas[x][3])
        canvas[x].append(canvas[x][2])
        canvas[x].append(canvas[x][1])
        canvas[x].append(canvas[x][0])
    #generate colours
    background = [round(random.random()*255),round(random.random()*255),round(random.random()*255)]
    fill = [round(random.random()*255),round(random.random()*255),round(random.random()*255)]
    outline = [round(random.random()*255),round(random.random()*255),round(random.random()*255)]
    return canvas, background, fill, outline, filled

#generate image function
def generateImage(params, name):
    #define variables
    canvas = params[0]
    background = params[1]
    fill = params[2]
    outline = params[3]
    numfilled = (params[4]*2)
    #generate hex values
    backgroundhex = '#%02x%02x%02x' % (background[0], background[1], background[2])
    fillhex = '#%02x%02x%02x' % (fill[0],fill[1],fill[2])
    outlinehex = '#%02x%02x%02x' % (outline[0],outline[1],outline[2])
    
    #create image
    im = Image.new('RGBA', (14,14))
    for x in range(14):
        for y in range(14):
            if (canvas[x][y] == 0):
                im.putpixel((y,x), (background[0],background[1],background[2]))
            if (canvas[x][y] == 1):
                im.putpixel((y,x), (fill[0],fill[1],fill[2]))
            if (canvas[x][y] == 2):
                im.putpixel((y,x), (outline[0],outline[1],outline[2]))
    img = im.resize((504,504), resample=Image.BOX)
    img.save(name + '.png')

    #save stats to excel document
    sheet['A'+(name[-5:])] = (name[10:])
    sheet['B'+(name[-5:])] = (backgroundhex)
    sheet['C'+(name[-5:])] = (fillhex)
    sheet['D'+(name[-5:])] = (outlinehex)
    sheet['E'+(name[-5:])] = (numfilled)
    
for i in range(5000):
    filenum = str(i+1)
    if (len(filenum) == 1):
        name = Filename + '0000' + filenum
    elif (len(filenum) == 2):
        name = Filename + '000' + filenum
    elif (len(filenum) == 3):
        name = Filename + '00' + filenum
    elif (len(filenum) == 4):
        name = Filename + '0' + filenum
    else:
        name = Filename + filenum
    generateImage(generateMatrix(),('Generated/'+name))
workbook.save(filename="Algostats.xlsx")
exit()
