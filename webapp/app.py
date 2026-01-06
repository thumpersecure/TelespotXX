"""
TeleSpotter Web Application
A comprehensive phone number OSINT web interface
"""

import os
import json
import re
import asyncio
from datetime import datetime
from flask import Flask, render_template, request, jsonify, Response
from flask_socketio import SocketIO, emit
import threading
import time

# Import modules
from modules.phone_utils import PhoneNumberParser, format_phone_number, get_phone_info
from modules.search_engines import SearchEngineManager
from modules.people_search import PeopleSearchManager
from modules.pattern_analysis import PatternAnalyzer

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'telespotter-secret-key-change-in-production')
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Store active searches
active_searches = {}


class SearchSession:
    """Manages a single phone number search session"""

    def __init__(self, session_id, phone_number, options):
        self.session_id = session_id
        self.phone_number = phone_number
        self.options = options
        self.results = {
            'phone_info': {},
            'search_engines': [],
            'people_search': [],
            'patterns': {
                'names': [],
                'emails': [],
                'addresses': [],
                'usernames': [],
                'associated_phones': [],
                'social_profiles': []
            },
            'raw_data': []
        }
        self.progress = 0
        self.status = 'initializing'
        self.start_time = datetime.now()
        self.errors = []

    def to_dict(self):
        return {
            'session_id': self.session_id,
            'phone_number': self.phone_number,
            'results': self.results,
            'progress': self.progress,
            'status': self.status,
            'start_time': self.start_time.isoformat(),
            'errors': self.errors,
            'options': self.options
        }


def emit_progress(session_id, progress, message, status='running'):
    """Emit progress update via WebSocket"""
    socketio.emit('progress', {
        'session_id': session_id,
        'progress': progress,
        'message': message,
        'status': status
    }, room=session_id)


def emit_result(session_id, result_type, data):
    """Emit result update via WebSocket"""
    socketio.emit('result', {
        'session_id': session_id,
        'type': result_type,
        'data': data
    }, room=session_id)


