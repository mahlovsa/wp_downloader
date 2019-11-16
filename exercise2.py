import requests
from requests.exceptions import RequestException
import sys
import os
from bs4 import BeautifulSoup

print('Welcome to Wallpaper Downloader v0.00019 alpha. \n')

#  it possible to set parameters from cmd
if len(sys.argv) == 4:
    wantedMonth = sys.argv[1]
    wantedYear = sys.argv[2]
    wantedResolution = sys.argv[3]
#  if  it does not - set it manually
else:
    try:
        #  handle any problems with given paramaters
        wantedMonth, wantedYear, wantedResolution = input('Please, enter the month, year and resolution: ').split(' ')
        print(wantedMonth, wantedYear, wantedResolution)
        if wantedResolution is None or wantedMonth is None or wantedYear is None:
            raise ValueError

    except ValueError:
        print('Sorry, but you gave incorrect parameters.\n'
              'Please, try to enter your request in this notation:\n'
              '[month] [year] [resolution]. All values separated by spaces\n'
              'Example: may 2019 1024x768')
        sys.exit(0)
# handle the fact, that publication year in january is not the same
publicationYear = wantedYear
if wantedMonth == 'january':
    publicationYear = str(int(publicationYear) - 1)

url = 'https://www.smashingmagazine.com/'
months = {'january': '12',
          'february': '01',
          'march': '02',
          'april': '03',
          'may': '04',
          'june': '05',
          'july': '06',
          'august': '07',
          'september': '08',
          'october': '09',
          'november': '10',
          'december': '11'}


try:
    request_url = '{}/{}/{}/desktop-wallpaper-calendars-{}-{}/'.format(url,
                                                                       publicationYear,
                                                                       months[wantedMonth],
                                                                       wantedMonth,
                                                                       wantedYear)

    page = requests.get(request_url).text
except RequestException as e:
    #  handling request problems
    print('Sorry, something going wrong, and request with your parameters has failed.\n'
          'Please, try another parameters, or contact with developer for assistance\n')
    sys.exit(0)


def filter_download_links(tag):
    #  declaring conditions for .findAll method
    return tag.has_attr('href') and tag.has_attr('title')


print('Searching for images...')
# looking for picture links
soup = BeautifulSoup(page, features='html.parser').findAll(filter_download_links, string=wantedResolution)
# checking links presence in list
if len(soup) < 1:
    print('Sorry, i did not found any pictures')
    sys.exit(0)


for i in soup:
    # save images in current work directory, as it required in exercise
    print('Start loading...')
    # there are two versions of each picture- with calendar and without it. we download both
    filename = os.path.join(os.getcwd(), i.attrs['title'])
    with open('{}.jpg'.format(filename), 'wb') as file:
        file.write(requests.get(i.attrs['href']).content)
        print('{} successfully downloaded'.format(i.attrs['title']))
print('All files was download successfully')
