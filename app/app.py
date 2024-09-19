from flask import Flask, request, jsonify
from resources.dmarc_parser import DMARCParser
from decorators import require_api_key
import dns.resolver
import os

app = Flask(__name__)

@app.route('/parse_dmarc', methods=['POST'])
@require_api_key
def parse_dmarc():
    # TODO: json format validation
    data = request.get_json()
    dmarc_record = data.get('dmarc_record')
    if not dmarc_record:
        return jsonify({'error': 'No DMARC record provided'}), 400
    parser = DMARCParser(dmarc_record)
    try:
        parsed_result = parser.parse()
        return jsonify(parsed_result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/check_dmarc/<domain>', methods=['GET'])
@require_api_key
def check_dmarc(domain):
    try:
        txt_records = dns.resolver.resolve('_dmarc.' + domain, 'TXT')
        dmarc_record = ''
        for txt_rec in txt_records:
            record = ''.join([b.decode('utf-8') for b in txt_rec.strings])
            if record.startswith('v=DMARC1'):
                dmarc_record = record
                break
        if not dmarc_record:
            return jsonify({'error': 'No DMARC record found'}), 404
        parser = DMARCParser(dmarc_record)
        parsed_result = parser.parse()
        return jsonify(parsed_result), 200
    except dns.resolver.NXDOMAIN:
        return jsonify({'error': 'Domain does not exist'}), 404
    except dns.resolver.NoAnswer:
        return jsonify({'error': 'No DMARC record found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
