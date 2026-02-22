#!/usr/bin/env python3
"""
Enhanced Flask Web Application with REAL AI
Fixed: removed duplicate simulate-attack route and moved imports before main block.
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from file_encryptor import FileEncryptor
from ai_security_monitor import AISecurityMonitor, MLPerformancePredictor
from quantum_threat_intel import QuantumThreatIntelligence
from real_ai_assistant import RealTimeAIAssistant  # NEW: Real AI
from quantum_attack_viz import QuantumAttackSimulator   # moved here (was duplicated after main)
import os
import io
import tempfile
import time

app = Flask(__name__,
            static_folder='../frontend/static',
            template_folder='../frontend/templates')
CORS(app)

# Initialize AI components
ai_monitor = AISecurityMonitor()
ml_predictor = MLPerformancePredictor()
threat_intel = QuantumThreatIntelligence()
crypto_assistant = RealTimeAIAssistant()  # NEW: Real AI with Groq
active_encryptors = {}
encrypted_files = {}  # session_id -> (file_path, original_filename)

# Initialize attack simulator
attack_simulator = QuantumAttackSimulator()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/generate-keys', methods=['POST'])
def generate_keys():
    try:
        data = request.json
        algorithm = data.get('algorithm', 'kyber768')

        encryptor = FileEncryptor(algorithm)
        keys = encryptor.generate_keys()

        session_id = os.urandom(16).hex()
        active_encryptors[session_id] = encryptor

        return jsonify({
            'success': True,
            'session_id': session_id,
            'algorithm': algorithm,
            'generation_time': keys['generation_time'],
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/encrypt', methods=['POST'])
def encrypt_file():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400

        file = request.files['file']
        session_id = request.form.get('session_id')

        if not session_id or session_id not in active_encryptors:
            return jsonify({'success': False, 'error': 'Invalid session'}), 400

        encryptor = active_encryptors[session_id]

        with tempfile.NamedTemporaryFile(delete=False) as tmp_input:
            file.save(tmp_input.name)
            input_path = tmp_input.name

        with tempfile.NamedTemporaryFile(delete=False, suffix='.encrypted') as tmp_output:
            output_path = tmp_output.name

        original_filename = file.filename or 'file'
        encrypted_path, metadata = encryptor.encrypt_file(input_path, output_path)

        # Store encrypted file path so it can be downloaded later
        encrypted_files[session_id] = (encrypted_path, original_filename)

        # AI anomaly detection
        encryption_data = {
            'file_size': metadata['original_size'],
            'encryption_time': metadata['encryption_time'],
            'algorithm': metadata['algorithm'],
            'key_size': 1184 if 'kyber' in metadata['algorithm'] else 256,
            'timestamp': time.time()
        }

        anomaly_result = ai_monitor.detect_anomaly(encryption_data)

        os.unlink(input_path)

        return jsonify({
            'success': True,
            'metadata': {
                'algorithm': metadata['algorithm'],
                'encryption_time': metadata['encryption_time'],
                'original_size': metadata['original_size'],
            },
            'ai_analysis': anomaly_result,
            'download_ready': True
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/benchmark', methods=['POST'])
def run_benchmark():
    try:
        from compare_algorithms import benchmark_kyber, benchmark_rsa

        kyber_results = benchmark_kyber(50)
        rsa_results = benchmark_rsa(50)

        return jsonify({
            'success': True,
            'kyber': kyber_results,
            'rsa': rsa_results
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/threat-intel', methods=['GET'])
def get_threat_intel():
    """Get quantum threat intelligence"""
    try:
        report = threat_intel.generate_threat_report()
        rsa2048 = threat_intel.predict_breaking_timeline('RSA-2048')

        return jsonify({
            'success': True,
            'current_year': 2026,
            'report': report,
            'rsa2048_prediction': rsa2048
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/assess-data-risk', methods=['POST'])
def assess_data_risk():
    """Assess risk for specific encrypted data"""
    try:
        data = request.json
        encryption_date = data.get('encryption_date')
        sensitivity = data.get('sensitivity', 'CONFIDENTIAL')
        algorithm = data.get('algorithm', 'RSA-2048')

        risk = threat_intel.assess_data_risk(encryption_date, sensitivity, algorithm)

        return jsonify({
            'success': True,
            'risk_assessment': risk
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/chat', methods=['POST'])
def chat():
    """REAL AI assistant chat endpoint"""
    try:
        data = request.json
        question = data.get('question', '')

        if not question:
            return jsonify({'success': False, 'error': 'No question provided'}), 400

        # Use REAL AI to answer
        answer = crypto_assistant.ask(question)

        return jsonify({
            'success': True,
            'answer': answer,
            'timestamp': time.time(),
            'ai_powered': crypto_assistant.enabled  # Let frontend know if using real AI
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/security-dashboard', methods=['GET'])
def security_dashboard():
    """Get AI security monitoring dashboard"""
    try:
        dashboard = ai_monitor.get_security_dashboard()

        return jsonify({
            'success': True,
            'dashboard': dashboard
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/download-encrypted', methods=['GET'])
def download_encrypted():
    """Download the encrypted file for a given session"""
    session_id = request.args.get('session_id')
    if not session_id or session_id not in encrypted_files:
        return jsonify({'success': False, 'error': 'No encrypted file found for this session'}), 404

    file_path, original_filename = encrypted_files.pop(session_id)  # remove immediately
    download_name = original_filename + '.encrypted'

    try:
        # Read entire file into memory first, then delete the temp file
        with open(file_path, 'rb') as f:
            file_data = f.read()
    except Exception as e:
        return jsonify({'success': False, 'error': f'Could not read encrypted file: {e}'}), 500
    finally:
        # Always clean up the temp file
        try:
            os.unlink(file_path)
        except Exception:
            pass

    # Serve from memory — 100% reliable, no streaming race condition
    buf = io.BytesIO(file_data)
    buf.seek(0)
    return send_file(
        buf,
        as_attachment=True,
        download_name=download_name,
        mimetype='application/octet-stream'
    )


@app.route('/api/simulate-attack', methods=['POST'])
def simulate_attack():
    """Simulate quantum attack on encryption"""
    try:
        data = request.json
        algorithm = data.get('algorithm', 'rsa')
        key_size = data.get('key_size', 2048)

        stages = attack_simulator.simulate_attack(algorithm, key_size)

        return jsonify({
            'success': True,
            'algorithm': algorithm,
            'stages': stages,
            'total_time': sum(s['time'] for s in stages)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/export-keys', methods=['GET'])
def export_keys():
    """Download the current session's keys as a JSON file."""
    session_id = request.args.get('session_id')
    if not session_id or session_id not in active_encryptors:
        return jsonify({'success': False, 'error': 'No active session.'}), 400

    encryptor = active_encryptors[session_id]
    if not encryptor.keys:
        return jsonify({'success': False, 'error': 'No keys in session.'}), 400

    import json as _json
    keys_json = _json.dumps(encryptor.keys, indent=2).encode('utf-8')
    buf = io.BytesIO(keys_json)
    buf.seek(0)
    return send_file(
        buf,
        as_attachment=True,
        download_name='qbits_private_key.json',
        mimetype='application/json'
    )


