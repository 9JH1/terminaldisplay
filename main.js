const { app, BrowserWindow } = require("electron");
const path = require("path");
const { execFile } = require("child_process");

function getData2(endpoint) {
  return fetch(`http://127.0.0.1:5000${endpoint}`)
    .then((res) => res.text())
    .catch((error) => {});
}
getData2("/alive").then(function (data) {
  if (String(data) === "alive") {
    console.log("app already open");
    app.exit();
  }
});
getData2("/stopServer");
function loadMainWindow() {
  let intervalId = setInterval(() => {
    getData2("/alive").then(function (data) {
      if (String(data) === "alive") {
        clearInterval(intervalId);
        const createWindow = () => {
          const win = new BrowserWindow({
            fullscreen: true,
            autoHideMenuBar: true,
          });
          win.loadFile("index.html");
        };
        createWindow();
        app.on("activate", () => {
          if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
          }
        });
      }
    });
  }, 1000);
}
app.whenReady().then(() => {
  getData2("/stopServer");
  let child = execFile(path.join(__dirname, "main.exe"), ["idk"], {
    detached: true,
    stdio: "ignore",
  });

  child.unref();

  child.on("exit", (code) => {
    console.log(`main.exe exited with code ${code}`);
  });
  child.on("message", (message) => {
    console.log(message);
  });

  child.on("error", (error) => {
    console.error(`Error starting main.exe: ${error}`);
  });
  loadMainWindow();

  app.on("before-quit", () => {
    getData2("/stopServer");
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});
