import requests
from bs4 import BeautifulSoup
import spacy
from spacy.matcher import PhraseMatcher

url_to_scrape = 'https://foodviva.com/curry-recipes/aloo-matar-curry/'

response = requests.get(url_to_scrape)
soup = BeautifulSoup(response.content, 'html.parser')

ingredients_section = soup.find('div', id='css_fv_recipe_table')
ingredients_table = ingredients_section.find('table')

ingredients = [row.get_text(strip=True) for row in ingredients_table.find_all('tr') if row.get_text(strip=True)]

for ingredient in ingredients:
    print("- " + ingredient)

directions_section = soup.find('div', id='css_fv_recipe_method')
directions_list = directions_section.find_all('li')

directions = [direction.get_text(strip=True) for direction in directions_list]

print("\nDirections:")
for i, direction in enumerate(directions, start=1):
    print(str(i) + ". " + direction)

nlp = spacy.load('en_core_web_sm')

food_entities = ['aloo', 'matar', 'peas', 'potatoes', 'tomato', 'mustard', 'seeds', 'cumin', 'coriander',
                            'powder', 'chilli', 'turmeric', 'leaves', 'water', 'haldi', 'dhania',
                            'jeera', 'coriander', 'mirch', 'salt', 'curry', 'gravy']

matcher = PhraseMatcher(nlp.vocab)
patterns = [nlp.make_doc(entity.lower()) for entity in food_entities]
matcher.add('FOOD_ENTITIES', None, *patterns)

text = ' '.join(ingredients) + ' ' + ' '.join(directions)

doc = nlp(text)

food_words = []
for match_id, start, end in matcher(doc):
    food_words.append(doc[start:end].text)

non_food_words = [token.text for token in doc if token.text.lower() not in [word.lower() for word in food_words]]

print("\nFood Words:")
for word in food_words:
    print("- " + word)

print("\nNon-Food Words:")
for word in non_food_words:
    print("- " + word)
