from bs4 import BeautifulSoup
from requests import get

def get_soup(html):
    return BeautifulSoup(html, 'html.parser')

if __name__ == '__main__':
    # URL: https://www.torontomu.ca/calendar/2024-2025/programs/science/computer_sci/#!accordion-1595938857886-full-time--four-year-program
    html = get('https://www.torontomu.ca/calendar/2024-2025/programs/science/computer_sci/#!accordion-1595938857886-full-time--four-year-program').text
 
    soup = get_soup(html)  
    # Get Element with class name resTwoColEven
    print(soup.find(class_='resTwoColEven').prettify())