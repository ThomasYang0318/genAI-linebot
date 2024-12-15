## 使用
1. .env 內密碼完善
2. 部署 render
    1. 在 Render 中，點擊 "New" > "Web Service"
    2. env 設置
        1. OPENAI_API_KEY=your_openai_api_key
        2. LINE_TOKEN=your_line_channel_access_token
        3. LINE_SECRET=your_line_channel_secret
    2. 設定 
        1. Start Command：python3 app.py
        2. Build Command：pip install -r requirements.txt