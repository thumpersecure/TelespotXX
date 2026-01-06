"""
Pattern extraction and analysis module
Extracts names, emails, addresses, usernames, social profiles from text
"""

import re
from typing import Dict, List, Set, Tuple
from collections import Counter
import json


class PatternAnalyzer:
    """Analyzes text to extract useful OSINT patterns"""

    def __init__(self):
        # Common name patterns
        self.name_prefixes = ['mr', 'mrs', 'ms', 'miss', 'dr', 'prof']
        self.name_suffixes = ['jr', 'sr', 'ii', 'iii', 'iv', 'phd', 'md', 'esq']

        # Social media platforms
        self.social_platforms = {
            'facebook': [r'facebook\.com/([a-zA-Z0-9_.]+)', r'fb\.com/([a-zA-Z0-9_.]+)'],
            'twitter': [r'twitter\.com/([a-zA-Z0-9_]+)', r'x\.com/([a-zA-Z0-9_]+)'],
            'instagram': [r'instagram\.com/([a-zA-Z0-9_.]+)'],
            'linkedin': [r'linkedin\.com/in/([a-zA-Z0-9_-]+)'],
            'tiktok': [r'tiktok\.com/@([a-zA-Z0-9_.]+)'],
            'youtube': [r'youtube\.com/(?:user|channel|c)/([a-zA-Z0-9_-]+)'],
            'pinterest': [r'pinterest\.com/([a-zA-Z0-9_]+)'],
            'reddit': [r'reddit\.com/u(?:ser)?/([a-zA-Z0-9_-]+)'],
            'snapchat': [r'snapchat\.com/add/([a-zA-Z0-9_.]+)'],
            'github': [r'github\.com/([a-zA-Z0-9_-]+)'],
            'telegram': [r't\.me/([a-zA-Z0-9_]+)'],
        }

        # US States for address parsing
        self.us_states = {
            'alabama': 'AL', 'alaska': 'AK', 'arizona': 'AZ', 'arkansas': 'AR',
            'california': 'CA', 'colorado': 'CO', 'connecticut': 'CT', 'delaware': 'DE',
            'florida': 'FL', 'georgia': 'GA', 'hawaii': 'HI', 'idaho': 'ID',
            'illinois': 'IL', 'indiana': 'IN', 'iowa': 'IA', 'kansas': 'KS',
            'kentucky': 'KY', 'louisiana': 'LA', 'maine': 'ME', 'maryland': 'MD',
            'massachusetts': 'MA', 'michigan': 'MI', 'minnesota': 'MN', 'mississippi': 'MS',
            'missouri': 'MO', 'montana': 'MT', 'nebraska': 'NE', 'nevada': 'NV',
            'new hampshire': 'NH', 'new jersey': 'NJ', 'new mexico': 'NM', 'new york': 'NY',
            'north carolina': 'NC', 'north dakota': 'ND', 'ohio': 'OH', 'oklahoma': 'OK',
            'oregon': 'OR', 'pennsylvania': 'PA', 'rhode island': 'RI', 'south carolina': 'SC',
            'south dakota': 'SD', 'tennessee': 'TN', 'texas': 'TX', 'utah': 'UT',
            'vermont': 'VT', 'virginia': 'VA', 'washington': 'WA', 'west virginia': 'WV',
            'wisconsin': 'WI', 'wyoming': 'WY', 'district of columbia': 'DC'
        }
        self.state_abbrevs = set(self.us_states.values())

    def extract_names(self, text: str) -> List[Dict]:
        """Extract potential names from text"""
        names = []
        seen = set()

        # Pattern 1: Capitalized word pairs (First Last)
        pattern1 = r'\b([A-Z][a-z]+)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b'
        for match in re.finditer(pattern1, text):
            full_name = match.group(0).strip()
            if self._is_valid_name(full_name) and full_name.lower() not in seen:
                seen.add(full_name.lower())
                names.append({
                    'value': full_name,
                    'source': 'pattern_match',
                    'confidence': self._calculate_name_confidence(full_name, text)
                })

        # Pattern 2: "Owner: Name" or "Name: Value" patterns
        pattern2 = r'(?:owner|name|caller|registered to|belongs to)[:\s]+([A-Z][a-z]+\s+[A-Z][a-z]+)'
        for match in re.finditer(pattern2, text, re.IGNORECASE):
            full_name = match.group(1).strip()
            if self._is_valid_name(full_name) and full_name.lower() not in seen:
                seen.add(full_name.lower())
                names.append({
                    'value': full_name,
                    'source': 'labeled_match',
                    'confidence': min(90, self._calculate_name_confidence(full_name, text) + 20)
                })

        # Sort by confidence
        names.sort(key=lambda x: x['confidence'], reverse=True)
        return names[:20]  # Limit results

    def _is_valid_name(self, name: str) -> bool:
        """Check if a string is likely a valid name"""
        words = name.split()
        if len(words) < 2 or len(words) > 4:
            return False

        # Filter out common false positives
        invalid_words = {
            'phone', 'number', 'search', 'lookup', 'reverse', 'caller', 'owner',
            'address', 'email', 'click', 'here', 'view', 'more', 'free', 'premium',
            'results', 'found', 'report', 'united', 'states', 'america', 'street',
            'avenue', 'road', 'drive', 'lane', 'court', 'january', 'february',
            'march', 'april', 'may', 'june', 'july', 'august', 'september',
            'october', 'november', 'december', 'monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday', 'privacy', 'policy',
            'terms', 'service', 'contact', 'about', 'home', 'page'
        }

        for word in words:
            if word.lower() in invalid_words:
                return False
            if len(word) < 2:
                return False
            if not word[0].isupper():
                return False

        return True

    def _calculate_name_confidence(self, name: str, text: str) -> int:
        """Calculate confidence score for a name"""
        confidence = 50

        # Count occurrences
        count = text.lower().count(name.lower())
        confidence += min(count * 5, 20)

        # Check for context clues
        context_clues = ['owner', 'registered', 'belongs', 'name', 'caller']
        name_lower = name.lower()
        text_lower = text.lower()

        for clue in context_clues:
            # Check if clue appears near the name
            idx = text_lower.find(name_lower)
            if idx != -1:
                context = text_lower[max(0, idx-50):idx+len(name)+50]
                if clue in context:
                    confidence += 10

        return min(confidence, 95)

    def extract_emails(self, text: str) -> List[Dict]:
        """Extract email addresses from text"""
        emails = []
        seen = set()

        # Standard email pattern
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        for match in re.finditer(pattern, text):
            email = match.group(0).lower()
            if email not in seen and self._is_valid_email(email):
                seen.add(email)
                emails.append({
                    'value': email,
                    'source': 'pattern_match',
                    'confidence': self._calculate_email_confidence(email, text),
                    'domain': email.split('@')[1] if '@' in email else ''
                })

        emails.sort(key=lambda x: x['confidence'], reverse=True)
        return emails[:10]

    def _is_valid_email(self, email: str) -> bool:
        """Validate email format"""
        # Filter out obvious false positives
        invalid_domains = ['example.com', 'test.com', 'email.com', 'domain.com']
        domain = email.split('@')[1] if '@' in email else ''

        if domain in invalid_domains:
            return False

        if len(email) < 6 or len(email) > 254:
            return False

        return True

    def _calculate_email_confidence(self, email: str, text: str) -> int:
        """Calculate confidence score for email"""
        confidence = 60

        # Check for personal domain vs generic
        personal_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com', 'aol.com']
        domain = email.split('@')[1] if '@' in email else ''

        if domain in personal_domains:
            confidence += 10

        # Count occurrences
        count = text.lower().count(email.lower())
        confidence += min(count * 5, 15)

        return min(confidence, 90)

    def extract_addresses(self, text: str) -> List[Dict]:
        """Extract physical addresses from text"""
        addresses = []
        seen = set()

        # US address pattern
        # Matches: 123 Main St, City, ST 12345
        pattern = r'\b(\d+\s+[A-Za-z0-9\s]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd|Court|Ct|Way|Place|Pl|Circle|Cir)\.?)[,\s]+([A-Za-z\s]+)[,\s]+([A-Z]{2})\s*(\d{5}(?:-\d{4})?)\b'

        for match in re.finditer(pattern, text, re.IGNORECASE):
            street = match.group(1).strip()
            city = match.group(2).strip()
            state = match.group(3).upper()
            zip_code = match.group(4)

            full_address = f"{street}, {city}, {state} {zip_code}"
            addr_key = full_address.lower()

            if addr_key not in seen and state in self.state_abbrevs:
                seen.add(addr_key)
                addresses.append({
                    'value': full_address,
                    'street': street,
                    'city': city,
                    'state': state,
                    'zip': zip_code,
                    'source': 'pattern_match',
                    'confidence': 75
                })

        # Simpler pattern for partial addresses
        pattern2 = r'\b([A-Za-z\s]+)[,\s]+([A-Z]{2})\s*(\d{5})\b'
        for match in re.finditer(pattern2, text):
            city = match.group(1).strip()
            state = match.group(2).upper()
            zip_code = match.group(3)

            if len(city) > 2 and state in self.state_abbrevs:
                partial = f"{city}, {state} {zip_code}"
                if partial.lower() not in seen:
                    seen.add(partial.lower())
                    addresses.append({
                        'value': partial,
                        'city': city,
                        'state': state,
                        'zip': zip_code,
                        'source': 'partial_match',
                        'confidence': 55
                    })

        addresses.sort(key=lambda x: x['confidence'], reverse=True)
        return addresses[:10]

    def extract_usernames(self, text: str) -> List[Dict]:
        """Extract potential usernames from text"""
        usernames = []
        seen = set()

        # Pattern for @username mentions
        pattern1 = r'@([A-Za-z0-9_]{3,20})'
        for match in re.finditer(pattern1, text):
            username = match.group(1)
            if username.lower() not in seen:
                seen.add(username.lower())
                usernames.append({
                    'value': f'@{username}',
                    'username': username,
                    'source': 'mention',
                    'confidence': 70
                })

        # Pattern for "username: value" format
        pattern2 = r'(?:username|user|handle|screen name)[:\s]+([A-Za-z0-9_]{3,20})'
        for match in re.finditer(pattern2, text, re.IGNORECASE):
            username = match.group(1)
            if username.lower() not in seen:
                seen.add(username.lower())
                usernames.append({
                    'value': username,
                    'username': username,
                    'source': 'labeled',
                    'confidence': 80
                })

        usernames.sort(key=lambda x: x['confidence'], reverse=True)
        return usernames[:15]

    def extract_phone_numbers(self, text: str, exclude_phone: str = '') -> List[Dict]:
        """Extract phone numbers from text, excluding the search number"""
        phones = []
        seen = set()
        exclude_digits = re.sub(r'[^\d]', '', exclude_phone)

        # Various phone patterns
        patterns = [
            r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b',
            r'\b([0-9]{10})\b',
            r'\b([0-9]{3})[-.]([0-9]{3})[-.]([0-9]{4})\b',
        ]

        for pattern in patterns:
            for match in re.finditer(pattern, text):
                groups = match.groups()
                digits = ''.join(groups)
                digits = re.sub(r'[^\d]', '', digits)

                # Skip if it's the search number
                if digits == exclude_digits or digits == exclude_digits[-10:]:
                    continue

                if len(digits) == 10 and digits not in seen:
                    seen.add(digits)
                    formatted = f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
                    phones.append({
                        'value': formatted,
                        'digits': digits,
                        'source': 'pattern_match',
                        'confidence': 65,
                        'relationship': 'associated'
                    })

        phones.sort(key=lambda x: x['confidence'], reverse=True)
        return phones[:10]

    def extract_social_profiles(self, text: str) -> List[Dict]:
        """Extract social media profile URLs"""
        profiles = []
        seen = set()

        for platform, patterns in self.social_platforms.items():
            for pattern in patterns:
                for match in re.finditer(pattern, text, re.IGNORECASE):
                    username = match.group(1)
                    url = match.group(0)
                    key = f"{platform}:{username.lower()}"

                    if key not in seen:
                        seen.add(key)
                        profiles.append({
                            'platform': platform,
                            'username': username,
                            'url': url if url.startswith('http') else f'https://{url}',
                            'source': 'url_match',
                            'confidence': 85
                        })

        profiles.sort(key=lambda x: x['confidence'], reverse=True)
        return profiles[:20]

    def extract_ages(self, text: str) -> List[Dict]:
        """Extract age information"""
        ages = []
        seen = set()

        patterns = [
            r'(?:age|aged?)[:\s]+(\d{1,3})',
            r'(\d{1,3})\s*(?:years?\s*old|yo|y\.o\.)',
            r'born\s+(?:in\s+)?(\d{4})',
        ]

        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                value = match.group(1)
                if value.isdigit():
                    num = int(value)
                    if 1900 <= num <= 2010:  # Birth year
                        age = 2025 - num
                        if 18 <= age <= 100 and age not in seen:
                            seen.add(age)
                            ages.append({
                                'value': age,
                                'source': 'birth_year',
                                'confidence': 70
                            })
                    elif 18 <= num <= 100:  # Direct age
                        if num not in seen:
                            seen.add(num)
                            ages.append({
                                'value': num,
                                'source': 'direct',
                                'confidence': 75
                            })

        return ages[:5]

    def finalize_results(self, results: Dict) -> Dict:
        """Finalize and deduplicate results"""
        # Deduplicate names
        if 'patterns' in results and 'names' in results['patterns']:
            names = results['patterns']['names']
            unique_names = {}
            for name in names:
                key = name['value'].lower()
                if key not in unique_names or name['confidence'] > unique_names[key]['confidence']:
                    unique_names[key] = name
            results['patterns']['names'] = sorted(
                unique_names.values(),
                key=lambda x: x['confidence'],
                reverse=True
            )

        # Deduplicate emails
        if 'patterns' in results and 'emails' in results['patterns']:
            emails = results['patterns']['emails']
            unique_emails = {}
            for email in emails:
                key = email['value'].lower()
                if key not in unique_emails:
                    unique_emails[key] = email
            results['patterns']['emails'] = list(unique_emails.values())

        # Deduplicate addresses
        if 'patterns' in results and 'addresses' in results['patterns']:
            addresses = results['patterns']['addresses']
            unique_addrs = {}
            for addr in addresses:
                key = addr['value'].lower()
                if key not in unique_addrs or addr['confidence'] > unique_addrs[key]['confidence']:
                    unique_addrs[key] = addr
            results['patterns']['addresses'] = sorted(
                unique_addrs.values(),
                key=lambda x: x['confidence'],
                reverse=True
            )

        # Calculate overall summary
        results['summary'] = {
            'total_names': len(results['patterns'].get('names', [])),
            'total_emails': len(results['patterns'].get('emails', [])),
            'total_addresses': len(results['patterns'].get('addresses', [])),
            'total_usernames': len(results['patterns'].get('usernames', [])),
            'total_social_profiles': len(results['patterns'].get('social_profiles', [])),
            'total_associated_phones': len(results['patterns'].get('associated_phones', [])),
            'search_engine_results': len(results.get('search_engines', [])),
            'people_search_results': len(results.get('people_search', []))
        }

        return results
