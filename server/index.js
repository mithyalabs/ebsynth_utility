const express = require('express');
const { temporal } = require('./temporal');
const app = express();
const port = 3000;


app.get('/temporal', async (req) => {
    const body = req.body || {};
    const { initImagePath, inputFolder, outputFolder, options } = body;
    await temporal(initImagePath, inputFolder, outputFolder, options);
});


app.listen(port, () => {
    console.log(`Server listening on port ${port}`)
});