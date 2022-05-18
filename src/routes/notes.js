const notes = require("express").Router();
const {appendToFile} = require("../helpers/fileHelper");
const fs = require("fs");
const {v4 : uuidv4} = require("uuid");
const util = require("util");

//Read file promise
const readFromFile = util.promisify(fs.readFile);

//Handles GET /api/notes route and responds with db.json file
notes.get("/", (req, res) => {
    console.info(`${req.method} request received, responding with db.json`);
    //res.json(db);
    readFromFile("./db/db.json").then((data) => res.json(JSON.parse(data)));
});

//Handles POST /api/notes route, saves the request into the database and responds with the new database item
notes.post("/", (req, res) => {
    console.info(`${req.method} request received, updating db.json`);
    const {title, text} = req.body;
    console.info(`Received \nTitle: ${title}\nText: ${text}`);
    let id = uuidv4();
    console.info(`Creating unique id: ${id}`);
    const newNote = appendToFile(title, text, id);
    console.info("Append complete!");
    res.send(newNote);
});

//Handles DELETE request, reads from the db, finds the corresponding id, removes the obj, and writes back
notes.delete("/:id", (req, res) => {
    console.info(`${req.method} request received, deleting note with id: ${req.params.id}`);
    fs.readFile("./db/db.json", (err, data) => {
        if (err) {
            console.err(`Error reading from ./db/db.json ${err}`);
        }
        let db = JSON.parse(data);
        db = db.filter((i) => {
            return i.id !== req.params.id;
        });
        fs.writeFile("./db/db.json", JSON.stringify(db), (err) => {
            if (err) {
                console.err(`Error writing to ./db/db.json ${err}`);
            }
        });
        console.info("Write back after deletion completed!");
    });
    res.send("Delete completed");
});

module.exports = notes;