const fs = require("fs");

//Helper function to read from the db, append to it, and write it back
function appendToFile(noteTitle, noteText, id) {
    const obj = {
        title: noteTitle,
        text: noteText,
        id: id
    };
    fs.readFile("./db/db.json", (err, data) => {
        if (err) {
            console.err(`Error reading from ./db/db.json ${err}`);
        }
        const jsonData = JSON.parse(data);
        jsonData.push(obj);
        fs.writeFile("./db/db.json", JSON.stringify(jsonData), (err) => {
            if (err) {
                console.err(`Error writing to ./db/db.json ${err}`);
            }
        });
    });
    return obj;
}

module.exports = {appendToFile};