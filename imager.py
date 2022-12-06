from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math
import random
import csv
import os.path
import imageio


def create_lot(spots):
    height = numpixel(spots)
    img = Image.new( 'RGB', (500,height), "#403F3C") # Create a new black image
    pixels = img.load() # Create the pixel map
    for i in range(50, img.size[1], 50):
        for j in range(0, 75):
            pixels[j, i] = (247, 181, 0)
        for k in range(250, 400):
            pixels[k, i] = (247, 181, 0)
    for i in range(50, img.size[1]-50):
        pixels[325, i] = (247, 181, 0)
    filename = "./lots/lot" + str(spots) + ".png"
    img.save(filename)
    return img

def numpixel(spots):
    sets = math.ceil(spots/3)
    return 150 + (sets-1)*50

def create_map(spots, cars):
    sets = math.ceil(spots/3)
    parkmap = []
    for i in range(0, sets):
        parkmap.append([0, 0, 0])
    for z in range(0, cars):
        openspot = open_spot(parkmap, sets)
        spotx = openspot[0]
        spoty = openspot[1]
        carcol = random.randint(1, 5)
        parkmap[spotx][spoty] = carcol
    return parkmap

def create_empty(spots):
    sets = math.ceil(spots/3)
    parkmap = []
    for i in range(0, sets):
        parkmap.append([0, 0, 0])
    return parkmap

def open_spot(parkmap, sets):
    for i in range(0, sets):
        for j in range(0, 3):
            if parkmap[i][j] == 0:
                return int(i), int(j)

def add_cars(spots, parkmap, time, outputfolder):
    filename1 = "./lots/lot" + str(spots) + ".png"
    if os.path.exists(filename1) == False:
        create_lot(spots)
    lot = Image.open(filename1)
    lotimage = lot.copy()
    #lotimage = lotimage.convert("RGBA")
    for i in range(0, len(parkmap)):
        for j in range(0, 3):
            if parkmap[i][j] > 0:
                carimg = "./cars/" + str(parkmap[i][j]) + ".png"
                car = Image.open(carimg)
                #car = car.convert("RGBA")
                ypixels = int(i)*50+58
                xpixels = 5
                if int(j) == 1:
                    xpixels += 250
                if int(j) == 2:
                    xpixels += 325
                lotimage.paste(car, (xpixels, ypixels))

    I1 = ImageDraw.Draw(lotimage)
    myFont = ImageFont.truetype('./inter.ttf', 24)
    I1.text((10, 10), "Time = " + str(time) + ":00", font=myFont, fill=(255, 255, 255))
    lotimage.save('./' + str(outputfolder) + '/'+ str(time) + '.png')
    #lotimage.show()

def fix_image():
    for i in range(1, 6):
        filename = "./cars/" + str(i) + ".png"
        carimg = Image.open(filename)
        carimg = carimg.convert('RGBA')
        newImage = []
        for item in carimg.getdata():
            if item[:3] == (0, 0, 0):
                newImage.append((64, 63, 60, 0))
            else:
                newImage.append(item)
        carimg.putdata(newImage)
        carimg.save(filename)

def read_sheet(num_spots, inputfile, outputfolder):
    sets = math.ceil(num_spots/3)
    f = open(inputfile)
    reader = csv.reader(f)
    time = 0
    for row in reader:
        lot = create_empty(num_spots)
        for i, color in enumerate(row):
            outerindex = math.floor(int(i)/3)
            innerindex = int(i)%3
            lot[outerindex][innerindex] = int(color)
        add_cars(num_spots, lot, str(time), outputfolder)
        time+=1
        #print(row)

def create_gif(foldername, outputgif):
    filenames = []
    for i in range(0, 60):
        filenames.append('./'+foldername+'/'+str(i)+'.png')
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    imageio.mimsave(outputgif, images)

if __name__ == "__main__":
    #image = create_lot(25)
    #image.show()
    #parkmap = create_map(25, 14)
    #add_cars(25, parkmap)
    #fix_image()
    num_spots = 48
    inputfile = './inputsheets/d60c66s48.csv'
    outputfolder = 'testoutput'
    outputgif = './c60s48.gif'
    read_sheet(num_spots, inputfile, outputfolder)
    create_gif(outputfolder, outputgif)

