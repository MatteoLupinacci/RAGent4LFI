from flask import Flask, request, jsonify # type: ignore
import subprocess
import re

#============================================ API settings on Kali Linux ============================================
app = Flask(__name__)

@app.route('/find_path_with_gobuster', methods=['POST'])
def find_path_with_gobuster():
    target_url = request.json.get('target_url')
    wordlist = "/usr/share/seclists/Discovery/Web-Content/common.txt"  # Path to the wordlist
    command = f"gobuster dir -u {target_url} -w {wordlist}"
    print(f"Executing: {command}")
    
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        valid_paths = []
        
        for line in process.stdout:
            clean_line = ansi_escape.sub('', line).strip()  
            if "(Status: 200)" in clean_line:
                valid_paths.append("".join(clean_line.split()[0]))  

        process.wait() 
        print("\nValid paths found:", valid_paths)
        return jsonify({"paths": valid_paths, "status": "success"})
    
    except subprocess.TimeoutExpired:
        return RuntimeError({"error": "Timeout during paths fuzzing.", "status": "failure"})


@app.route('/find_query_params_with_wfuzz', methods=['POST'])
def find_query_params_with_wfuzz():
    target_url = request.json.get('target_url')
    payload = request.json.get('payload')
    wordlist = "/usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt"
    command = f"wfuzz -w {wordlist} --hc 404 --sc 200 {target_url}?FUZZ={payload}"
    print(f"Executing: {command}\n")
    
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        valid_params = []
        
        for line in process.stdout:
            clean_line = ansi_escape.sub('', line).strip()  
            if "200" in clean_line:
                match = re.match(r'\d+:\s+200\s+(\d+)\s+L\s+(\d+)\s+W\s+(\d+)\s+Ch\s+"([^"]+)"', clean_line)
                if match:
                    length = int(match.group(1))
                    word_count = int(match.group(2))
                    char_count = int(match.group(3))
                    payload = match.group(4)
                    if length > 0 or word_count > 0 or char_count > 0:
                        valid_params.append(payload)

        process.wait()
        print("\nValid query params found:", valid_params)
        return jsonify({"params": valid_params, "status": "success"})
    
    except subprocess.TimeoutExpired:
        return RuntimeError({"error": "Timeout during paths fuzzing.", "status": "failure"})


@app.route('/execute_command', methods=['POST'])
def execute_command():
    command = request.json.get('command')
    print(f"Executing: {command}")

    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.stdout:
            clean_line = ansi_escape.sub('', result.stdout).strip()  
            print("\nCommand output:", clean_line)
            return jsonify({"output": clean_line, "status": "success"})
        clean_line = ansi_escape.sub('', result.stderr).strip()  
        print("\nCommand output:", clean_line)
        return jsonify({"output": clean_line, "status": "error"})
    except Exception as e:
        return f"Error during command execution: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
