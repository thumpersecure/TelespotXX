"""
Phone number parsing and utility functions
"""

import re
from typing import Dict, Optional, List


# Country codes and their info
COUNTRY_CODES = {
    '1': {'country': 'United States/Canada', 'format': '+1 (XXX) XXX-XXXX'},
    '7': {'country': 'Russia/Kazakhstan', 'format': '+7 XXX XXX-XX-XX'},
    '20': {'country': 'Egypt', 'format': '+20 XX XXXX XXXX'},
    '27': {'country': 'South Africa', 'format': '+27 XX XXX XXXX'},
    '30': {'country': 'Greece', 'format': '+30 XXX XXX XXXX'},
    '31': {'country': 'Netherlands', 'format': '+31 X XXXXXXXX'},
    '32': {'country': 'Belgium', 'format': '+32 XXX XX XX XX'},
    '33': {'country': 'France', 'format': '+33 X XX XX XX XX'},
    '34': {'country': 'Spain', 'format': '+34 XXX XXX XXX'},
    '36': {'country': 'Hungary', 'format': '+36 XX XXX XXXX'},
    '39': {'country': 'Italy', 'format': '+39 XXX XXX XXXX'},
    '40': {'country': 'Romania', 'format': '+40 XXX XXX XXX'},
    '41': {'country': 'Switzerland', 'format': '+41 XX XXX XX XX'},
    '43': {'country': 'Austria', 'format': '+43 X XXXXXXXX'},
    '44': {'country': 'United Kingdom', 'format': '+44 XXXX XXXXXX'},
    '45': {'country': 'Denmark', 'format': '+45 XX XX XX XX'},
    '46': {'country': 'Sweden', 'format': '+46 XX XXX XX XX'},
    '47': {'country': 'Norway', 'format': '+47 XXX XX XXX'},
    '48': {'country': 'Poland', 'format': '+48 XXX XXX XXX'},
    '49': {'country': 'Germany', 'format': '+49 XXX XXXXXXX'},
    '51': {'country': 'Peru', 'format': '+51 XXX XXX XXX'},
    '52': {'country': 'Mexico', 'format': '+52 XX XXXX XXXX'},
    '53': {'country': 'Cuba', 'format': '+53 X XXX XXXX'},
    '54': {'country': 'Argentina', 'format': '+54 XX XXXX XXXX'},
    '55': {'country': 'Brazil', 'format': '+55 XX XXXXX XXXX'},
    '56': {'country': 'Chile', 'format': '+56 X XXXX XXXX'},
    '57': {'country': 'Colombia', 'format': '+57 XXX XXX XXXX'},
    '58': {'country': 'Venezuela', 'format': '+58 XXX XXX XXXX'},
    '60': {'country': 'Malaysia', 'format': '+60 XX XXX XXXX'},
    '61': {'country': 'Australia', 'format': '+61 X XXXX XXXX'},
    '62': {'country': 'Indonesia', 'format': '+62 XXX XXXX XXXX'},
    '63': {'country': 'Philippines', 'format': '+63 XXX XXX XXXX'},
    '64': {'country': 'New Zealand', 'format': '+64 XX XXX XXXX'},
    '65': {'country': 'Singapore', 'format': '+65 XXXX XXXX'},
    '66': {'country': 'Thailand', 'format': '+66 XX XXX XXXX'},
    '81': {'country': 'Japan', 'format': '+81 XX XXXX XXXX'},
    '82': {'country': 'South Korea', 'format': '+82 XX XXXX XXXX'},
    '84': {'country': 'Vietnam', 'format': '+84 XXX XXX XXX'},
    '86': {'country': 'China', 'format': '+86 XXX XXXX XXXX'},
    '90': {'country': 'Turkey', 'format': '+90 XXX XXX XXXX'},
    '91': {'country': 'India', 'format': '+91 XXXXX XXXXX'},
    '92': {'country': 'Pakistan', 'format': '+92 XXX XXXXXXX'},
    '93': {'country': 'Afghanistan', 'format': '+93 XX XXX XXXX'},
    '94': {'country': 'Sri Lanka', 'format': '+94 XX XXX XXXX'},
    '95': {'country': 'Myanmar', 'format': '+95 XX XXX XXXX'},
    '98': {'country': 'Iran', 'format': '+98 XXX XXX XXXX'},
    '212': {'country': 'Morocco', 'format': '+212 XXX XXXXXX'},
    '213': {'country': 'Algeria', 'format': '+213 XXX XX XX XX'},
    '216': {'country': 'Tunisia', 'format': '+216 XX XXX XXX'},
    '234': {'country': 'Nigeria', 'format': '+234 XXX XXX XXXX'},
    '254': {'country': 'Kenya', 'format': '+254 XXX XXXXXX'},
    '351': {'country': 'Portugal', 'format': '+351 XXX XXX XXX'},
    '352': {'country': 'Luxembourg', 'format': '+352 XXX XXX XXX'},
    '353': {'country': 'Ireland', 'format': '+353 XX XXX XXXX'},
    '354': {'country': 'Iceland', 'format': '+354 XXX XXXX'},
    '358': {'country': 'Finland', 'format': '+358 XX XXX XXXX'},
    '370': {'country': 'Lithuania', 'format': '+370 XXX XXXXX'},
    '371': {'country': 'Latvia', 'format': '+371 XXXX XXXX'},
    '372': {'country': 'Estonia', 'format': '+372 XXXX XXXX'},
    '380': {'country': 'Ukraine', 'format': '+380 XX XXX XXXX'},
    '381': {'country': 'Serbia', 'format': '+381 XX XXX XXXX'},
    '385': {'country': 'Croatia', 'format': '+385 XX XXX XXXX'},
    '386': {'country': 'Slovenia', 'format': '+386 XX XXX XXX'},
    '420': {'country': 'Czech Republic', 'format': '+420 XXX XXX XXX'},
    '421': {'country': 'Slovakia', 'format': '+421 XXX XXX XXX'},
    '852': {'country': 'Hong Kong', 'format': '+852 XXXX XXXX'},
    '853': {'country': 'Macau', 'format': '+853 XXXX XXXX'},
    '886': {'country': 'Taiwan', 'format': '+886 X XXXX XXXX'},
    '961': {'country': 'Lebanon', 'format': '+961 XX XXX XXX'},
    '962': {'country': 'Jordan', 'format': '+962 X XXX XXXX'},
    '963': {'country': 'Syria', 'format': '+963 XXX XXX XXX'},
    '964': {'country': 'Iraq', 'format': '+964 XXX XXX XXXX'},
    '965': {'country': 'Kuwait', 'format': '+965 XXXX XXXX'},
    '966': {'country': 'Saudi Arabia', 'format': '+966 XX XXX XXXX'},
    '971': {'country': 'United Arab Emirates', 'format': '+971 XX XXX XXXX'},
    '972': {'country': 'Israel', 'format': '+972 XX XXX XXXX'},
    '974': {'country': 'Qatar', 'format': '+974 XXXX XXXX'},
}

