const express = require('express');
const bodyParser = require('body-parser');
const { temporal } = require('./temporal');
const { upscale } = require('./upscale');
const app = express();
const port = 3000;

app.use(bodyParser.json());

app.post('/server/temporal', async (req, res, next) => {
    const body = req.body || {};
    const { initImagePath, inputFolder, outputFolder, options, maskFolder } = body;
    console.log(initImagePath, inputFolder, outputFolder, options, maskFolder);
    console.log("temporal:initImagePath", initImagePath);
    console.log("temporal:inputFolder", inputFolder);
    console.log("temporal:outputFolder", outputFolder);
    console.log("temporal:options", JSON.stringify(options, null, 2));
    console.log("temporal:maskFolder", maskFolder);
    try {
        await temporal(initImagePath, inputFolder, outputFolder, options, maskFolder);
    } catch (err) {
        console.log(err);
        next(err);
    }
});

app.post('/server/upscale', async (req, res, next) => {
    const body = req.body || {};
    const { inputFolder, outputFolder, options } = body;
    console.log("upscale:inputFolder", inputFolder); 
    console.log("upscale:outputFolder", outputFolder); 
    console.log("upscale:options", JSON.stringify(options, null, 2)); 
    try {
        await upscale(inputFolder, outputFolder, options);
    } catch (err) {
        console.log(err);
        next(err);
    }
});


app.listen(port, () => {
    console.log(`Server listening on port ${port}`)
});