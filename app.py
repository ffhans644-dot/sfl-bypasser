from flask import Flask, render_template_string, request, jsonify
import requests
import re

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ultimate SFL Bypasser Pro</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; }
        :root {
            --bg-primary: #0f172a; --bg-secondary: #1e293b;
            --accent-blue: #0072ff; --accent-cyan: #00dfa2;
            --text-main: #f8fafc; --text-muted: #94a3b8;
            --border-color: #334155; --success-color: #10b981; --error-color: #ef4444;
        }
        body {
            background-color: var(--bg-primary); color: var(--text-main);
            min-height: 100vh; display: flex; flex-direction: column;
            align-items: center; justify-content: center; padding: 20px;
        }
        .container {
            width: 100%; max-width: 550px; background: var(--bg-secondary);
            border: 1px solid var(--border-color); border-radius: 20px;
            padding: 35px; box-shadow: 0 20px 30px rgba(0, 0, 0, 0.4);
        }
        .header { text-align: center; margin-bottom: 25px; }
        .header .logo {
            font-size: 45px; background: linear-gradient(135deg, var(--accent-blue), var(--accent-cyan));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px;
        }
        .header h1 { font-size: 22px; font-weight: 800; }
        .header p { color: var(--text-muted); font-size: 13px; margin-top: 5px; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; font-size: 12px; font-weight: 700; margin-bottom: 8px; color: var(--text-muted); text-transform: uppercase; }
        .input-wrapper { position: relative; display: flex; align-items: center; }
        .input-wrapper i { position: absolute; left: 15px; color: var(--text-muted); }
        .input-wrapper input {
            width: 100%; padding: 14px 15px 14px 45px; background: rgba(15, 23, 42, 0.7);
            border: 1px solid var(--border-color); border-radius: 12px; color: var(--text-main); font-size: 14px;
        }
        .input-wrapper input:focus { outline: none; border-color: var(--accent-blue); box-shadow: 0 0 0 3px rgba(0, 114, 255, 0.2); }
        .btn-bypass {
            width: 100%; padding: 14px; background: linear-gradient(135deg, var(--accent-blue), var(--accent-cyan));
            border: none; border-radius: 12px; color: white; font-size: 15px; font-weight: 700; cursor: pointer;
            display: flex; align-items: center; justify-content: center; gap: 8px; margin-top: 10px;
            box-shadow: 0 4px 12px rgba(0, 114, 255, 0.3); transition: transform 0.2s;
        }
        .btn-bypass:hover { transform: translateY(-2px); }
        .loading-box { display: none; text-align: center; margin-top: 15px; color: var(--text-muted); font-size: 13px; }
        .error-box {
            margin-top: 15px; color: var(--error-color); font-size: 13px; text-align: center; display: none;
            background: rgba(239, 68, 68, 0.1); padding: 10px; border-radius: 8px; border: 1px solid rgba(239, 68, 68, 0.3);
        }
        .result-box {
            margin-top: 25px; background: rgba(0, 223, 162, 0.08); border: 1px solid var(--accent-cyan);
            border-radius: 12px; padding: 20px; display: none;
        }
        .result-box.active { display: block; }
        .result-box h3 { font-size: 13px; color: var(--accent-cyan); margin-bottom: 10px; display: flex; align-items: center; gap: 6px; }
        .result-input-group { display: flex; gap: 10px; }
        .result-input-group input {
            flex: 1; padding: 10px; background: var(--bg-primary); border: 1px solid var(--border-color);
            border-radius: 8px; color: var(--accent-cyan); font-weight: 600; font-size: 13px;
        }
        .btn-copy { padding: 0 15px; background: var(--accent-cyan); border: none; border-radius: 8px; color: #0f172a; font-weight: 700; cursor: pointer; }
        .btn-open {
            margin-top: 10px; width: 100%; padding: 10px; background: var(--success-color); border: none;
            border-radius: 8px; color: white; font-weight: 700; text-decoration: none; display: block; text-align: center; font-size: 13px;
        }
        .footer { margin-top: 20px; font-size: 12px; color: var(--text-muted); text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo"><i class="fa-solid fa-unlock-keyhole"></i></div>
            <h1>Ultimate SFL Bypasser</h1>
            <p>Khusus Mediafire & Sfile.co</p>
        </div>
        <div class="form-group">
            <label for="sflUrl">Link Safelink / SFL</label>
            <div class="input-wrapper">
                <i class="fa-solid fa-link"></i>
                <input type="url" id="sflUrl" placeholder="https://sfl.gl/..." required>
            </div>
        </div>
        <button class="btn-bypass" onclick="bypassLink()"><i class="fa-solid fa-wand-magic-sparkles"></i> Bypass Link Sekarang</button>
        <div class="loading-box" id="loadingBox"><i class="fa-solid fa-spinner fa-spin"></i> Membongkar enkripsi & melacak link...</div>
        <div class="error-box" id="errorBox"></div>
        <div class="result-box" id="resultBox">
            <h3><i class="fa-solid fa-circle-check"></i> Link File Asli Ditemukan:</h3>
            <div class="result-input-group">
                <input type="text" id="targetResult" readonly>
                <button class="btn-copy" onclick="copyLink()"><i class="fa-solid fa-copy"></i> Salin</button>
            </div>
            <a href="#" id="openLinkBtn" target="_blank" class="btn-open"><i class="fa-solid fa-arrow-up-right-from-square"></i> Buka File Tujuan</a>
        </div>
    </div>
    <div class="footer">CodingXOndev Engine &copy; 2026</div>

    <script>
        async function bypassLink() {
            const urlInput = document.getElementById('sflUrl').value.trim();
            const resultBox = document.getElementById('resultBox');
            const loadingBox = document.getElementById('loadingBox');
            const errorBox = document.getElementById('errorBox');
            const targetResult = document.getElementById('targetResult');
            const openLinkBtn = document.getElementById('openLinkBtn');

            if (!urlInput) { alert('Masukkan link SFL dulu bos!'); return; }

            resultBox.classList.remove('active');
            errorBox.style.display = 'none';
            loadingBox.style.display = 'block';

            try {
                const response = await fetch('/api/bypass', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: urlInput })
                });
                const data = await response.json();
                loadingBox.style.display = 'none';

                if (data.success) {
                    targetResult.value = data.targetUrl;
                    openLinkBtn.href = data.targetUrl;
                    resultBox.classList.add('active');
                } else {
                    errorBox.innerText = data.message || 'Gagal generate link!';
                    errorBox.style.display = 'block';
                }
            } catch (err) {
                loadingBox.style.display = 'none';
                errorBox.innerText = 'Kesalahan koneksi server.';
                errorBox.style.display = 'block';
            }
        }
        function copyLink() {
            const res = document.getElementById('targetResult');
            res.select();
            navigator.clipboard.writeText(res.value);
            alert('Berhasil disalin, bos!');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/bypass', methods=['POST'])
def api_bypass():
    data = request.get_json()
    target_url = data.get('url', '').strip()

    if not target_url.startswith(('http://', 'https://')):
        return jsonify({'success': False, 'message': 'Format URL harus pakai http:// atau https://'})

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        
        session = requests.Session()
        response = session.get(target_url, headers=headers, allow_redirects=True, timeout=20)
        
        final_url = response.url
        html_content = response.text

        found_url = ""

        # 1. Cek langsung dari URL akhir redirect
        if 'mediafire.com' in final_url or 'sfile.co' in final_url:
            found_url = final_url
        else:
            # 2. Cari pola tautan sfile.co atau mediafire di dalam seluruh teks HTML / skrip JS halaman
            matches = re.findall(r'https?://(?:www\.)?(?:sfile\.co|mediafire\.com)/[^\s"\'<>]+', html_content)
            if matches:
                found_url = matches[0]
            else:
                # 3. Cari di dalam tag <form action="..."> atau hidden input
                form_actions = re.findall(r'action=["\']([^"\']+)["\']', html_content)
                for action in form_actions:
                    if 'sfile.co' in action or 'mediafire.com' in action:
                        found_url = action
                        break
                
                # 4. Cari alternatif tag href biasa
                if not found_url:
                    all_links = re.findall(r'href=["\']([^"\']+)["\']', html_content)
                    for l in all_links:
                        if 'sfile.co' in l or 'mediafire.com' in l:
                            found_url = l
                            break

        if found_url:
            # Bersihkan karakter penutup aneh jika tertangkap regex
            found_url = found_url.rstrip('\'").')
            return jsonify({'success': True, 'targetUrl': found_url})
        else:
            return jsonify({'success': False, 'message': 'Gagal! Link Mediafire atau sfile.co terkunci di dalam tombol verifikasi SFL.'})

    except Exception as e:
        return jsonify({'success': False, 'message': 'Koneksi timeout atau link SFL tidak dapat dijangkau.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
