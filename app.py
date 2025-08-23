#!/usr/bin/env python3

"""
🕵️ CIA Web Interface - Command Intelligence Agency
Web dashboard voor AI orchestration
"""

from flask import Flask, render_template, request, jsonify, Response
import asyncio
import json
from datetime import datetime
from cia import CIA, AIProvider
import threading
import queue

app = Flask(__name__)
cia = CIA()

# Queue voor streaming responses
response_queue = queue.Queue()

@app.route('/')
def index():
    """Landing page / Dashboard"""
    return render_template('index.html')

@app.route('/lab')
def lab():
    """GPT-5 Research Lab interface"""
    return render_template('gpt5_lab.html')

@app.route('/api/status')
def get_status():
    """Get status of all AI providers"""
    status = {
        'providers': [],
        'timestamp': datetime.now().isoformat()
    }
    
    for provider, data in cia.providers.items():
        provider_status = {
            'name': provider.value.upper(),
            'status': 'active' if data['api_key'] else 'missing_key',
            'models': data.get('models', []),
            'capabilities': data.get('capabilities', [])
        }
        status['providers'].append(provider_status)
    
    # Add special models we discovered
    status['special_models'] = {
        'gpt5_series': ['gpt-5', 'gpt-5-mini', 'gpt-5-nano'],
        'gpt4.1_series': ['gpt-4.1', 'gpt-4.1-mini', 'gpt-4.1-nano'],
        'preview_features': ['search-preview', 'realtime-preview', 'audio-preview']
    }
    
    return jsonify(status)

@app.route('/api/execute', methods=['POST'])
def execute_mission():
    """Execute mission on selected AI(s)"""
    data = request.json
    mission = data.get('mission', '')
    provider = data.get('provider', 'auto')
    parallel = data.get('parallel', False)
    model = data.get('model', None)  # Support specific model selection
    
    # Run async mission in sync context
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        if parallel:
            result = loop.run_until_complete(
                cia.execute_mission(mission, parallel=True)
            )
        elif provider == 'auto':
            result = loop.run_until_complete(
                cia.execute_mission(mission)
            )
        else:
            # Convert string to enum
            provider_enum = None
            for p in AIProvider:
                if p.value == provider.lower():
                    provider_enum = p
                    break
            
            if provider_enum:
                result = loop.run_until_complete(
                    cia.execute_mission(mission, provider=provider_enum, model=model)
                )
            else:
                result = {'error': f'Unknown provider: {provider}'}
    finally:
        loop.close()
    
    return jsonify(result)

@app.route('/api/models')
def get_models():
    """Get all available models"""
    models = {
        'openai': {
            'standard': ['gpt-4-turbo-preview', 'gpt-4', 'gpt-3.5-turbo'],
            'special': ['gpt-5', 'gpt-5-mini', 'gpt-5-nano'],
            'preview': ['gpt-4o-search-preview', 'gpt-4o-realtime-preview']
        },
        'google': ['gemini-pro', 'gemini-pro-vision'],
        'grok': ['grok-1']
    }
    return jsonify(models)

@app.route('/api/stream', methods=['POST'])
def stream_mission():
    """Stream responses from multiple AIs"""
    data = request.json
    mission = data.get('mission', '')
    
    def generate():
        # Send initial message
        yield f"data: {json.dumps({'type': 'start', 'message': 'Starting multi-AI query...'})}\n\n"
        
        # Execute on each provider
        for provider in ['chatgpt', 'google']:
            provider_enum = None
            for p in AIProvider:
                if p.value == provider:
                    provider_enum = p
                    break
            
            if provider_enum and cia.providers[provider_enum]['api_key']:
                yield f"data: {json.dumps({'type': 'provider_start', 'provider': provider})}\n\n"
                
                # Run async in thread
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                try:
                    result = loop.run_until_complete(
                        cia.execute_mission(mission, provider=provider_enum)
                    )
                    
                    yield f"data: {json.dumps({'type': 'provider_complete', 'provider': provider, 'result': result})}\n\n"
                finally:
                    loop.close()
        
        yield f"data: {json.dumps({'type': 'complete'})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'CIA Web Interface'})

if __name__ == '__main__':
    print("🕵️ CIA Web Interface starting...")
    print("📡 Access at: http://localhost:8080")
    print("📱 Also available at: http://127.0.0.1:8080")
    # Use port 8080 to avoid conflict with AirPlay on port 5000
    app.run(host='0.0.0.0', debug=True, port=8080)