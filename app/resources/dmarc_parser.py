import re

class DMARCParser:
    def __init__(self, dmarc_record):
        self.dmarc_record = dmarc_record
        self.parsed = {}

    def parse(self):
        if not self.dmarc_record.startswith('v=DMARC1'):
            raise ValueError('Invalid DMARC record: Missing v=DMARC1')
        tags = self.dmarc_record.split(';')
        for tag in tags:
            tag = tag.strip()
            if not tag:
                continue
            if '=' in tag:
                key, value = tag.split('=', 1)
                key = key.strip()
                value = value.strip()
                self.parsed[key] = value
            else:
                raise ValueError(f'Invalid tag format: {tag}')
        required_tags = ['v', 'p']
        for tag in required_tags:
            if tag not in self.parsed:
                # TODO: return all exceptions if multiple tags are missing
                raise ValueError(f'Missing required tag: {tag}')
        self.validate_tags()
        return self.parsed

    def validate_tags(self):
        if self.parsed['v'] != 'DMARC1':
            raise ValueError("Invalid 'v' tag value, must be 'DMARC1'")
        if self.parsed['p'] not in ['none', 'quarantine', 'reject']:
            raise ValueError("Invalid 'p' tag value, must be 'none', 'quarantine', or 'reject'")
        if 'sp' in self.parsed:
            if self.parsed['sp'] not in ['none', 'quarantine', 'reject']:
                raise ValueError("Invalid 'sp' tag value, must be 'none', 'quarantine', or 'reject'")
        if 'adkim' in self.parsed:
            if self.parsed['adkim'] not in ['r', 's']:
                raise ValueError("Invalid 'adkim' tag value, must be 'r' or 's'")
        if 'aspf' in self.parsed:
            if self.parsed['aspf'] not in ['r', 's']:
                raise ValueError("Invalid 'aspf' tag value, must be 'r' or 's'")
        if 'pct' in self.parsed:
            if not self.parsed['pct'].isdigit() or not (0 <= int(self.parsed['pct']) <= 100):
                raise ValueError("Invalid 'pct' tag value, must be an integer between 0 and 100")
        if 'ri' in self.parsed:
            if not self.parsed['ri'].isdigit():
                raise ValueError("Invalid 'ri' tag value, must be an integer")
       # TODO: add rua and ruf tag validation
