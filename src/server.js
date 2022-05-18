//set up express, globals
const express = require("express");
const path = require("path");
//const db = require("./db/db.json"); Using this method won't allow the db to update in real time, you would have to restart the server after
//every update
const fs = require("fs");
const {v4 : uuidv4} = require("uuid");
const util = require("util");
//const { json } = require("express/lib/response");
const api = require("./routes/index");
const PORT = process.env.PORT || 3001;
const app = express();

//middleware
app.use(express.urlencoded({extended: true}));
app.use(express.json());

//custom middleware
app.use("/api", api);

app.use(express.static("public"));

//Handles GET /notes route and responds with notes.html
app.get("/notes", (req, res) => {
    console.info(`${req.method} request received, responding with notes.html`);
    res.sendFile(path.join(__dirname, "public/notes.html"));
});

//Handles GET wildcard, responds with index.html
app.get("*", (req, res) => {
    console.info(`${req.method} request received and handled at wildcard, responding with index.html`);
    res.sendFile(path.join(__dirname, "public/index.html"));
});

//Listens on PORT, which is handled by the above
app.listen(PORT, () => {
    console.log(`Listening at ${PORT}`);
});
