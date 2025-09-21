import asyncio
import logging
import threading
import time
import shutil
import subprocess
import os
import socket

from typing import Optional, Tuple

from flask import Flask, render_template_string, request, redirect, url_for, jsonify, send_from_directory
from pyrogram.client import Client
from pyrogram.errors import RPCError, SessionPasswordNeeded
from pyrogram.errors import PhoneCodeInvalid, PhoneCodeExpired, PasswordHashInvalid
from pyrogram.types import User, TermsOfService


app = Flask(__name__)
code_input = None
auth_complete = False
auth_result = None
current_step = "phone"
current_phone = "+7"
sent_code_hash = None 
user_data = {'api_id': 0, 'api_hash': '', 'device_mod': ''}
error_message = ''


HTML_TEMPLATE = open('web_auth/site.html', 'r', encoding='utf-8').read()


@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('web_auth/static', filename)

@app.route('/', methods=['GET', 'POST'])
def auth_web():
    global code_input, auth_complete, current_step, current_phone, error_message
    
    if request.method == 'POST':
        if 'phone' in request.form:
            current_phone = request.form['phone']
            current_step = 'code' 
            error_message = ''
            return redirect(url_for('auth_web', step='code', phone=current_phone))
            
        elif 'code' in request.form:
            code_input = request.form['code']
            auth_complete = True 
            current_step = 'code' 
            # Очистим прошлую ошибку на попытку ввода нового кода
            error_message = ''
            return redirect(url_for('auth_web', step='code', phone=current_phone))
            
        elif 'password' in request.form:
            code_input = request.form['password']
            auth_complete = True 
            # Шаг сменится из фоновой логики; очищаем ошибку
            error_message = ''
            return redirect(url_for('auth_web', step='password', phone=current_phone))
    
    step = request.args.get('step', current_step)
    phone = request.args.get('phone', current_phone)
    error = request.args.get('error', '') or error_message
    
    if step == 'password':
        current_step = 'password'
        current_phone = phone
    
    return render_template_string(HTML_TEMPLATE, step=step, phone=phone, error=error)

@app.route('/check_step', methods=['GET'])
def check_step():
    global current_step, error_message
    return {'step': current_step, 'error': error_message}

@app.route('/submit_code', methods=['POST'])
def submit_code():
    global code_input, auth_complete, current_step
    code = request.form.get('code')
    phone = request.args.get('phone') 
    
    if not code:
        return jsonify({'error': 'Missing code'}), 400
    
    code_input = code
    auth_complete = True
    print(f"📝 Logging: Code entered: {code}")
    return jsonify({'message': 'Code received'})


@app.route('/submit_password', methods=['POST'])
def submit_password():
    global code_input, auth_complete, current_step
    password = request.form.get('password')
    
    if not password:
        return jsonify({'error': 'Missing password'}), 400
    
    code_input = password
    auth_complete = True
    print("📝 Logging: 2FA password entered")
    return jsonify({'message': 'Password received'})

def find_free_port() -> int:
    if "SHARKHOST" or "HIKKAHOST" in os.environ:
        return 8080
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 0))
        return s.getsockname()[1]