def run_search(session_id, phone_number, options):
    """Run the complete search process"""
    session = active_searches.get(session_id)
    if not session:
        return

    try:
        # Phase 1: Parse and validate phone number (5%)
        emit_progress(session_id, 5, 'Parsing phone number...')
        session.status = 'parsing'

        parser = PhoneNumberParser()
        phone_info = parser.parse(phone_number)
        session.results['phone_info'] = phone_info
        emit_result(session_id, 'phone_info', phone_info)

        if not phone_info.get('valid', False):
            emit_progress(session_id, 100, 'Invalid phone number format', 'error')
            session.status = 'error'
            session.errors.append('Invalid phone number format')
            return

        formatted_number = phone_info.get('formatted', phone_number)

        # Phase 2: Search engines (5-40%)
        if options.get('search_engines', True):
            emit_progress(session_id, 10, 'Searching search engines...')
            session.status = 'searching_engines'

            search_manager = SearchEngineManager()
            engines_to_search = []

            if options.get('google', True):
                engines_to_search.append('google')
            if options.get('bing', True):
                engines_to_search.append('bing')
            if options.get('duckduckgo', True):
                engines_to_search.append('duckduckgo')

            progress_per_engine = 30 / max(len(engines_to_search), 1)
            current_progress = 10

            for engine in engines_to_search:
                emit_progress(session_id, int(current_progress), f'Searching {engine.capitalize()}...')
                try:
                    results = search_manager.search(engine, formatted_number, options)
                    session.results['search_engines'].extend(results)
                    emit_result(session_id, 'search_engine', {'engine': engine, 'results': results})
                except Exception as e:
                    session.errors.append(f'{engine}: {str(e)}')
                current_progress += progress_per_engine
                time.sleep(0.5)  # Rate limiting

        # Phase 3: People search sites (40-70%)
        if options.get('people_search', True):
            emit_progress(session_id, 40, 'Searching people search sites...')
            session.status = 'searching_people'

            people_manager = PeopleSearchManager()
            sites_to_search = []

            if options.get('whitepages', True):
                sites_to_search.append('whitepages')
            if options.get('truepeoplesearch', True):
                sites_to_search.append('truepeoplesearch')
            if options.get('fastpeoplesearch', True):
                sites_to_search.append('fastpeoplesearch')
            if options.get('spokeo', True):
                sites_to_search.append('spokeo')
            if options.get('beenverified', True):
                sites_to_search.append('beenverified')

            progress_per_site = 30 / max(len(sites_to_search), 1)
            current_progress = 40

            for site in sites_to_search:
                emit_progress(session_id, int(current_progress), f'Searching {site.replace("_", " ").title()}...')
                try:
                    results = people_manager.search(site, formatted_number, options)
                    session.results['people_search'].extend(results)
                    emit_result(session_id, 'people_search', {'site': site, 'results': results})
                except Exception as e:
                    session.errors.append(f'{site}: {str(e)}')
                current_progress += progress_per_site
                time.sleep(0.5)  # Rate limiting

        # Phase 4: Pattern analysis (70-90%)
        emit_progress(session_id, 70, 'Analyzing patterns...')
        session.status = 'analyzing'

        analyzer = PatternAnalyzer()
        all_text = []

        for result in session.results['search_engines']:
            all_text.append(result.get('title', ''))
            all_text.append(result.get('snippet', ''))

        for result in session.results['people_search']:
            all_text.append(json.dumps(result))

        combined_text = ' '.join(all_text)

        emit_progress(session_id, 75, 'Extracting names...')
        session.results['patterns']['names'] = analyzer.extract_names(combined_text)
        emit_result(session_id, 'pattern', {'type': 'names', 'data': session.results['patterns']['names']})

        emit_progress(session_id, 78, 'Extracting emails...')
        session.results['patterns']['emails'] = analyzer.extract_emails(combined_text)
        emit_result(session_id, 'pattern', {'type': 'emails', 'data': session.results['patterns']['emails']})

        emit_progress(session_id, 81, 'Extracting addresses...')
        session.results['patterns']['addresses'] = analyzer.extract_addresses(combined_text)
        emit_result(session_id, 'pattern', {'type': 'addresses', 'data': session.results['patterns']['addresses']})

        emit_progress(session_id, 84, 'Extracting usernames...')
        session.results['patterns']['usernames'] = analyzer.extract_usernames(combined_text)
        emit_result(session_id, 'pattern', {'type': 'usernames', 'data': session.results['patterns']['usernames']})

        emit_progress(session_id, 87, 'Finding associated phone numbers...')
        session.results['patterns']['associated_phones'] = analyzer.extract_phone_numbers(combined_text, formatted_number)
        emit_result(session_id, 'pattern', {'type': 'associated_phones', 'data': session.results['patterns']['associated_phones']})

        emit_progress(session_id, 90, 'Finding social profiles...')
        session.results['patterns']['social_profiles'] = analyzer.extract_social_profiles(combined_text)
        emit_result(session_id, 'pattern', {'type': 'social_profiles', 'data': session.results['patterns']['social_profiles']})

        # Phase 5: Finalize (90-100%)
        emit_progress(session_id, 95, 'Finalizing results...')
        session.status = 'finalizing'

        # Calculate confidence scores and deduplicate
        session.results = analyzer.finalize_results(session.results)

        emit_progress(session_id, 100, 'Search complete!', 'complete')
        session.status = 'complete'
        emit_result(session_id, 'complete', session.results)

    except Exception as e:
        emit_progress(session_id, session.progress, f'Error: {str(e)}', 'error')
        session.status = 'error'
        session.errors.append(str(e))


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/api/search', methods=['POST'])
def start_search():
    """Start a new phone number search"""
    data = request.json
    phone_number = data.get('phone_number', '').strip()
    options = data.get('options', {})

    if not phone_number:
        return jsonify({'error': 'Phone number is required'}), 400

    # Generate session ID
    session_id = f"search_{int(time.time() * 1000)}_{hash(phone_number) % 10000}"

    # Create session
    session = SearchSession(session_id, phone_number, options)
    active_searches[session_id] = session

    # Start search in background thread
    thread = threading.Thread(target=run_search, args=(session_id, phone_number, options))
    thread.daemon = True
    thread.start()

    return jsonify({
        'session_id': session_id,
        'status': 'started',
        'phone_number': phone_number
    })


