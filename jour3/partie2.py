import re
from bs4 import BeautifulSoup

def create_bs_obj(file_path: str) -> BeautifulSoup:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        print(f"File content loaded from {file_path}")
        return BeautifulSoup(content, 'html.parser')
    except Exception as e:
        print(f"Error in create_bs_obj: {e}")
        raise

def find_title(file_path: str) -> str:
    soup = create_bs_obj(file_path)
    title = soup.title
    print(f"Title found: {title}")
    return title

def find_paragraphs(file_path: str) -> list[str]:
    soup = create_bs_obj(file_path)
    paragraphs = soup.find_all('p')
    print(f"Paragraphs found: {len(paragraphs)}")
    return [str(paragraph) for paragraph in paragraphs]

def find_links(file_path: str) -> list[str]:
    soup = create_bs_obj(file_path)
    links = soup.find_all('a')
    print(f"Links found: {len(links)}")
    return [link.get('href', '') for link in links]

def find_elements_with_css_class(file_path: str, css_class: str) -> list[str]:
    soup = create_bs_obj(file_path)
    elements = soup.find_all(class_=css_class)
    print(f"Elements with class '{css_class}' found: {len(elements)}")
    return [str(element) for element in elements]

def find_headers(file_path: str) -> list[str]:
    soup = create_bs_obj(file_path)
    header_regex = re.compile(r'h[1-6]')
    headers = soup.find_all(header_regex)
    print(f"Headers found: {len(headers)}")
    return [header.get_text(strip=True) for header in headers]

def extract_table(file_path: str) -> list[dict]:
    soup = create_bs_obj(file_path)
    table = soup.find('table')
    if not table:
        print("No table found")
        return []
    table_data = []
    for row in table.find_all('tr')[1:]:
        columns = row.find_all('td')
        if len(columns) == 3:
            fruit_info = {
                'name': columns[0].get_text().strip(),
                'color': columns[1].get_text().strip(),
                'price': float(columns[2].get_text().strip().replace('$', '').replace(',', ''))
            }
            table_data.append(fruit_info)
    print(f"Table data extracted: {table_data}")
    return table_data

# Test de la fonction
file_path = 'example.html'

print("Title:", find_title(file_path))
print("Paragraphs:", find_paragraphs(file_path))
print("Links:", find_links(file_path))
print("Elements with CSS class 'example':", find_elements_with_css_class(file_path, 'example'))
print("Headers:", find_headers(file_path))
print("Table data:", extract_table(file_path))