# US Area codes by state/region (partial list)
US_AREA_CODES = {
    '201': 'New Jersey', '202': 'Washington DC', '203': 'Connecticut',
    '205': 'Alabama', '206': 'Washington', '207': 'Maine',
    '208': 'Idaho', '209': 'California', '210': 'Texas',
    '212': 'New York', '213': 'California', '214': 'Texas',
    '215': 'Pennsylvania', '216': 'Ohio', '217': 'Illinois',
    '218': 'Minnesota', '219': 'Indiana', '224': 'Illinois',
    '225': 'Louisiana', '228': 'Mississippi', '229': 'Georgia',
    '231': 'Michigan', '234': 'Ohio', '239': 'Florida',
    '240': 'Maryland', '248': 'Michigan', '251': 'Alabama',
    '252': 'North Carolina', '253': 'Washington', '254': 'Texas',
    '256': 'Alabama', '260': 'Indiana', '262': 'Wisconsin',
    '267': 'Pennsylvania', '269': 'Michigan', '270': 'Kentucky',
    '272': 'Pennsylvania', '276': 'Virginia', '281': 'Texas',
    '301': 'Maryland', '302': 'Delaware', '303': 'Colorado',
    '304': 'West Virginia', '305': 'Florida', '307': 'Wyoming',
    '308': 'Nebraska', '309': 'Illinois', '310': 'California',
    '312': 'Illinois', '313': 'Michigan', '314': 'Missouri',
    '315': 'New York', '316': 'Kansas', '317': 'Indiana',
    '318': 'Louisiana', '319': 'Iowa', '320': 'Minnesota',
    '321': 'Florida', '323': 'California', '325': 'Texas',
    '330': 'Ohio', '331': 'Illinois', '334': 'Alabama',
    '336': 'North Carolina', '337': 'Louisiana', '339': 'Massachusetts',
    '340': 'US Virgin Islands', '346': 'Texas', '347': 'New York',
    '351': 'Massachusetts', '352': 'Florida', '360': 'Washington',
    '361': 'Texas', '364': 'Kentucky', '385': 'Utah',
    '386': 'Florida', '401': 'Rhode Island', '402': 'Nebraska',
    '404': 'Georgia', '405': 'Oklahoma', '406': 'Montana',
    '407': 'Florida', '408': 'California', '409': 'Texas',
    '410': 'Maryland', '412': 'Pennsylvania', '413': 'Massachusetts',
    '414': 'Wisconsin', '415': 'California', '417': 'Missouri',
    '419': 'Ohio', '423': 'Tennessee', '424': 'California',
    '425': 'Washington', '430': 'Texas', '432': 'Texas',
    '434': 'Virginia', '435': 'Utah', '440': 'Ohio',
    '442': 'California', '443': 'Maryland', '458': 'Oregon',
    '469': 'Texas', '470': 'Georgia', '475': 'Connecticut',
    '478': 'Georgia', '479': 'Arkansas', '480': 'Arizona',
    '484': 'Pennsylvania', '501': 'Arkansas', '502': 'Kentucky',
    '503': 'Oregon', '504': 'Louisiana', '505': 'New Mexico',
    '507': 'Minnesota', '508': 'Massachusetts', '509': 'Washington',
    '510': 'California', '512': 'Texas', '513': 'Ohio',
    '515': 'Iowa', '516': 'New York', '517': 'Michigan',
    '518': 'New York', '520': 'Arizona', '530': 'California',
    '531': 'Nebraska', '534': 'Wisconsin', '539': 'Oklahoma',
    '540': 'Virginia', '541': 'Oregon', '551': 'New Jersey',
    '559': 'California', '561': 'Florida', '562': 'California',
    '563': 'Iowa', '567': 'Ohio', '570': 'Pennsylvania',
    '571': 'Virginia', '573': 'Missouri', '574': 'Indiana',
    '575': 'New Mexico', '580': 'Oklahoma', '585': 'New York',
    '586': 'Michigan', '601': 'Mississippi', '602': 'Arizona',
    '603': 'New Hampshire', '605': 'South Dakota', '606': 'Kentucky',
    '607': 'New York', '608': 'Wisconsin', '609': 'New Jersey',
    '610': 'Pennsylvania', '612': 'Minnesota', '614': 'Ohio',
    '615': 'Tennessee', '616': 'Michigan', '617': 'Massachusetts',
    '618': 'Illinois', '619': 'California', '620': 'Kansas',
    '623': 'Arizona', '626': 'California', '628': 'California',
    '629': 'Tennessee', '630': 'Illinois', '631': 'New York',
    '636': 'Missouri', '641': 'Iowa', '646': 'New York',
    '650': 'California', '651': 'Minnesota', '657': 'California',
    '660': 'Missouri', '661': 'California', '662': 'Mississippi',
    '667': 'Maryland', '669': 'California', '678': 'Georgia',
    '681': 'West Virginia', '682': 'Texas', '701': 'North Dakota',
    '702': 'Nevada', '703': 'Virginia', '704': 'North Carolina',
    '706': 'Georgia', '707': 'California', '708': 'Illinois',
    '712': 'Iowa', '713': 'Texas', '714': 'California',
    '715': 'Wisconsin', '716': 'New York', '717': 'Pennsylvania',
    '718': 'New York', '719': 'Colorado', '720': 'Colorado',
    '724': 'Pennsylvania', '725': 'Nevada', '727': 'Florida',
    '731': 'Tennessee', '732': 'New Jersey', '734': 'Michigan',
    '737': 'Texas', '740': 'Ohio', '743': 'North Carolina',
    '747': 'California', '754': 'Florida', '757': 'Virginia',
    '760': 'California', '762': 'Georgia', '763': 'Minnesota',
    '765': 'Indiana', '769': 'Mississippi', '770': 'Georgia',
    '772': 'Florida', '773': 'Illinois', '774': 'Massachusetts',
    '775': 'Nevada', '779': 'Illinois', '781': 'Massachusetts',
    '785': 'Kansas', '786': 'Florida', '801': 'Utah',
    '802': 'Vermont', '803': 'South Carolina', '804': 'Virginia',
    '805': 'California', '806': 'Texas', '808': 'Hawaii',
    '810': 'Michigan', '812': 'Indiana', '813': 'Florida',
    '814': 'Pennsylvania', '815': 'Illinois', '816': 'Missouri',
    '817': 'Texas', '818': 'California', '828': 'North Carolina',
    '830': 'Texas', '831': 'California', '832': 'Texas',
    '843': 'South Carolina', '845': 'New York', '847': 'Illinois',
    '848': 'New Jersey', '850': 'Florida', '856': 'New Jersey',
    '857': 'Massachusetts', '858': 'California', '859': 'Kentucky',
    '860': 'Connecticut', '862': 'New Jersey', '863': 'Florida',
    '864': 'South Carolina', '865': 'Tennessee', '870': 'Arkansas',
    '872': 'Illinois', '878': 'Pennsylvania', '901': 'Tennessee',
    '903': 'Texas', '904': 'Florida', '906': 'Michigan',
    '907': 'Alaska', '908': 'New Jersey', '909': 'California',
    '910': 'North Carolina', '912': 'Georgia', '913': 'Kansas',
    '914': 'New York', '915': 'Texas', '916': 'California',
    '917': 'New York', '918': 'Oklahoma', '919': 'North Carolina',
    '920': 'Wisconsin', '925': 'California', '928': 'Arizona',
    '929': 'New York', '931': 'Tennessee', '936': 'Texas',
    '937': 'Ohio', '938': 'Alabama', '940': 'Texas',
    '941': 'Florida', '947': 'Michigan', '949': 'California',
    '951': 'California', '952': 'Minnesota', '954': 'Florida',
    '956': 'Texas', '959': 'Connecticut', '970': 'Colorado',
    '971': 'Oregon', '972': 'Texas', '973': 'New Jersey',
    '978': 'Massachusetts', '979': 'Texas', '980': 'North Carolina',
    '984': 'North Carolina', '985': 'Louisiana', '989': 'Michigan',
}

