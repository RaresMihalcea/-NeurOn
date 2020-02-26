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

let lock = 0;

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
    if(lock === 0) {
        lock = 1;
        var runPath;
        if (isDev) {
            runPath = path.join(__dirname, "../python/dist/main/main.exe");
        }
        else {
            runPath = path.join(process.resourcesPath, '../python/dist/main/main.exe');
        }
        exec(runPath, [arg], (error, stdout, stderr) => {
            console.log(arg);
            console.log(stdout);
    
            if(stdout.includes('finished')) {
                mainWindow.webContents.send('info', 'Algorithm Finished');
                mainWindow.webContents.send('output', stdout);
                lock = 0;
            }

            if(stderr != []) {
                lock = 0;
                console.log(stderr);
                mainWindow.webContents.send('error', stderr);
            }
    
            if (error) throw error;
        });
    }
    else {
        mainWindow.webContents.send('info', "Algorithm is already running");
    }
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