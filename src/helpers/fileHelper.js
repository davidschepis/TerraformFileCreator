const fs = require("fs");

checkFilePath = () => {
    if (fs.existsSync("../mnt/note-taker-db")) {
        console.log('Directory exists!');
        return true
    } else {
        console.log('Directory not found.');
        return false
    }
};

let path = ""
if (checkFilePath()) {
    path = "../mnt/note-taker-db/db.json"
}
else {
    path = "./db/db.json"
}


//Helper function to read from the db, append to it, and write it back
function appendToFile(noteTitle, noteText, id) {
    const obj = {
        title: noteTitle,
        text: noteText,
        id: id
    };
    fs.readFile(path, (err, data) => {
        if (err) {
            console.err(`Error reading from ../mnt/note-taker-db/db.json ${err}`);
        }
        const jsonData = JSON.parse(data);
        jsonData.push(obj);
        fs.writeFile(path, JSON.stringify(jsonData), (err) => {
            if (err) {
                console.err(`Error writing to ../mnt/note-taker-db/db.json ${err}`);
            }
        });
    });
    return obj;
}

module.exports = { appendToFile };