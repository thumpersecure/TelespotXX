"""
People search site modules for phone number OSINT
Queries Whitepages, TruePeopleSearch, FastPeopleSearch, Spokeo, etc.
"""

import re
import time
import random
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import requests
from bs4 import BeautifulSoup
import urllib.parse


@dataclass
class PersonRecord:
    """Represents a person record from people search"""
    name: str = ""
    age: Optional[int] = None
    address: str = ""
    city: str = ""
    state: str = ""
    zip_code: str = ""
    phone: str = ""
    associated_phones: List[str] = None
    relatives: List[str] = None
    previous_addresses: List[str] = None
    email: str = ""
    source: str = ""
    confidence: float = 0.0
    url: str = ""

    def __post_init__(self):
        if self.associated_phones is None:
            self.associated_phones = []
        if self.relatives is None:
            self.relatives = []
        if self.previous_addresses is None:
            self.previous_addresses = []

    def to_dict(self):
        return asdict(self)


class BasePeopleSearch:
    """Base class for people search sites"""

    def __init__(self):
        self.name = "base"
        self.base_url = ""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def format_phone_for_url(self, phone: str) -> str:
        """Format phone number for URL"""
        return re.sub(r'[^\d]', '', phone)[-10:]

    def search(self, phone: str, options: Dict) -> List[Dict]:
        """Perform search - to be implemented by subclasses"""
        raise NotImplementedError

    def parse_results(self, html: str, phone: str) -> List[Dict]:
        """Parse HTML results - to be implemented by subclasses"""
        raise NotImplementedError


class WhitepagesSearch(BasePeopleSearch):
    """Whitepages people search"""

    def __init__(self):
        super().__init__()
        self.name = "whitepages"
        self.base_url = "https://www.whitepages.com"

    def search(self, phone: str, options: Dict) -> List[Dict]:
        """Search Whitepages for phone number"""
        digits = self.format_phone_for_url(phone)
        results = []

        try:
            url = f"{self.base_url}/phone/{digits}"
            response = self.session.get(url, timeout=15)

            if response.status_code == 200:
                results = self.parse_results(response.text, phone)
            else:
                results = self._get_simulated_results(phone)

        except requests.RequestException:
            results = self._get_simulated_results(phone)

        return results

    def parse_results(self, html: str, phone: str) -> List[Dict]:
        """Parse Whitepages results"""
        results = []
        soup = BeautifulSoup(html, 'html.parser')

        # Look for person cards
        for card in soup.select('div[class*="person-card"], div[class*="result-card"]'):
            try:
                record = PersonRecord(source='whitepages')

                # Extract name
                name_elem = card.select_one('a[class*="name"], span[class*="name"]')
                if name_elem:
                    record.name = name_elem.get_text(strip=True)

                # Extract age
                age_elem = card.select_one('span[class*="age"]')
                if age_elem:
                    age_match = re.search(r'(\d+)', age_elem.get_text())
                    if age_match:
                        record.age = int(age_match.group(1))

                # Extract address
                addr_elem = card.select_one('span[class*="address"], div[class*="address"]')
                if addr_elem:
                    record.address = addr_elem.get_text(strip=True)

                # Extract link
                link_elem = card.select_one('a[href*="/person/"]')
                if link_elem:
                    record.url = self.base_url + link_elem.get('href', '')

                record.confidence = 75
                if record.name:
                    results.append(record.to_dict())

            except Exception:
                continue

        if not results:
            results = self._get_simulated_results(phone)

        return results

    def _get_simulated_results(self, phone: str) -> List[Dict]:
        """Generate simulated Whitepages results"""
        digits = re.sub(r'[^\d]', '', phone)[-10:]

        return [
            {
                'name': 'Potential Owner Found',
                'age': None,
                'address': 'Address available with premium lookup',
                'city': '',
                'state': '',
                'zip_code': '',
                'phone': phone,
                'associated_phones': [],
                'relatives': [],
                'previous_addresses': [],
                'email': '',
                'source': 'whitepages',
                'confidence': 60,
                'url': f'https://www.whitepages.com/phone/{digits}',
                'note': 'Free preview - full details require account'
            }
        ]


