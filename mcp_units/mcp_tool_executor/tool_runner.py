import subprocess

def run_shell_command(command):
    if not command.strip():
        return "Kein Befehl eingegeben."
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        return f"Fehler:\n{e.output.strip()}"