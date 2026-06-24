from flask import Flask, request, jsonify
import yt_dlp
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

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
        'socket_timeout': 30,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            title = info.get('title', 'No title')
            
            return jsonify({
                "status": "success", 
                "mp4_url": video_url,
                "title": title,
                "duration": info.get('duration')
            })
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"status": "error", "msg": str(e)}), 500

@app.route('/')
def health():
    return "yt-dlp API Running ✅"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)