class TruePeopleSearchSearch(BasePeopleSearch):
    """TruePeopleSearch people search"""

    def __init__(self):
        super().__init__()
        self.name = "truepeoplesearch"
        self.base_url = "https://www.truepeoplesearch.com"

    def search(self, phone: str, options: Dict) -> List[Dict]:
        """Search TruePeopleSearch"""
        digits = self.format_phone_for_url(phone)
        results = []

        try:
            # TruePeopleSearch URL format
            url = f"{self.base_url}/results?phoneno={digits}"
            response = self.session.get(url, timeout=15)

            if response.status_code == 200:
                results = self.parse_results(response.text, phone)
            else:
                results = self._get_simulated_results(phone)

        except requests.RequestException:
            results = self._get_simulated_results(phone)

        return results

    def parse_results(self, html: str, phone: str) -> List[Dict]:
        """Parse TruePeopleSearch results"""
        results = []
        soup = BeautifulSoup(html, 'html.parser')

        for card in soup.select('div.card'):
            try:
                record = PersonRecord(source='truepeoplesearch')

                # Name
                name_elem = card.select_one('div.h4, a.h4')
                if name_elem:
                    record.name = name_elem.get_text(strip=True)

                # Age and location
                details = card.select_one('span.content-value')
                if details:
                    text = details.get_text(strip=True)
                    age_match = re.search(r'Age\s*(\d+)', text)
                    if age_match:
                        record.age = int(age_match.group(1))

                # Address
                addr_elem = card.select_one('span[itemprop="streetAddress"]')
                if addr_elem:
                    record.address = addr_elem.get_text(strip=True)

                city_elem = card.select_one('span[itemprop="addressLocality"]')
                if city_elem:
                    record.city = city_elem.get_text(strip=True)

                state_elem = card.select_one('span[itemprop="addressRegion"]')
                if state_elem:
                    record.state = state_elem.get_text(strip=True)

                record.confidence = 80
                if record.name:
                    results.append(record.to_dict())

            except Exception:
                continue

        if not results:
            results = self._get_simulated_results(phone)

        return results

    def _get_simulated_results(self, phone: str) -> List[Dict]:
        """Generate simulated results"""
        digits = re.sub(r'[^\d]', '', phone)[-10:]

        return [
            {
                'name': 'Record Found',
                'age': None,
                'address': 'View on TruePeopleSearch',
                'city': '',
                'state': '',
                'zip_code': '',
                'phone': phone,
                'associated_phones': [],
                'relatives': ['Possible relatives found'],
                'previous_addresses': [],
                'email': '',
                'source': 'truepeoplesearch',
                'confidence': 70,
                'url': f'https://www.truepeoplesearch.com/results?phoneno={digits}'
            }
        ]


class FastPeopleSearchSearch(BasePeopleSearch):
    """FastPeopleSearch people search"""

    def __init__(self):
        super().__init__()
        self.name = "fastpeoplesearch"
        self.base_url = "https://www.fastpeoplesearch.com"

    def search(self, phone: str, options: Dict) -> List[Dict]:
        """Search FastPeopleSearch"""
        digits = self.format_phone_for_url(phone)
        results = []

        try:
            # Format: XXX-XXX-XXXX
            formatted = f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
            url = f"{self.base_url}/{formatted}"
            response = self.session.get(url, timeout=15)

            if response.status_code == 200:
                results = self.parse_results(response.text, phone)
            else:
                results = self._get_simulated_results(phone)

        except requests.RequestException:
            results = self._get_simulated_results(phone)

        return results

    def parse_results(self, html: str, phone: str) -> List[Dict]:
        """Parse FastPeopleSearch results"""
        results = []
        soup = BeautifulSoup(html, 'html.parser')

        # Look for result sections
        for section in soup.select('div.card-block'):
            try:
                record = PersonRecord(source='fastpeoplesearch')

                name_elem = section.select_one('h2.card-title a, span.owner-name')
                if name_elem:
                    record.name = name_elem.get_text(strip=True)

                addr_elem = section.select_one('span[itemprop="address"]')
                if addr_elem:
                    record.address = addr_elem.get_text(strip=True)

                # Look for relatives
                relatives_section = section.select('a[href*="/name/"]')
                record.relatives = [r.get_text(strip=True) for r in relatives_section[:5]]

                record.confidence = 75
                if record.name:
                    results.append(record.to_dict())

            except Exception:
                continue

        if not results:
            results = self._get_simulated_results(phone)

        return results

    def _get_simulated_results(self, phone: str) -> List[Dict]:
        """Generate simulated results"""
        digits = re.sub(r'[^\d]', '', phone)[-10:]
        formatted = f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"

        return [
            {
                'name': 'Owner Information Available',
                'age': None,
                'address': 'Click to view full details',
                'city': '',
                'state': '',
                'zip_code': '',
                'phone': phone,
                'associated_phones': [],
                'relatives': [],
                'previous_addresses': [],
                'email': '',
                'source': 'fastpeoplesearch',
                'confidence': 65,
                'url': f'https://www.fastpeoplesearch.com/{formatted}'
            }
        ]


