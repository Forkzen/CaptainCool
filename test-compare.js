const fs = require('fs');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;

const html = fs.readFileSync('/Users/abhisar/Desktop/Project/index.html', 'utf8');

const dom = new JSDOM(html, { runScripts: "dangerously", pretendToBeVisual: true });
const window = dom.window;
const document = window.document;

setTimeout(async () => {
  // Stub genAI module
  window.GoogleGenAI = class {
    constructor() {
      this.models = {
        generateContent: async () => { throw new Error("Offline mock trigger"); }
      }
    }
  };
  window.Type = { OBJECT: "OBJECT", STRING: "STRING", INTEGER: "INTEGER", BOOLEAN: "BOOLEAN" };

  try {
    // Fill api key to bypass check
    document.getElementById('api-key-input').value = "test-key";
    document.getElementById('save-key-btn').click();

    // Toggle compare mode
    document.getElementById('compare-toggle-btn').click();

    // Run
    document.getElementById('match-input').value = "Last over, 10 runs to win";
    
    // Listen for any errors
    window.addEventListener('error', (event) => {
      console.error("Window Error:", event.error);
    });
    
    console.log("Before click, isCompareMode:", window.isCompareMode);
    document.getElementById('run-btn').click();
    
    await new Promise(r => setTimeout(r, 6000)); // wait for delays
    
    console.log("Dhoni Col HTML:", document.querySelector('#col-dhoni .col-content').innerHTML);
    console.log("Kohli Col HTML:", document.querySelector('#col-kohli .col-content').innerHTML);
    console.log("Compare Grid Display:", document.getElementById('compare-grid').style.display);
  } catch(e) {
    console.error("Caught error:", e);
  }
}, 500);