@app.route('/api/search/<session_id>', methods=['GET'])
def get_search_status(session_id):
    """Get current search status and results"""
    session = active_searches.get(session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404

    return jsonify(session.to_dict())


@app.route('/api/search/<session_id>/export', methods=['GET'])
def export_results(session_id):
    """Export search results"""
    session = active_searches.get(session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404

    export_format = request.args.get('format', 'json')

    if export_format == 'json':
        return Response(
            json.dumps(session.to_dict(), indent=2),
            mimetype='application/json',
            headers={'Content-Disposition': f'attachment; filename=telespotter_{session_id}.json'}
        )
    elif export_format == 'csv':
        # Generate CSV
        csv_lines = ['Type,Value,Source,Confidence']

        for name in session.results['patterns'].get('names', []):
            csv_lines.append(f"Name,\"{name.get('value', '')}\",\"{name.get('source', '')}\",{name.get('confidence', 0)}")

        for email in session.results['patterns'].get('emails', []):
            csv_lines.append(f"Email,\"{email.get('value', '')}\",\"{email.get('source', '')}\",{email.get('confidence', 0)}")

        for address in session.results['patterns'].get('addresses', []):
            csv_lines.append(f"Address,\"{address.get('value', '')}\",\"{address.get('source', '')}\",{address.get('confidence', 0)}")

        for username in session.results['patterns'].get('usernames', []):
            csv_lines.append(f"Username,\"{username.get('value', '')}\",\"{username.get('source', '')}\",{username.get('confidence', 0)}")

        return Response(
            '\n'.join(csv_lines),
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename=telespotter_{session_id}.csv'}
        )
    elif export_format == 'txt':
        # Generate text report
        lines = [
            '=' * 60,
            'TELESPOTTER OSINT REPORT',
            '=' * 60,
            f'Phone Number: {session.phone_number}',
            f'Search Date: {session.start_time.strftime("%Y-%m-%d %H:%M:%S")}',
            '=' * 60,
            '',
            'PHONE INFORMATION',
            '-' * 40
        ]

        phone_info = session.results.get('phone_info', {})
        lines.append(f"Country: {phone_info.get('country', 'Unknown')}")
        lines.append(f"Carrier: {phone_info.get('carrier', 'Unknown')}")
        lines.append(f"Line Type: {phone_info.get('line_type', 'Unknown')}")
        lines.append(f"Location: {phone_info.get('location', 'Unknown')}")

        lines.extend(['', 'EXTRACTED NAMES', '-' * 40])
        for name in session.results['patterns'].get('names', []):
            lines.append(f"  - {name.get('value', '')} (confidence: {name.get('confidence', 0)}%)")

        lines.extend(['', 'EXTRACTED EMAILS', '-' * 40])
        for email in session.results['patterns'].get('emails', []):
            lines.append(f"  - {email.get('value', '')}")

        lines.extend(['', 'EXTRACTED ADDRESSES', '-' * 40])
        for address in session.results['patterns'].get('addresses', []):
            lines.append(f"  - {address.get('value', '')}")

        lines.extend(['', 'EXTRACTED USERNAMES', '-' * 40])
        for username in session.results['patterns'].get('usernames', []):
            lines.append(f"  - {username.get('value', '')}")

        lines.extend(['', 'SOCIAL PROFILES', '-' * 40])
        for profile in session.results['patterns'].get('social_profiles', []):
            lines.append(f"  - {profile.get('platform', '')}: {profile.get('url', '')}")

        lines.extend(['', '=' * 60, 'END OF REPORT', '=' * 60])

        return Response(
            '\n'.join(lines),
            mimetype='text/plain',
            headers={'Content-Disposition': f'attachment; filename=telespotter_{session_id}.txt'}
        )

    return jsonify({'error': 'Invalid export format'}), 400


@app.route('/api/validate', methods=['POST'])
def validate_phone():
    """Validate a phone number without full search"""
    data = request.json
    phone_number = data.get('phone_number', '').strip()

    if not phone_number:
        return jsonify({'error': 'Phone number is required'}), 400

    parser = PhoneNumberParser()
    info = parser.parse(phone_number)

    return jsonify(info)


@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    print(f'Client connected: {request.sid}')


@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    print(f'Client disconnected: {request.sid}')


@socketio.on('join')
def handle_join(data):
    """Join a search session room"""
    session_id = data.get('session_id')
    if session_id:
        from flask_socketio import join_room
        join_room(session_id)
        emit('joined', {'session_id': session_id})


@socketio.on('leave')
def handle_leave(data):
    """Leave a search session room"""
    session_id = data.get('session_id')
    if session_id:
        from flask_socketio import leave_room
        leave_room(session_id)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    socketio.run(app, host='0.0.0.0', port=port, debug=debug)
