#!/usr/bin/env python

import pandas as pd
import numpy as np
import Image
import ImageDraw
import ImageFont

def black_or_white(val):
  val = np.array(val)
  black = np.array([0,0,0])
  white = np.array([255,255,255])
  dist_black = np.linalg.norm(val-black)
  dist_white = np.linalg.norm(val-white)
  if dist_black < dist_white:
    return tuple(black)
  else:
    return tuple(white)

def transform_bw(img):
  #  cast image to either black or white
  new_img = [ black_or_white(val)  for val in img.getdata()]
  img.putdata(new_img)
  img.save("img/a_test.png")

def load_data():
  data = pd.read_csv('bac2012.csv', sep='|', header=0,
      names = ['name', 'county', 'pos', 'unit', 'retry', 'type', 'special',
        'ro1', 'ro2', 'oblig', 'oblig1', 'oblig2',
        'choice', 'choice1', 'choice2', 'avg', 'admitted'])
  admit = data[data['admitted'] >0]
  print len(admit)
  admit_county = data[['county', 'admitted']]
  grouped = admit_county.groupby('county')
  county_percents = grouped.aggregate(np.average)
  county_percents = county_percents.sort('admitted')
  print county_percents
  harta_jud = Image.open('img/harta_bw3.png')
  #transform_bw(harta_jud)
  #harta_jud = harta_jud.convert('1')
  county_pos = {
    'ab' : (140, 130),
    'ag' : (210, 210),
    'ar' : (100, 130),
    'b' : (273, 243), # + if
    'bc' : (300, 140),
    'bh' : (100, 100),
    'bn' : (200, 60),
    'br' : (340, 200),
    'bt' : (300, 20),
    'bv' : (230, 160),
    'bz' : (300, 220),
    'cj' : (170, 100),
    'cl' : (330, 270),
    'cs' : (90, 200),
    'ct' : (380, 260),
    'cv' : (270, 170),
    'db' : (240, 220),
    'dj' : (160, 260),
    'gj' : (150, 210),
    'gl' : (350, 160),
    'gr' : (260, 270),
    'hd' : (120, 160),
    'hr' : (240, 100),
    'il' : (340, 240),
    'is' : (300, 70),
    'mh' : (110, 230),
    'mm' : (200, 40),
    'ms' : (220, 100),
    'nt' : (280, 80),
    'ot' : (200, 260),
    'ph' : (260, 200),
    'sb' : (190, 150),
    'sj' : (150, 70),
    'sm' : (140, 30),
    'sv' : (250, 40),
    'tl' : (410, 220),
    'tm' : (70, 170),
    'tr' : (230, 270),
    'vl' : (180, 200),
    'vn' : (300, 160),
    'vs' : (340, 110)
  }
  print float(county_percents.loc['ab'])
  percent_min =  float(county_percents.iloc[0])
  percent_max = float(county_percents.iloc[-1])
  percent_delta = percent_max-percent_min
  draw = ImageDraw.Draw(harta_jud)
  font = ImageFont.truetype("/Library/Fonts/Georgia.ttf",12)
  for k,v in county_pos.items():
    (x,y) = v
    alpha = county_percents.loc[k]
    ImageDraw.floodfill(harta_jud, (x,y), (int((1-alpha)*255), int(alpha*255), 0))
    draw.text((x,y), k, (0, 0, 0), font=font)
  harta_jud.save("img/a_test.png")



def main():
  load_data()

if __name__=='__main__':
  main()
