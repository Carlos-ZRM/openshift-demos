import subprocess
import ipaddress
import os
import re
from urllib.parse import urlparse
from flask import Flask, request, render_template_string

# Initialize the Flask application
app = Flask(__name__)

# --- Helper Functions for Validation ---
def is_valid_hostname(hostname):
    """
    Validates if the given string is a valid FQDN.
    """
    if not hostname or len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1] # strip trailing dot
    allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))

def is_valid_url(url):
    """
    Validates if a string is or can be a valid HTTP/HTTPS URL (e.g., host:port).
    Returns a tuple: (bool, processed_url_or_None).
    """
    if not isinstance(url, str) or not url:
        return False, None

    # Prepend a default scheme if one is missing to handle host:port cases.
    if "://" not in url:
        url = "http://" + url

    try:
        result = urlparse(url)
        # Check that we have a valid scheme and a network location.
        if result.scheme in ['http', 'https'] and result.netloc:
            return True, url  # Return True and the processed URL
        else:
            return False, None
    except ValueError:
        return False, None

# HTML template with embedded CSS and JS for a tabbed interface.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Network Tools</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&family=Roboto:wght@400;500&display=swap');

        :root {
            --bg-color: #1a1b26;
            --fg-color: #a9b1d6;
            --card-color: #24283b;
            --border-color: #414868;
            --accent-color: #7aa2f7;
            --success-color: #9ece6a;
            --error-color: #f7768e;
            --input-bg: #2f3549;
            --info-color: #c0caf5;
        }

        body {
            font-family: 'Roboto', sans-serif;
            background-color: var(--bg-color);
            color: var(--fg-color);
            margin: 0;
            padding: 2rem;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            min-height: 100vh;
        }

        .container {
            width: 100%;
            max-width: 800px;
            background-color: var(--card-color);
            border-radius: 12px;
            border: 1px solid var(--border-color);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            padding: 2rem;
            box-sizing: border-box;
        }
        
        .k8s-info {
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 2rem;
            background-color: var(--input-bg);
        }

        .k8s-info h2 {
            margin-top: 0;
            color: var(--accent-color);
            font-size: 1.2rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 0.5rem 1rem;
            font-family: 'Fira Code', monospace;
            font-size: 0.9rem;
        }
        
        .info-grid div {
            color: var(--info-color);
            word-break: break-all;
        }

        .info-grid span {
            font-weight: bold;
            color: var(--fg-color);
        }

        .tab-nav {
            display: flex;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 1.5rem;
        }

        .tab-button {
            padding: 0.75rem 1.5rem;
            cursor: pointer;
            border: none;
            background-color: transparent;
            color: var(--fg-color);
            font-size: 1rem;
            font-weight: 500;
            border-bottom: 3px solid transparent;
            transition: color 0.3s, border-color 0.3s;
        }

        .tab-button.active {
            color: var(--accent-color);
            border-bottom: 3px solid var(--accent-color);
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }

        .form-group {
            display: flex;
            flex-direction: column;
        }
        
        .form-group-full {
             grid-column: 1 / -1;
        }

        label {
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        p.help-text {
            font-size: 0.8rem;
            color: var(--info-color);
            margin-top: 0.5rem;
            font-family: 'Fira Code', monospace;
        }

        input, select {
            background-color: var(--input-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.75rem;
            color: var(--fg-color);
            font-family: 'Fira Code', monospace;
            font-size: 1rem;
            transition: border-color 0.3s, box-shadow 0.3s;
        }

        input:focus, select:focus {
            outline: none;
            border-color: var(--accent-color);
            box-shadow: 0 0 0 3px rgba(122, 162, 247, 0.3);
        }

        .execute-button {
            width: 100%;
            background-color: var(--accent-color);
            color: var(--card-color);
            font-size: 1.1rem;
            font-weight: bold;
            padding: 0.8rem;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.2s;
            margin-top: 1rem;
        }

        .execute-button:hover {
            background-color: #9abdfa;
            transform: translateY(-2px);
        }

        .result-box {
            margin-top: 2rem;
        }

        .result-box h2 {
            color: var(--fg-color);
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
        }
        
        .result-output {
            background-color: var(--bg-color);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.5rem;
            font-family: 'Fira Code', monospace;
            white-space: pre-wrap;
            word-wrap: break-word;
            min-height: 50px;
            max-height: 400px;
            overflow-y: auto;
            color: var(--fg-color);
        }
        
        .result-output.success {
            color: var(--success-color);
        }

        .result-output.error {
            color: var(--error-color);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="k8s-info">
            <h2>Kubernetes Pod Info</h2>
            <div class="info-grid">
                <div>Pod Name: <span>{{ k8s_info.pod_name }}</span></div>
                <div>Namespace: <span>{{ k8s_info.pod_namespace }}</span></div>
                <div>Service Name: <span>{{ k8s_info.service_name }}</span></div>
                <div>App Label: <span>{{ k8s_info.app_label }}</span></div>
            </div>
        </div>

        <div class="tab-nav">
            <button class="tab-button {% if active_tab == 'netcat' %}active{% endif %}" onclick="openTab(event, 'netcat')">Netcat</button>
            <button class="tab-button {% if active_tab == 'curl' %}active{% endif %}" onclick="openTab(event, 'curl')">Curl</button>
        </div>

        <!-- Netcat Tab -->
        <div id="netcat" class="tab-content {% if active_tab == 'netcat' %}active{% endif %}">
            <form method="post">
                <div class="form-grid">
                    <div class="form-group">
                        <label for="host">IP Address or FQDN</label>
                        <input type="text" id="host" name="host" value="{{ form_data.host or '' }}" required placeholder="e.g., google.com">
                    </div>
                    <div class="form-group">
                        <label for="port">Port</label>
                        <input type="number" id="port" name="port" value="{{ form_data.port or '' }}" required min="1" max="65535" placeholder="e.g., 443">
                    </div>
                    <div class="form-group">
                        <label for="protocol">Protocol</label>
                        <select id="protocol" name="protocol">
                            <option value="tcp" {% if form_data.protocol == 'tcp' %}selected{% endif %}>TCP</option>
                            <option value="udp" {% if form_data.protocol == 'udp' %}selected{% endif %}>UDP</option>
                        </select>
                    </div>
                </div>
                <button type="submit" name="submit_netcat" class="execute-button">Execute Netcat</button>
            </form>
        </div>

        <!-- Curl Tab -->
        <div id="curl" class="tab-content {% if active_tab == 'curl' %}active{% endif %}">
            <form method="post">
                <div class="form-grid">
                    <div class="form-group form-group-full">
                        <label for="url">URL</label>
                        <input type="text" id="url" name="url" value="{{ form_data.url or '' }}" required placeholder="https://example.com or my-service:8080">
                    </div>
                    <div class="form-group form-group-full">
                        <label for="curl_flags">Additional Flags</label>
                        <input type="text" id="curl_flags" name="curl_flags" value="{{ form_data.curl_flags or '' }}" placeholder="-v -I">
                        <p class="help-text">Allowed flags: -v, -i, -I, --verbose, --include, --head</p>
                    </div>
                </div>
                <button type="submit" name="submit_curl" class="execute-button">Execute Curl</button>
            </form>
        </div>
        
        {% if result is not none %}
        <div class="result-box">
            <h2>Result</h2>
            <pre class="result-output {{ 'error' if error else 'success' }}">{{ result }}</pre>
        </div>
        {% endif %}
    </div>

    <script>
        function openTab(evt, tabName) {
            var i, tabcontent, tabbuttons;
            tabcontent = document.getElementsByClassName("tab-content");
            for (i = 0; i < tabcontent.length; i++) {
                tabcontent[i].style.display = "none";
            }
            tabbuttons = document.getElementsByClassName("tab-button");
            for (i = 0; i < tabbuttons.length; i++) {
                tabbuttons[i].className = tabbuttons[i].className.replace(" active", "");
            }
            document.getElementById(tabName).style.display = "block";
            evt.currentTarget.className += " active";
        }
        // Ensure the active tab is shown on page load if it exists
        if (document.querySelector('.tab-button.active')) {
            document.querySelector('.tab-button.active').click();
        }
    </script>
</body>
</html>
"""

def get_k8s_info():
    """
    Retrieves Kubernetes metadata from environment variables.
    """
    return {
        'pod_name': os.getenv('POD_NAME', 'N/A'),
        'pod_namespace': os.getenv('POD_NAMESPACE', 'N/A'),
        'service_name': os.getenv('SERVICE_NAME', 'N/A'),
        'app_label': os.getenv('APP_LABEL', 'N/A')
    }

def handle_netcat_request(form_data):
    """Handles the logic for a netcat request."""
    host = form_data.get("host")
    port_str = form_data.get("port")
    protocol = form_data.get("protocol")
    
    # Validation
    is_valid_ip = False
    try:
        if host: ipaddress.ip_address(host)
        is_valid_ip = True
    except ValueError: pass

    if not is_valid_ip and not is_valid_hostname(host):
        return f"Error: Invalid IP address or FQDN provided: {host}", True

    try:
        port = int(port_str)
        if not 1 <= port <= 65535: raise ValueError
    except (ValueError, TypeError):
        return f"Error: Invalid port number: {port_str}. Must be 1-65535.", True

    # Execution
    try:
        command = ["nc", "-v", "-z"]
        if protocol == "udp": command.append("-u")
        command.extend([host, str(port)])

        process = subprocess.run(command, capture_output=True, text=True, timeout=10, check=False)
        return process.stdout + process.stderr, process.returncode != 0
    except FileNotFoundError:
        return "Error: 'nc' (netcat) command not found on the server.", True
    except subprocess.TimeoutExpired:
        return f"Error: Command timed out after 10s. Host {host}:{port} may be unresponsive.", True
    except Exception as e:
        return f"An unexpected error occurred: {e}", True

def handle_curl_request(form_data):
    """
    Handles the logic for a curl request.
    """
    url = form_data.get("url")
    curl_flags = form_data.get("curl_flags", "")

    # --- Validation ---
    is_valid, processed_url = is_valid_url(url)
    if not is_valid:
        return f"Error: Invalid or insecure URL provided: {url}. Must be a full URL or host:port.", True

    # Flag Validation (Security)
    ALLOWED_CURL_FLAGS = {'-v', '--verbose', '-i', '--include', '-I', '--head'}
    user_flags = curl_flags.strip().split()
    for flag in user_flags:
        if flag not in ALLOWED_CURL_FLAGS:
            return f"Error: Disallowed or invalid curl flag used: '{flag}'.", True

    # --- Execution ---
    try:
        # Base command. -sS: Silent mode but show errors. -L: follow redirects. -m: max time.
        command = ["curl", "-sSL", "-m", "5"]
        # Add validated user flags
        command.extend(user_flags)
        # Add the URL at the end
        command.append(processed_url)
        
        process = subprocess.run(command, capture_output=True, text=True, check=False)
        
        output = process.stdout
        if process.returncode != 0:
            output = process.stderr + output

        return output, process.returncode != 0
    except FileNotFoundError:
        return "Error: 'curl' command not found on the server.", True
    except subprocess.TimeoutExpired:
        return f"Error: Subprocess timed out. The request to {url} took too long.", True
    except Exception as e:
        return f"An unexpected error occurred: {e}", True

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Main route to display the forms and handle submissions.
    """
    k8s_info = get_k8s_info()
    active_tab = 'netcat'
    result = None
    error = False
    form_data = {}

    if request.method == "POST":
        form_data = request.form.to_dict()
        if 'submit_netcat' in request.form:
            active_tab = 'netcat'
            result, error = handle_netcat_request(form_data)
        elif 'submit_curl' in request.form:
            active_tab = 'curl'
            result, error = handle_curl_request(form_data)

    return render_template_string(HTML_TEMPLATE, 
                                  k8s_info=k8s_info,
                                  active_tab=active_tab,
                                  result=result,
                                  error=error,
                                  form_data=form_data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
