from flask import Flask, render_template
import subprocess
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)


def ping(ip):
    proc = subprocess.Popen(['ping', '-n', '1', ip], stdout=subprocess.PIPE)
    output, error = proc.communicate()
    if b'Reply from' in output:
        return ('green', ip, 'Success')
    else:
        return ('red', ip, 'Failure')


@app.route('/')
def index():
    with open('ips.txt', 'r') as f:
        ips = [line.strip() for line in f.readlines()]
    ipsVal = len(ips)
    results = []
    with ThreadPoolExecutor(
            max_workers=5) as executor:  # max_workers değeri ile aynı anda çalışacak işlem sayısını belirleyebilirsiniz.
        for result in executor.map(ping, ips):
            results.append(result)

    ping_success = len([r for r in results if r[0] == 'green'])
    ping_failure = len([r for r in results if r[0] == 'red'])

    return render_template('index.html', results=results, ping_success=ping_success, ping_failure=ping_failure,
                           ipsVal=ipsVal)

if __name__ == '__main__':
    app.run(debug=True)