# Carrier identification patterns
CARRIER_PATTERNS = {
    'verizon': ['vzw', 'verizon', 'vtext'],
    'att': ['att', 'at&t', 'cingular'],
    'tmobile': ['tmobile', 't-mobile', 'tmo'],
    'sprint': ['sprint', 'sprintpcs'],
    'cricket': ['cricket'],
    'metropcs': ['metro', 'metropcs'],
    'boost': ['boost'],
    'virgin': ['virgin'],
    'uscellular': ['uscellular', 'us cellular'],
    'google_voice': ['google', 'googlevoice'],
    'voip': ['voip', 'bandwidth', 'twilio', 'plivo', 'nexmo'],
}


class PhoneNumberParser:
    """Parse and analyze phone numbers"""

    def __init__(self):
        self.country_codes = COUNTRY_CODES
        self.us_area_codes = US_AREA_CODES

    def clean_number(self, phone: str) -> str:
        """Remove all non-digit characters except leading +"""
        has_plus = phone.strip().startswith('+')
        digits = re.sub(r'[^\d]', '', phone)
        return f'+{digits}' if has_plus else digits

    def parse(self, phone: str) -> Dict:
        """Parse a phone number and return detailed information"""
        original = phone
        cleaned = self.clean_number(phone)

        # Remove leading + for processing
        digits = cleaned.lstrip('+')

        result = {
            'original': original,
            'cleaned': cleaned,
            'digits_only': digits,
            'valid': False,
            'country': 'Unknown',
            'country_code': '',
            'national_number': '',
            'formatted': '',
            'location': '',
            'line_type': 'Unknown',
            'carrier': 'Unknown',
            'timezone': '',
            'possible_formats': []
        }

        if not digits or len(digits) < 7:
            result['error'] = 'Phone number too short'
            return result

        if len(digits) > 15:
            result['error'] = 'Phone number too long'
            return result

        # Try to identify country code
        country_info = self._identify_country(digits, cleaned.startswith('+'))

        if country_info:
            result.update(country_info)
            result['valid'] = True

            # For US numbers, get additional info
            if country_info['country_code'] == '1':
                us_info = self._parse_us_number(country_info['national_number'])
                result.update(us_info)

        # Generate possible formats
        result['possible_formats'] = self._generate_formats(digits, result.get('country_code', ''))

        # Determine line type (basic heuristic)
        result['line_type'] = self._guess_line_type(digits)

        return result

    def _identify_country(self, digits: str, has_plus: bool) -> Optional[Dict]:
        """Identify country from phone number"""
        # If starts with +, try to match country code
        if has_plus or len(digits) > 10:
            # Try 1-3 digit country codes
            for length in [1, 2, 3]:
                if len(digits) >= length:
                    code = digits[:length]
                    if code in self.country_codes:
                        return {
                            'country_code': code,
                            'country': self.country_codes[code]['country'],
                            'national_number': digits[length:],
                            'formatted': f'+{code} {digits[length:]}'
                        }

        # Assume US/Canada for 10-digit numbers without country code
        if len(digits) == 10:
            return {
                'country_code': '1',
                'country': 'United States/Canada',
                'national_number': digits,
                'formatted': f'+1 ({digits[:3]}) {digits[3:6]}-{digits[6:]}'
            }

        # Assume US/Canada for 11-digit numbers starting with 1
        if len(digits) == 11 and digits.startswith('1'):
            national = digits[1:]
            return {
                'country_code': '1',
                'country': 'United States/Canada',
                'national_number': national,
                'formatted': f'+1 ({national[:3]}) {national[3:6]}-{national[6:]}'
            }

        return None

    def _parse_us_number(self, national: str) -> Dict:
        """Parse US-specific information"""
        result = {}

        if len(national) >= 3:
            area_code = national[:3]
            if area_code in self.us_area_codes:
                result['location'] = self.us_area_codes[area_code]
                result['area_code'] = area_code

        return result

    def _generate_formats(self, digits: str, country_code: str) -> List[str]:
        """Generate various possible formats for the number"""
        formats = []

        if country_code == '1' or (len(digits) == 10 and not country_code):
            # US formats
            d = digits[-10:] if len(digits) >= 10 else digits
            if len(d) == 10:
                formats.extend([
                    f'+1{d}',
                    f'+1 {d}',
                    f'+1-{d[:3]}-{d[3:6]}-{d[6:]}',
                    f'+1 ({d[:3]}) {d[3:6]}-{d[6:]}',
                    f'1{d}',
                    f'1-{d[:3]}-{d[3:6]}-{d[6:]}',
                    f'({d[:3]}) {d[3:6]}-{d[6:]}',
                    f'{d[:3]}-{d[3:6]}-{d[6:]}',
                    f'{d[:3]}.{d[3:6]}.{d[6:]}',
                    f'{d[:3]} {d[3:6]} {d[6:]}',
                    d
                ])
        else:
            # Generic formats
            formats.extend([
                f'+{digits}',
                digits,
                f'+{digits[:len(country_code)]} {digits[len(country_code):]}' if country_code else digits
            ])

        return list(set(formats))

    def _guess_line_type(self, digits: str) -> str:
        """Make educated guess about line type"""
        # This is a simplified heuristic
        # Real implementation would use carrier lookup APIs

        if len(digits) >= 10:
            # Check for known VoIP prefixes (simplified)
            prefix = digits[-10:-7] if len(digits) >= 10 else ''

            # Some area codes are commonly used for VoIP
            voip_common = ['424', '442', '559', '657', '669', '747']
            if prefix in voip_common:
                return 'Possibly VoIP'

        return 'Unknown (Landline/Mobile/VoIP)'


def format_phone_number(phone: str, format_type: str = 'international') -> str:
    """Format a phone number in the specified format"""
    parser = PhoneNumberParser()
    info = parser.parse(phone)

    if not info['valid']:
        return phone

    if format_type == 'international':
        return info['formatted']
    elif format_type == 'national':
        return info['national_number']
    elif format_type == 'e164':
        return f"+{info['country_code']}{info['national_number']}"
    else:
        return info['formatted']


def get_phone_info(phone: str) -> Dict:
    """Get detailed information about a phone number"""
    parser = PhoneNumberParser()
    return parser.parse(phone)
