const express = require('express');
const bodyParser = require('body-parser');
const { temporal } = require('./temporal');
const app = express();
const port = 3000;

app.use(bodyParser.json());

app.post('/server/temporal', async (req, res, next) => {
    const body = req.body || {};
    const { initImagePath, inputFolder, outputFolder, options } = body;
    console.log(initImagePath, inputFolder, outputFolder, options); 
    try {
        await temporal(initImagePath, inputFolder, outputFolder, options);
    } catch (err) {
        console.log(err);
        next(err);
    }
});


app.listen(port, () => {
    console.log(`Server listening on port ${port}`)
});