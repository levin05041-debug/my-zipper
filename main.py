from flask import Flask, request
import os
import zipfile
import requests
import yt_dlp

app = Flask(__name__)

@app.route('/download')
def download_video():
    video_url = request.args.get('url')
    if not video_url:
        return "Please provide a youtube URL", 400

    temp_video = 'v.mp4'                 
    zip_filename = 'v.zip'                  

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': temp_video,
        'nocheckcertificate': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        if not os.path.exists(temp_video) and os.path.exists(temp_video + '.mp4'):
            temp_video += '.mp4'
            
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(temp_video, 'video.mp4')

        api_url = "https://tmpfiles.org/api/v1/upload"
        with open(zip_filename, 'rb') as f:
            files = {'file': f}
            response = requests.post(api_url, files=files)
        
        if response.status_code == 200:
            return response.json().get('data', {}).get('url')
        else:
            return "Upload Error to tmpfiles", 500

    except Exception as e:
        return f"Error: {str(e)}", 500

    finally:
        if os.path.exists(temp_video): os.remove(temp_video)
        if os.path.exists(zip_filename): os.remove(zip_filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
