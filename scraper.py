import requests 

from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

def get_html_doc(url):
    r = requests.get(url)
    return r.text

def scrape_languages():
    html_doc = get_html_doc('https://www.tiobe.com/tiobe-index/')

    soup = BeautifulSoup(html_doc, 'html.parser')

    table = soup.find("table", class_="table table-striped table-top20", id="top20")

    languages = []

    for row in table.find_all("tr")[1:5]:
        columns = row.find_all("td")
        lang_name = columns[4].text.strip()

        img_tag = columns[3].find('img')
    
        if img_tag:
            image_url = f"https://www.tiobe.com{img_tag['src']}"
            
            image_response = requests.get(image_url)
            with open(f"img/{lang_name}.png", "wb") as f:
                f.write(image_response.content)

        languages.append(columns[4].text.strip())

    return languages

def get_languages_informations(languages):
    langs_info = dict()
    for language in languages:


        query = f"{language} Wikipedia"
        results = DDGS().text(query)
        wiki_url = results[0]["href"]

        wiki_html_doc = get_html_doc(wiki_url)

        soup = BeautifulSoup(wiki_html_doc, "html.parser")
        paragraphs = soup.select("p")

        langs_info[language] = {
            "lang": language,
            "website": wiki_url,
            "paragraphs": []
        }


        for i in range(1, min(len(paragraphs), 5)):
            langs_info[language]["paragraphs"].append(
                paragraphs[i].get_text())

    return langs_info

def save_as_markdown(langs_info):
    markdown_text = f"# Popular Programing Languages\n\n"
    markdown_text += "This is a list of most populat programing languages according to TIOBE index :). \n\n"
    markdown_text += "I hope you find your favorite one :))). \n\n"
    idx = 1
    for key, lang_info in langs_info.items():
        markdown_text += f"### **[{idx}. {key}]({key}.md)** "
        markdown_text += f"![Language Icon](img/{key}.png)\n\n"
        markdown_text += f"### **[original website]({lang_info['website']})**\n\n"
        markdown_text += f"---\n"

        subsite_text = f"# {key} \n\n"

        for paragraph in lang_info["paragraphs"]:
            subsite_text += f"{paragraph} \n\n"

        subsite_text += f"[main list](popular_languages.md)"

        with open(f"{key}.md", 'w') as file:
            file.write(subsite_text)

        idx += 1

    with open("popular_languages.md", 'w') as file:
        file.write(markdown_text)


if __name__ == "__main__":
    languages = scrape_languages()

    langs_info = get_languages_informations(languages)

    save_as_markdown(langs_info)