@app.route('/api/import-keys', methods=['POST'])
def import_keys():
    """Upload a previously exported key file and create a new decryption session."""
    try:
        if 'keyfile' not in request.files:
            return jsonify({'success': False, 'error': 'No key file provided.'}), 400

        keyfile = request.files['keyfile']
        import json as _json
        try:
            keys = _json.loads(keyfile.read().decode('utf-8'))
        except Exception:
            return jsonify({'success': False, 'error': 'Invalid key file format. Must be a QBits JSON key file.'}), 400

        algorithm = keys.get('algorithm', 'kyber768')
        encryptor = FileEncryptor(algorithm)
        encryptor.keys = keys

        # Restore the live KEM object so decryption actually works
        from crypto_engine import CryptoEngine
        import base64
        try:
            if 'kyber_secret' in keys:
                from oqs import KeyEncapsulation
                encryptor.engine.kyber_kem = KeyEncapsulation("Kyber768")
                encryptor.engine.kyber_kem.generate_keypair()  # init structure
                # Re-import the secret key
                secret_bytes = base64.b64decode(keys['kyber_secret'])
                # Directly set the secret key via a fresh KEM using secret bytes
                kem2 = KeyEncapsulation("Kyber768", secret_bytes)
                encryptor.engine.kyber_kem = kem2
        except Exception as e:
            return jsonify({'success': False, 'error': f'Failed to restore KEM from key file: {e}'}), 500

        session_id = os.urandom(16).hex()
        active_encryptors[session_id] = encryptor

        return jsonify({
            'success': True,
            'session_id': session_id,
            'algorithm': algorithm,
            'message': 'Key file loaded successfully. You can now decrypt files encrypted with these keys.'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/decrypt', methods=['POST'])

def decrypt_file():
    """Decrypt a previously encrypted file and stream it back."""
    try:
        session_id = request.form.get('session_id')
        if not session_id or session_id not in active_encryptors:
            return jsonify({'success': False, 'error': 'No active session. Please generate keys first.'}), 400

        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided.'}), 400

        uploaded_file = request.files['file']
        if uploaded_file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected.'}), 400

        # Read the encrypted JSON into memory
        file_bytes = uploaded_file.read()

        import json as _json
        try:
            encrypted_data = _json.loads(file_bytes.decode('utf-8'))
        except Exception:
            return jsonify({'success': False, 'error': 'File is not a valid QBits encrypted JSON.'}), 400

        encryptor = active_encryptors[session_id]

        # Write to a temp file so the encryptor can read it
        with tempfile.NamedTemporaryFile(suffix='.encrypted', delete=False) as tmp_in:
            tmp_in.write(file_bytes)
            tmp_in_path = tmp_in.name

        tmp_out_path = None
        try:
            output_path, decrypted_data = encryptor.decrypt_file(tmp_in_path)
            tmp_out_path = output_path

            # Determine the original filename from the encrypted metadata
            original_filename = encrypted_data.get('original_filename', 'decrypted_file')

            buf = io.BytesIO(decrypted_data)
            buf.seek(0)
            return send_file(
                buf,
                as_attachment=True,
                download_name=original_filename,
                mimetype='application/octet-stream'
            )
        except Exception as e:
            return jsonify({'success': False, 'error': f'Decryption failed: {str(e)}'}), 500
        finally:
            try:
                os.unlink(tmp_in_path)
            except Exception:
                pass
            if tmp_out_path:
                try:
                    os.unlink(tmp_out_path)
                except Exception:
                    pass
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':

    print("=" * 70)
    print("🚀 QBits - AI-POWERED QUANTUM-SAFE ENCRYPTION PLATFORM")
    print("=" * 70)
    print("\n🌐 Starting server at http://localhost:5000")
    print("\n✨ FEATURES:")
    print("   🤖 REAL AI Assistant (powered by Groq LLM)")
    print("   📊 ML-based anomaly detection")
    print("   🌐 Quantum threat intelligence")
    print("   🛡️  Real-time security monitoring")
    print("   🔐 NIST-approved PQC encryption")

    if crypto_assistant.enabled:
        print("\n✅ AI Mode: FULL (Real-time LLM responses)")
    else:
        print("\n⚠️  AI Mode: LIMITED (Set GROQ_API_KEY for full AI)")
        print("   Get FREE key: https://console.groq.com")

    print("\n⚠️  Press Ctrl+C to stop\n")
    print("=" * 70)

    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
