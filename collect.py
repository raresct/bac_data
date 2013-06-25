#!/usr/bin/env python

from selenium import webdriver

def clean_var (var):
  if var is None:
   return None
  else:
    return var.strip().lower()

def collect(year):
  year = str(year)
  with open('out.txt', 'a') as f:
    header = ('Nume complet', 'Judet', 'Pozitie tara', 'Unitate invatamant', 'Promotie anterioara', # 4
        'Forma invatamant', 'Specializare', 'Nota Limba romana (1)', 'Nota Limba romana (2)', 'Disciplina obligatorie', # 9
        'Nota la disciplina obligatorie (1)', 'Nota la disciplina obligatorie (2)', 'Disciplina la alegere',
        'Nota la disciplina la alegere (1)', 'Nota la disciplina la alegere (2)', # 14
        'Media', 'Admis'
        )
    len_header = len(header)
    #f.write('|'.join(header)+'\n')

    # Read html filenames
    base_url = 'http://static.bacalaureat.edu.ro/'+year+'/rapoarte/rezultate/dupa_medie/'
    page_no = 20020
    driver = webdriver.Firefox()
    driver.implicitly_wait(10)

    while True:
      print page_no
      url = base_url+'page_{}.html'.format(page_no)
      driver.get(url)
      if '404' in driver.title:
        return

      # surround in try except until it can read
      table = driver.find_element_by_id('mainTable')

      rows =  table.text.split('\n')

      csv_row = [None for i in xrange(len_header)]


      for i in xrange(2, len(rows), 3): # first two rows are irrelevant, and we read three at a time
        row1 = clean_var(rows[i]).split('  ')
        row2 = clean_var(rows[i+1]).split('  ')
        row3 = clean_var(rows[i+2]).split('  ')

        csv_row[0] = row1[1]+' '+row2[0] # nume
        csv_row[1] = row2[2] # judet
        csv_row[2] = row1[0] # poz tara
        csv_row[3] = row2[1] # unit inv
        csv_row[4] = u'0' if row2[3]=='nu' else u'1' # prom ant
        csv_row[5] = row2[4] # forma_inv
        csv_row[6] = row2[5] # spec
        csv_row[7] = row2[7] # nota lb rom (1)
        csv_row[8] = row2[9] # nota lb rom (2)
        csv_row[9] = row2[13].strip() # disciplina obligatorie
        csv_row[12] = row2[14] # disc alegere
        csv_row[10] = row3[0] # nota disc oblig (1)
        csv_row[11] = row3[1] # nota disc oblig (2)
        csv_row[13] = row3[2] # nota disc alegere (1)
        csv_row[14] = row3[3] # nota disc alegere (2)
        csv_row[15] = row2[16] # media
        csv_row[16] = u'1' if row2[17]==u'reu\u015fit' else u'0' # admis

        f.write(('|'.join(csv_row)+'\n').encode('utf-8'))
      page_no += 1
    driver.close()
def main():
  collect(2012)

if __name__=='__main__':
  main()

