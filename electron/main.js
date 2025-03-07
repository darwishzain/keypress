const { app, BrowserWindow } = require('electron');
const path = require('path');

let mainWindow;
app.commandLine.appendSwitch('disable-gpu');
app.commandLine.appendSwitch('disable-features', 'Autofill');

function createWindow() {
  // Create a new browser window
    mainWindow = new BrowserWindow({
    width: 600,
    height: 300,
    frame:false,
    transparent:true,
    webPreferences: {
      nodeIntegration: true, // allows the renderer to access Node.js APIs
      contextIsolation: false, // Disable context isolation for compatibility
    },
  });

  // Load the index.html file into the window
  mainWindow.loadFile('index.html');

  // Open the DevTools (optional)
  //mainWindow.webContents.openDevTools();

  // When the window is closed, clean up
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// When Electron is ready to create windows
app.whenReady().then(() => {
    createWindow();

// On macOS, create a window when the app is activated (e.g., clicking the app icon)
app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
  });
});

// Quit the app when all windows are closed (except on macOS)
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