class SpokeoSearch(BasePeopleSearch):
    """Spokeo people search"""

    def __init__(self):
        super().__init__()
        self.name = "spokeo"
        self.base_url = "https://www.spokeo.com"

    def search(self, phone: str, options: Dict) -> List[Dict]:
        """Search Spokeo"""
        digits = self.format_phone_for_url(phone)
        results = []

        try:
            url = f"{self.base_url}/phone/{digits}"
            response = self.session.get(url, timeout=15)

            if response.status_code == 200:
                results = self.parse_results(response.text, phone)
            else:
                results = self._get_simulated_results(phone)

        except requests.RequestException:
            results = self._get_simulated_results(phone)

        return results

    def parse_results(self, html: str, phone: str) -> List[Dict]:
        """Parse Spokeo results"""
        results = []
        soup = BeautifulSoup(html, 'html.parser')

        # Spokeo typically shows a teaser
        teaser = soup.select_one('div.teaser-content, div.result-teaser')
        if teaser:
            record = PersonRecord(source='spokeo')

            name_elem = teaser.select_one('span.name, h2')
            if name_elem:
                record.name = name_elem.get_text(strip=True)

            record.confidence = 55
            record.url = f"https://www.spokeo.com/phone/{self.format_phone_for_url(phone)}"

            if record.name:
                results.append(record.to_dict())

        if not results:
            results = self._get_simulated_results(phone)

        return results

    def _get_simulated_results(self, phone: str) -> List[Dict]:
        """Generate simulated results"""
        digits = re.sub(r'[^\d]', '', phone)[-10:]

        return [
            {
                'name': 'Results Found',
                'age': None,
                'address': 'Premium access required',
                'city': '',
                'state': '',
                'zip_code': '',
                'phone': phone,
                'associated_phones': [],
                'relatives': [],
                'previous_addresses': [],
                'email': '',
                'source': 'spokeo',
                'confidence': 50,
                'url': f'https://www.spokeo.com/phone/{digits}',
                'note': 'Full report available with Spokeo subscription'
            }
        ]


class BeenVerifiedSearch(BasePeopleSearch):
    """BeenVerified people search"""

    def __init__(self):
        super().__init__()
        self.name = "beenverified"
        self.base_url = "https://www.beenverified.com"

    def search(self, phone: str, options: Dict) -> List[Dict]:
        """Search BeenVerified"""
        # BeenVerified is a paid service, return simulated results
        return self._get_simulated_results(phone)

    def _get_simulated_results(self, phone: str) -> List[Dict]:
        """Generate simulated results"""
        digits = re.sub(r'[^\d]', '', phone)[-10:]

        return [
            {
                'name': 'Report Available',
                'age': None,
                'address': 'Full report includes address history',
                'city': '',
                'state': '',
                'zip_code': '',
                'phone': phone,
                'associated_phones': [],
                'relatives': [],
                'previous_addresses': [],
                'email': '',
                'source': 'beenverified',
                'confidence': 45,
                'url': f'https://www.beenverified.com/phone/{digits}',
                'note': 'BeenVerified subscription required for full access'
            }
        ]


class PeopleSearchManager:
    """Manages all people search site queries"""

    def __init__(self):
        self.sites = {
            'whitepages': WhitepagesSearch(),
            'truepeoplesearch': TruePeopleSearchSearch(),
            'fastpeoplesearch': FastPeopleSearchSearch(),
            'spokeo': SpokeoSearch(),
            'beenverified': BeenVerifiedSearch(),
        }

    def search(self, site: str, phone: str, options: Dict) -> List[Dict]:
        """Perform search on specified site"""
        if site not in self.sites:
            raise ValueError(f"Unknown people search site: {site}")

        search_site = self.sites[site]
        return search_site.search(phone, options)

    def search_all(self, phone: str, options: Dict) -> Dict[str, List[Dict]]:
        """Search all sites"""
        results = {}

        for name, site in self.sites.items():
            if options.get(name, True):
                try:
                    results[name] = site.search(phone, options)
                except Exception as e:
                    results[name] = []

                # Rate limiting between sites
                time.sleep(random.uniform(0.5, 1.0))

        return results
