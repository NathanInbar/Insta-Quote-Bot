from PIL import Image, ImageDraw, ImageFont, ImageOps
from colorthief import ColorThief
import requests
from io import BytesIO
import re, os, time
from instabot import Bot
import markovify

#example image from lorem picsum
#picsum = r"C:\Users\robot\Pictures\Saved Pictures\loremPicsum-1080x1080.jpg"

def main():

#uh-oh spaghettios D:
#meh who gives a fuck.
	if os.path.exists("images/gen.jpg"):
		os.remove("images/gen.jpg")
	if os.path.exists("images/gen.jpg.REMOVE_ME"):
		os.remove("images/gen.jpg.REMOVE_ME")
	if os.path.exists("images/temp.jpg"):
		os.remove("images/temp.jpg")

	quote = genQuote("texts/frankenstein.txt")#returns quote as string
	image = genImage(quote)#returns directory of generated image as string
	uploadImage(image)


def genQuote(txtFile):#quote generation

	with open(txtFile) as f:
		text = f.read()

		text_model = markovify.Text(text)
		text_model = text_model.compile()

		#LAZY LULW SUGMA NUTS
		quote="zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
		while len(quote) > 60: #max quote length is 60 chars
			quote = text_model.make_sentence()
		#---
		quote = quote.split()

		if(len(quote) > 5):#put a newline in the middle of the quote if there are more than 5 words
			quote.insert(int(len(quote)/2), "\n")

		q=""
		for word in quote:#join from list back to string
			q+= word + " "
		quote = q

		return quote

def genImage(quote):#image generation with text

	imgDir = "images/gen.jpg"
	tmpDir = "images/temp.jpg"

	url = r"https://picsum.photos/1080/1080/?blur" #gets an image via lorem picsum (has blur effect)
	response = requests.get(url)
	img = Image.open(BytesIO(response.content))
						#left, top, right, bottom
	quoteBounds = img.crop((0, 0, 1080, 724))#creates a copy of the image except cropped to be around the quote
	quoteBounds = ImageOps.invert(quoteBounds)
	quoteBounds.save(tmpDir)

	d = ImageDraw.Draw(img)#start drawing the image
	fnt = ImageFont.truetype('fonts/Stay Happy.ttf', 100)#set font


	color_thief = ColorThief(tmpDir)#gets the most dominant color in the image
	inv_dominant_color = color_thief.get_color(quality=1)

	#draw the quote on the image
	d.text((50,50), quote, fill=inv_dominant_color, font=fnt)

	#save the image, remove the temp file
	img.save(imgDir)
	#os.remove(tmpDir)
	return imgDir

def uploadImage(image, capt="Follow for more #SensibleQuotes"):#uploads to instagram

	bot = Bot()
	bot.login(username = "***************",
		  	  password = "***************")
	bot.upload_photo(image, caption = capt)

for x in range(10):
	main()
	time.sleep(30)
