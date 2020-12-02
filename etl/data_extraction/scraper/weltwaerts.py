import re

from data_extraction.Scraper import Scraper


class WeltwaertsScraper(Scraper):
    """Scrapes the website weltwaerts.de."""

    base_url = 'https://www.weltwaerts.de'
    debug = True

    def parse(self, response, url):
        """Handles the soupified response of a detail page in the predefined way and returns it"""

        param_box = response.find('div', {'class': 'parameter__box'})

        content = response.find('div', {'class': 'mod_epdetail__content-container'})
        contact = content.find('h2', text='Ansprechpartner*in und Entsendeorganisation').findNext('div')

        google_map = response.find('a', {'class': 'mod_epdetail__link-map'})
        lat = None
        lon = None

        # Scrape longitude and latitude, if available
        if google_map:
            try:
                result = re.findall(r'q=(-?\d+\.\d+),(-?\d+\.\d+)', google_map['href'])
                lat = float(result[0][0])
                lon = float(result[0][1])
            except (IndexError, TypeError, ValueError):
                pass

        parsed_object = {
            'title': param_box.find("h1").decode_contents().strip() or None,
            'categories': ['International'],
            'location': param_box.find('li').find('span', {'class': 'parameter__value'}).decode_contents().strip() or None,
            'task': content.find('h2', text='Deine Aufgabe').findNext('div').decode_contents().strip() or None,
            'target_group': None,
            'timing': param_box.find('li').findNext('li').findNext('li').find('span', {'class': 'parameter__value'}).decode_contents().strip() or None,
            'effort': None,
            'opportunities': None,
            'organization': content.find('h2', text='Die Aufnahmeorganisation vor Ort').findNext('div').p.decode_contents().strip() or None,
            'contact': contact.decode_contents().strip() or None,
            'link': url or None,
            'source': self.base_url,
            'geo_location': {
                'lat': lat,
                'lon': lon,
            } if lat and lon else None, # If longitude and latitude are None, geo_location is set to None
            'languages': param_box.find('li').findNext('li').find('span', {'class': 'parameter__value'}).decode_contents().strip() or None,
            'requirements': content.find('h2', text='Anforderungen an dich').findNext('div').p.decode_contents().strip() or None,
        }

        contact_split = self.__extract_contact_data(parsed_object['contact'])

        parsed_object['post_struct'] = {
            'title': parsed_object['title'],
            'categories': parsed_object['categories'],
            'location': {
                'country': parsed_object['location'].split(', ')[-1] or None,
                'zipcode': None,
                'city': None,
                'street': None,
            },
            'task': re.sub(r'</?p>', '', parsed_object['task']).strip(),
            'target_group': None,
            'timing': parsed_object['timing'],
            'effort': None,
            'opportunities': None,
            'organization': {
                'name': parsed_object['organization'],
                'zipcode': None,
                'city': None,
                'street': None,
                'phone': None,
                'email': None,
            },
            'contact': {
                'name':  contact_split[0].strip() or None,
                'zipcode': contact_split[2][:5].strip() or None,
                'city': contact_split[2][5:].strip() or None,
                'street':  contact_split[1].strip() or None,
                'phone': None,
                # Extract the e-mail address, if available
                'email': contact.find('a', href=re.compile("mailto:.*"))['href'].replace('mailto:', '').strip() or None,
            },
            'link': parsed_object['link'],
            'source': parsed_object['source'],
            'geo_location': parsed_object['geo_location'],
            'languages': parsed_object['languages'],
            'requirements': parsed_object['requirements'],
        }

        return parsed_object

    def add_urls(self):
        """Adds all URLs of detail pages, found on the search pages, for the crawl function to scrape"""

        import time

        search_page_url = f'{self.base_url}/de/ep-ergebnis.html'
        next_page_url = search_page_url

        index = 1
        while next_page_url:

            response = self.soupify_post(next_page_url, {
                'ep-sortfilter': 1,
                'ep-numperpage': 50,
                'ep-sortorder': 'alpha'
            })

            # Get tags of individual results
            detail_link_tags = [x.find('a') for x in response.find_all('h3', {'class': 'result__headline'})]

            # Get maximum number of pages
            index_max = response.find('div', {'class': 'result__pagination'}).nav.p.decode_contents().strip()
            index_max = index_max.split(" von ", 1)[1]

            if self.debug:
                print(f'Fetched {len(detail_link_tags)} URLs from {next_page_url} [{index}/{index_max}]')

            # Iterate links and add, if not already found
            for link_tag in detail_link_tags:
                current_link = self.base_url + '/' + link_tag['href']
                if current_link in self.urls:
                    self.add_error({
                        'func': 'add_urls',
                        'body': {
                            'page_index': index,
                            'search_page': next_page_url,
                            'duplicate_link': current_link,
                            'duplicate_index': self.urls.index(current_link)
                        }
                    })
                else:
                    self.urls.append(current_link)

            # Get next result page
            next_page_url = response.find('li', {'class': 'next'}).find('a', {'class': 'next'})
            if next_page_url:
                next_page_url = self.base_url + '/' + next_page_url['href']

            index += 1

            time.sleep(self.delay)

    def __extract_contact_data(self, contact_raw):
        """Extracts the contact data"""

        # Removing HTML-Tags
        contact_raw = re.sub(r'<br/?>', '\n', contact_raw)
        contact_raw = Scraper.clean_html_tags(contact_raw)

        contact_split = list(filter(lambda s: 'E-mail' not in s, filter(None, contact_raw.split('\n'))))

        # If the contact data contains additional information, it is combined into a string
        if len(contact_split) > 3:
            names_split = contact_split[:(len(contact_split)-2)]
            names_raw = ', '.join(names_split)
            contact_split = [names_raw, contact_split[-2], contact_split[-1]]

        return contact_split
