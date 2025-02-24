from flask import Flask, request, jsonify
import subprocess
import re

app = Flask(__name__)

@app.route('/find_path_with_gobuster', methods=['POST'])
def find_path_with_gobuster():
    target_url = request.json.get('target_url')
    wordlist = "/usr/share/seclists/Discovery/Web-Content/common.txt"  # Path alla wordlist
    command = f"gobuster dir -u {target_url} -w {wordlist}"
    print(f"Executing: {command}\n")
    
    # Regex per rimuovere caratteri ANSI (es. colori e sequenze di controllo)
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        valid_paths = []
        
        # Legge l'output riga per riga in tempo reale
        for line in process.stdout:
            clean_line = ansi_escape.sub('', line).strip()  
            #print(clean_line)
            
            if "(Status: 200)" in clean_line:
                valid_paths.append(clean_line.split()[0])  # Prende solo il path

        process.wait()  # Aspetta la fine del processo
        print("\nValid paths found:", valid_paths)
        return jsonify({"paths": valid_paths, "status": "success"})
    
    except subprocess.TimeoutExpired:
        return RuntimeError({"error": "Timeout during paths fuzzing.", "status": "failure"})


@app.route('/find_query_params_with_wfuzz', methods=['POST'])
def find_query_params_with_wfuzz():
    target_url = request.json.get('target_url')
    payload = request.json.get('payload')
    wordlist = "/usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt"  # Path alla wordlist
    command = f"wfuzz -w {wordlist} --hc 404 --hw 0 {target_url}?FUZZ={payload}"
    print(f"Executing: {command}\n")
    
    # Regex per rimuovere caratteri ANSI (es. colori e sequenze di controllo)
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        valid_params = []
        
        # Legge l'output riga per riga in tempo reale
        for line in process.stdout:
            clean_line = ansi_escape.sub('', line).strip()  
            #print(clean_line)
            
            if "(Status: 200)" in clean_line:
                valid_params.append(clean_line.split()[0])  # Prende solo il path

        process.wait()  # Aspetta la fine del processo
        print("\nValid query params found:", valid_params)
        return jsonify({"params": valid_params, "status": "success"})
    
    except subprocess.TimeoutExpired:
        return RuntimeError({"error": "Timeout during paths fuzzing.", "status": "failure"})
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
