from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

# Cookies file ka content env variable se lo
cookies_content = os.environ.get('IG_COOKIES', '')
if cookies_content:
    with open('/tmp/cookies.txt', 'w') as f:
        f.write(cookies_content)

@app.route('/api')
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"status": "error", "msg": "url missing"}), 400
    
    ydl_opts = {
        'format': 'mp4/best[height<=720]/best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'cookiefile': '/tmp/cookies.txt' if cookies_content else None,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "status": "success", 
                "mp4_url": info['url'],
                "title": info.get('title', '')
            })
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)