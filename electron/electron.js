// Electron declarations
const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
const ipcMain = electron.ipcMain;

// Other dependencies
const path = require('path');
const url = require('url');
const isDev = require('electron-is-dev');
const exec = require('child_process').execFile;

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow(
        {
            width: 800, height: 600,
            webPreferences: {
                nodeIntegration: true
            }
        });

    mainWindow.loadURL(
        process.env.ELECTRON_START_URL ||
        url.format({
            pathname: isDev ? 'http://localhost:4200' : path.join(__dirname, '../build/index.html'),
            slashes: isDev ? false : true
        }
        )
    );

    mainWindow.setMenu(null);
    mainWindow.webContents.openDevTools();
    mainWindow.maximize();

    mainWindow.on('closed', () => {
        mainWindow = null
    });
}

ipcMain.on('run', (event, arg) => {
    var runPath;
    if (isDev) {
        runPath = path.join(__dirname, "../python/dist/test/test.exe");
    }
    else {
        runPath = path.join(process.resourcesPath, '../python/dist/test/test.exe');
    }
    exec(runPath, [arg], (error, stdout, stderr) => {
        console.log(event);
        console.log(arg);
        console.log(stdout);
        // mainWindow.webContents.send('testIpc', stdout);
        if (error) throw error;
    });
});

app.on('ready', () => {
    createWindow();
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
});

app.on('activate', () => {
    if (mainWindow === null) {
        createWindow();
    }
});