def ensure_ssh():
    try:
        result = subprocess.run(['ssh', '-V'], capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            print("❌ SSH not found!")
            return False
    except Exception as e:
        print(f"❌ Error checking SSH: {e}")
        return False

def get_public_url(port: int) -> Optional[str]:
    if not ensure_ssh():
        return None

    localhost_run_output_file = "localhost_run_output.txt"
    if os.path.exists(localhost_run_output_file):
        os.remove(localhost_run_output_file)

    try:      
        if os.name == 'nt':
            subprocess.Popen(
                f'ssh -o StrictHostKeyChecking=no -R 80:localhost:{port} nokey@localhost.run > {localhost_run_output_file} 2>&1 &',
                shell=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:
            subprocess.Popen(
            f'ssh -o StrictHostKeyChecking=no -R 80:localhost:{port} nokey@localhost.run > {localhost_run_output_file} 2>&1 &',
            shell=True,
            preexec_fn=os.setsid
        )
        
        timeout = 30 
        start_time = time.time()
        while time.time() - start_time < timeout:
            if os.path.exists(localhost_run_output_file):
                with open(localhost_run_output_file, 'r') as file:
                    content = file.read()
                    lines = content.splitlines()
                    for line in lines:
                        if "tunneled with tls termination" in line:
                            url = line.split()[-1]
                            return url
            time.sleep(1) 
        print("⏰ Timeout reached, no URL found")
        return None 
    except Exception as e:
        print(f"📝 Logging: Error starting localhost.run or getting public URL: {e}")
        return None

def run_web_server(port: int):
    public_url = get_public_url(port)
    if public_url:
        print(f"🌐 Public URL: {public_url}")
    if "SHARKHOST" in os.environ or "DOCKER" in os.environ:
        host = '0.0.0.0'
    else:
        host = '127.0.0.1'
    app.run(host=host, port=port, debug=False, use_reloader=False) 
    

async def web_auth(api_id: int, api_hash: str, device_model: str) -> Tuple[bool, Optional[User]]:
    global code_input, auth_complete, auth_result, current_step, current_phone, sent_code_hash, error_message

    code_input = None
    auth_complete = False
    auth_result = None
    current_step = "phone"
    current_phone = "+7"
    sent_code_hash = None 
    error_message = ''
 
    user_data['api_id'] = api_id
    user_data['api_hash'] = api_hash
    user_data['device_mod'] = device_model

    port = find_free_port()

    web_thread = threading.Thread(target=lambda: run_web_server(port), daemon=True)
    web_thread.start()

    client = Client(
        "my_account",
        api_id=api_id,
        api_hash=api_hash,
        device_model=device_model
    )

    try:
        await client.connect()
        
        while current_step == "phone":
            await asyncio.sleep(1) 
        
        sent_code = await client.send_code(current_phone)
        sent_code_hash = sent_code.phone_code_hash 

        current_step = "code" 

        # Цикл попыток ввода кода, пока не авторизуемся или не перейдем на ввод пароля
        while True:
            while not auth_complete:
                await asyncio.sleep(1)

            code = code_input
            if not code:
                error_message = 'Code was not entered'
                current_step = 'code'
                continue

            auth_complete = False
            code_input = None

            try:
                signed_in = await client.sign_in(current_phone, sent_code_hash, code)

                if isinstance(signed_in, User):
                    current_step = 'success'
                    error_message = ''
                    auth_result = signed_in
                    return True, signed_in

            except SessionPasswordNeeded:
                current_step = 'password'
                error_message = ''
                break  # переходим к вводу пароля
            except (PhoneCodeInvalid, PhoneCodeExpired):
                error_message = 'Invalid or expired code. Please try again.'
                current_step = 'code'
                continue
            except RPCError as e:
                logging.error(f"RPC Error on sign_in: {e}")
                error_message = 'Authorization error. Please try again.'
                current_step = 'code'
                continue

        # Ввод пароля 2FA
        while True:
            while not auth_complete:
                await asyncio.sleep(1)

            password = code_input
            auth_complete = False
            code_input = None

            if not password:
                error_message = 'Password was not entered'
                current_step = 'password'
                continue

            try:
                await client.check_password(password)
                user = await client.get_me()
                current_step = 'success'
                error_message = ''
                auth_result = user
                return True, user
            except PasswordHashInvalid:
                error_message = 'Invalid password. Please try again.'
                current_step = 'password'
                continue
            except RPCError as e:
                logging.error(f"RPC Error on check_password: {e}")
                error_message = 'Authorization error. Please try again.'
                current_step = 'password'
                continue

        signed_up = await client.sign_up(current_phone, sent_code_hash, "FoxUserbot")

        if isinstance(signed_up, TermsOfService):
            await client.accept_terms_of_service(str(signed_up.id))
        
        auth_result = signed_up
        return True, signed_up

    except RPCError as e:
        logging.error(f"RPC Error: {e}")
        auth_result = None
        current_step = "error" 
        return False, None
    except Exception as e:
        logging.error(f"Auth Error: {e}")
        auth_result = None
        current_step = "error" 
        return False, None
    finally:
        try:
            await client.disconnect()
        except:
            pass

def start_web_auth(api_id, api_hash, device_model) -> Tuple[bool, Optional[User]]:
    return asyncio.run(web_auth(api_id, api_hash, device_model)) 
