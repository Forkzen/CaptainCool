import sys

with open("/Users/abhisar/Desktop/Project/index.html", "r") as f:
    lines = f.readlines()

new_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Captain Cool - Minimalist Sports HUD</title>
  <link href="https://fonts.googleapis.com/css2?family=Teko:wght@400;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0a0a0a;
      --surface: rgba(255, 255, 255, 0.03);
      --border: rgba(255, 255, 255, 0.1);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      
      /* Accents */
      --dhoni: #eab308;
      --kohli: #ef4444;
      --rohit: #3b82f6;
      --gambhir: #a855f7;
      
      --font-sports: "Teko", sans-serif;
      --font-body: "Inter", sans-serif;
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
      background-color: var(--bg);
      color: var(--text-main);
      font-family: var(--font-body);
      height: 100vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      background-image: 
        linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
      background-size: 50px 50px;
    }

    h1, h2, h3, .sports-text {
      font-family: var(--font-sports);
      text-transform: uppercase;
      letter-spacing: 1px;
    }

    /* Modal */
    #api-modal {
      position: fixed; inset: 0; background: rgba(0,0,0,0.9);
      backdrop-filter: blur(5px); display: flex; justify-content: center; align-items: center; z-index: 1000;
    }
    .modal-content {
      background: var(--bg); border: 1px solid var(--border);
      padding: 2.5rem; border-radius: 8px; text-align: center; width: 90%; max-width: 400px;
      animation: slideUp 0.4s ease;
    }
    .modal-content h2 { font-size: 2.5rem; color: #fff; margin-bottom: 0.5rem; }
    .modal-content p { color: var(--text-muted); margin-bottom: 1.5rem; }
    .modal-content input {
      width: 100%; padding: 12px; margin-bottom: 1.5rem;
      background: rgba(255,255,255,0.05); border: 1px solid var(--border); color: #fff;
      font-family: var(--font-body); border-radius: 4px; outline: none;
    }
    .modal-content input:focus { border-color: var(--text-main); }
    .modal-content button {
      background: #fff; color: #000; border: none; padding: 12px 24px;
      font-family: var(--font-sports); font-size: 1.5rem; width: 100%; cursor: pointer; border-radius: 4px; transition: 0.2s;
    }
    .modal-content button:hover { background: #e2e8f0; }

    /* Header */
    header {
      height: 60px; border-bottom: 1px solid var(--border); background: var(--bg);
      display: flex; justify-content: space-between; align-items: center; padding: 0 24px; z-index: 10;
    }
    .brand { display: flex; align-items: center; gap: 15px; }
    .live-indicator {
      display: flex; align-items: center; gap: 8px; color: var(--text-muted); font-family: var(--font-sports); font-size: 1.2rem;
    }
    .live-dot { width: 8px; height: 8px; background: #ef4444; border-radius: 50%; animation: blink 1.5s infinite; }
    header h1 { font-size: 2rem; color: #fff; }
    
    #compare-toggle-btn {
      background: transparent; border: 1px solid var(--border); color: #fff;
      padding: 6px 16px; font-family: var(--font-sports); font-size: 1.2rem; cursor: pointer; border-radius: 4px; transition: 0.2s;
    }
    #compare-toggle-btn:hover { background: rgba(255,255,255,0.1); }

    /* Layout */
    .main-container {
      display: grid; grid-template-columns: 320px 1fr; gap: 20px; padding: 20px;
      flex: 1; overflow: hidden; height: calc(100vh - 100px); /* 60px header + 40px footer */
    }

    /* Left Panel */
    .control-panel {
      display: flex; flex-direction: column; gap: 15px; overflow-y: auto;
    }
    
    .panel-box {
      background: var(--surface); border: 1px solid var(--border); padding: 16px; border-radius: 8px;
    }
    .panel-title { font-family: var(--font-sports); font-size: 1.5rem; color: #fff; margin-bottom: 12px; border-bottom: 1px solid var(--border); padding-bottom: 4px;}

    /* Captains */
    .captains { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
    .captain-card {
      background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-radius: 6px;
      padding: 12px 8px; text-align: center; cursor: pointer; transition: all 0.3s ease;
    }
    .captain-card .emoji { font-size: 1.8rem; margin-bottom: 4px; display: block; }
    .captain-card .name { font-family: var(--font-sports); font-size: 1.3rem; letter-spacing: 1px; color: var(--text-muted); }
    
    .captain-card:hover { transform: translateY(-2px); background: rgba(255,255,255,0.05); }
    .captain-card[data-id="dhoni"].active { border-color: var(--dhoni); box-shadow: 0 0 15px rgba(234, 179, 8, 0.2); }
    .captain-card[data-id="dhoni"].active .name { color: var(--dhoni); }
    .captain-card[data-id="kohli"].active { border-color: var(--kohli); box-shadow: 0 0 15px rgba(239, 68, 68, 0.2); }
    .captain-card[data-id="kohli"].active .name { color: var(--kohli); }
    .captain-card[data-id="rohit"].active { border-color: var(--rohit); box-shadow: 0 0 15px rgba(59, 130, 246, 0.2); }
    .captain-card[data-id="rohit"].active .name { color: var(--rohit); }
    .captain-card[data-id="gambhir"].active { border-color: var(--gambhir); box-shadow: 0 0 15px rgba(168, 85, 247, 0.2); }
    .captain-card[data-id="gambhir"].active .name { color: var(--gambhir); }

    /* Input */
    textarea {
      width: 100%; height: 80px; background: rgba(0,0,0,0.5); border: 1px solid var(--border);
      color: #fff; padding: 10px; font-family: var(--font-body); font-size: 0.9rem;
      border-radius: 4px; outline: none; resize: none; margin-bottom: 10px;
    }
    textarea:focus { border-color: #fff; }
    
    .btn-row { display: flex; gap: 8px; }
    .btn {
      flex: 1; padding: 8px; font-family: var(--font-sports); font-size: 1.2rem; cursor: pointer; border-radius: 4px; transition: 0.2s; border: none;
    }
    .btn-secondary { background: rgba(255,255,255,0.1); color: #fff; }
    .btn-secondary:hover { background: rgba(255,255,255,0.2); }
    .btn-primary { background: #fff; color: #000; }
    .btn-primary:hover { background: #e2e8f0; }

    /* Pressure Meter */
    .pressure-meter { padding: 15px 0; }
    .pressure-label { display: flex; justify-content: space-between; font-family: var(--font-sports); font-size: 1.3rem; margin-bottom: 8px; }
    .pressure-track { height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; overflow: hidden; }
    .pressure-fill { height: 100%; width: 0%; background: #fff; transition: width 1s ease, background 0.5s ease; }

    /* War Room */
    #war-room-toggle { font-family: var(--font-sports); font-size: 1.2rem; color: var(--text-muted); cursor: pointer; text-align: center; padding-top: 10px; transition: 0.2s; }
    #war-room-toggle:hover { color: #fff; }
    #war-room-content {
      margin-top: 10px; font-family: monospace; font-size: 0.75rem; color: #10b981;
      background: #000; padding: 10px; border-radius: 4px; overflow-y: auto; max-height: 150px; display: none;
    }

    /* Center Arena */
    .arena { position: relative; display: flex; flex-direction: column; overflow: hidden; }
    .transcript { flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; padding-bottom: 100px; padding-right: 10px; }
    
    .chat-msg {
      background: var(--surface); border: 1px solid var(--border); padding: 16px; border-radius: 8px;
      animation: slideUpFade 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards; opacity: 0; transform: translateY(20px);
      max-width: 85%;
    }
    .chat-msg.strategist { border-left: 4px solid var(--dhoni); align-self: flex-start; }
    .chat-msg.advocate { border-right: 4px solid var(--text-muted); align-self: flex-end; text-align: right; }
    
    /* Dynamically inject active captain color via inline style in JS, but for default/fallback: */
    
    .chat-msg .author { font-family: var(--font-sports); font-size: 1.4rem; margin-bottom: 4px; display: flex; align-items: center; gap: 8px; }
    .chat-msg.advocate .author { justify-content: flex-end; color: var(--text-muted); }
    .chat-msg .content { font-size: 0.95rem; line-height: 1.5; color: var(--text-main); }
    
    .confidence-score {
      font-family: var(--font-sports); font-size: 1.2rem; padding: 2px 8px; border-radius: 4px; background: rgba(255,255,255,0.1); margin-left: auto;
    }
    .counterfactual { margin-top: 10px; font-size: 0.85rem; color: #ef4444; font-style: italic; border-top: 1px solid var(--border); padding-top: 8px; }

    /* Lower Third (Commentator) */
    .lower-third {
      position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%);
      width: 90%; background: rgba(0,0,0,0.85); border: 1px solid var(--border); border-left: 4px solid #fff;
      padding: 16px 24px; border-radius: 8px; backdrop-filter: blur(10px);
      box-shadow: 0 10px 30px rgba(0,0,0,0.5); z-index: 5;
    }
    .lower-third h3 { color: var(--text-muted); font-size: 1.2rem; margin-bottom: 4px; }
    .lower-third p { font-size: 1rem; line-height: 1.4; color: #fff; font-weight: 500; }

    /* Compare Mode */
    .compare-grid { display: none; grid-template-columns: 1fr 1fr; gap: 15px; height: 100%; overflow: hidden; }
    .compare-col {
      background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 15px;
      display: flex; flex-direction: column; overflow-y: auto;
    }
    .compare-col h3 { text-align: center; font-size: 1.8rem; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid var(--border); }
    
    /* Dynamic Compare Headers */
    #col-dhoni h3 { color: var(--dhoni); }
    #col-kohli h3 { color: var(--kohli); }
    #col-rohit h3 { color: var(--rohit); }
    #col-gambhir h3 { color: var(--gambhir); }

    /* Bottom Ticker (Whispers) */
    footer {
      height: 40px; background: #000; border-top: 1px solid var(--border); display: flex; align-items: center; overflow: hidden;
    }
    .ticker-label {
      background: #fff; color: #000; font-family: var(--font-sports); font-size: 1.2rem; padding: 0 15px; height: 100%;
      display: flex; align-items: center; z-index: 2; border-right: 1px solid #333;
    }
    .ticker-wrapper { flex: 1; overflow: hidden; white-space: nowrap; position: relative; display: flex; align-items: center; }
    
    .whisper-card { display: inline-block; padding: 0 20px; font-family: monospace; font-size: 0.9rem; color: var(--text-muted); border-right: 1px solid #333; }
    .whisper-card strong { color: #fff; }
    
    #whisper-feed {
      display: inline-block; white-space: nowrap; animation: ticker 25s linear infinite;
    }

    #loader {
      position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
      font-family: var(--font-sports); font-size: 2rem; color: #fff; display: none; letter-spacing: 2px;
      animation: blink 1s infinite;
    }

    /* Scrollbars */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 3px; }

    @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes slideUpFade { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
    @keyframes ticker { 0% { transform: translateX(100vw); } 100% { transform: translateX(-100%); } }

  </style>
</head>

<body>

  <div id="api-modal">
    <div class="modal-content">
      <h2 class="sports-text">SYSTEM INITIALIZATION</h2>
      <p>Enter Gemini API Key to establish secure uplink.</p>
      <input type="password" id="api-key-input" placeholder="AIzaSy...">
      <button id="save-key-btn">CONNECT</button>
    </div>
  </div>

  <header>
    <div class="brand">
      <div class="live-indicator"><div class="live-dot"></div> ON AIR</div>
      <h1>CAPTAINS HUD</h1>
    </div>
    <div class="header-controls">
      <button id="compare-toggle-btn">COMPARE MODE</button>
    </div>
  </header>

  <div class="main-container">
    
    <!-- Left Panel -->
    <div class="control-panel">
      
      <div class="panel-box">
        <h2 class="panel-title">SELECT TACTICIAN</h2>
        <div class="captains" id="captain-selector">
          <div class="captain-card active" data-id="dhoni">
            <span class="emoji">🧊</span><span class="name">DHONI</span>
          </div>
          <div class="captain-card" data-id="kohli">
            <span class="emoji">🔥</span><span class="name">KOHLI</span>
          </div>
          <div class="captain-card" data-id="rohit">
            <span class="emoji">🌊</span><span class="name">ROHIT</span>
          </div>
          <div class="captain-card" data-id="gambhir">
            <span class="emoji">⚔️</span><span class="name">GAMBHIR</span>
          </div>
        </div>
      </div>

      <div class="panel-box">
        <h2 class="panel-title">MATCH SCENARIO</h2>
        <textarea id="match-input" placeholder="Input match situation..."></textarea>
        <div class="btn-row">
          <button class="btn btn-secondary" id="load-demo-btn">DEMO</button>
          <button class="btn btn-primary" id="run-btn">EXECUTE</button>
        </div>
      </div>

      <div class="panel-box pressure-meter">
        <div class="pressure-label"><span>PRESSURE INDEX</span> <span id="pressure-val">0</span></div>
        <div class="pressure-track"><div class="pressure-fill" id="pressure-fill"></div></div>
      </div>

      <div class="panel-box" style="flex: 1; display: flex; flex-direction: column;">
        <div id="war-room-toggle">[+] VIEW RAW TELEMETRY</div>
        <div id="war-room-content"></div>
      </div>

    </div>

    <!-- Center Arena -->
    <div class="arena">
      
      <div class="transcript-container" id="transcript-container" style="height: 100%; display: flex; flex-direction: column;">
        <div class="transcript" id="transcript">
          <div style="color: #666; text-align: center; margin-top: 50px;">Awaiting match parameters...</div>
        </div>
        <div class="lower-third">
          <h3 class="sports-text">COMMENTARY DESK</h3>
          <p id="commentator-text" style="color: #666; font-style: italic;">Awaiting match action...</p>
        </div>
      </div>

      <div class="compare-grid" id="compare-grid">
        <div class="compare-col" id="col-dhoni" style="display:none;"><h3>DHONI</h3><div class="col-content"></div></div>
        <div class="compare-col" id="col-kohli" style="display:none;"><h3>KOHLI</h3><div class="col-content"></div></div>
        <div class="compare-col" id="col-rohit" style="display:none;"><h3>ROHIT</h3><div class="col-content"></div></div>
        <div class="compare-col" id="col-gambhir" style="display:none;"><h3>GAMBHIR</h3><div class="col-content"></div></div>
      </div>
      
      <div id="loader">PROCESSING...</div>
    </div>

  </div>

  <footer>
    <div class="ticker-label">LATEST UPDATES</div>
    <div class="ticker-wrapper">
      <div id="whisper-feed">
        <div class="whisper-card">System standing by...</div>
      </div>
    </div>
  </footer>
\n"""

start_idx = 0
for i, line in enumerate(lines):
    if "<script type=\"module\">" in line:
        start_idx = i
        break

lines = [new_html] + lines[start_idx:]

with open("/Users/abhisar/Desktop/Project/index.html", "w") as f:
    f.writelines(lines)
