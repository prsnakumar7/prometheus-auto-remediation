from flask import Flask, request
import paramiko
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    
    if not data or 'alerts' not in data:
        logging.warning("Received invalid payload")
        return "Invalid payload", 400

    alert = data['alerts'][0]  # take the first alert
    labels = alert.get('labels', {})

    alert_name = labels.get('alertname', 'UnknownAlert')
    instance = labels.get('instance', 'UnknownInstance').split(":")[0]

    print(f"Received alert: {alert_name} from {instance}")

    if alert_name == "HighCPUUsage":
        logging.info(f"Remediating High CPU on {instance}")
        remediate_high_cpu(instance)

    return "OK", 200

def remediate_high_cpu(target_ip):
    username = "<user_name>"              # SSH user on target node
    key_file = "<path_to_your_private_key>"      # Path to your private key

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(target_ip, username=username, key_filename=key_file)
        logging.info(f"Connected to {target_ip} via SSH")

        # Command: kill the top CPU-consuming process
        cmd = """
        top -b -n1 | awk 'NR>7 {print $1,$9,$12}' | sort -k2 -nr | head -n1 | awk '{print $1}' | xargs kill -9
        """
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode()
        err = stderr.read().decode()
        if out:
            logging.info(f"Command output: {out}")
        if err:
            logging.error(f"Command error: {err}")

        ssh.close()
        logging.info(f"Remediation completed on {target_ip}")

    except Exception as e:
        logging.error(f"Failed to remediate High CPU on {target_ip}: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
