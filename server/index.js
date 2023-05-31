const express = require('express');
const bodyParser = require('body-parser');
const { temporal } = require('./temporal');
const { upscale } = require('./upscale');
const { img2img } = require('./img2img');
const { selectKeyframes } = require('./select-keyframes');
const app = express();
const port = 3000;

app.use(bodyParser.json());

app.post('/server/temporal', async (req, res, next) => {
    const body = req.body || {};
    const { initImagePath, inputFolder, outputFolder, options, maskFolder } = body;
    console.log(initImagePath, inputFolder, outputFolder, options, maskFolder);
    console.log("temporal:options", JSON.stringify(options, null, 2));
    console.log("temporal:initImagePath", initImagePath);
    console.log("temporal:inputFolder", inputFolder);
    console.log("temporal:outputFolder", outputFolder);
    console.log("temporal:maskFolder", maskFolder);
    try {
        await temporal(initImagePath, inputFolder, outputFolder, options, maskFolder);
    } catch (err) {
        console.log(err);
        return next(err);
    }
    return res.send('OK');
});

app.post('/server/upscale', async (req, res, next) => {
    const body = req.body || {};
    const { inputFolder, outputFolder, options } = body;
    console.log("upscale:options", JSON.stringify(options, null, 2));
    console.log("upscale:inputFolder", inputFolder); 
    console.log("upscale:outputFolder", outputFolder);
    try {
        await upscale(inputFolder, outputFolder, options);
    } catch (err) {
        console.log(err);
        return next(err);
    }
    return res.send('OK');
});

app.post('/server/img2img', async (req, res, next) => {
    const body = req.body || {};
    const { inputImagePath, outputImagePath, options, maskImagePath } = body;
    console.log("img2img:options", JSON.stringify(options, null, 2)); 
    console.log("img2img:inputImagePath", inputImagePath); 
    console.log("img2img:outputImagePath", outputImagePath);
    console.log("img2img:maskImagePath", maskImagePath); 
    try {
        await img2img(inputImagePath, outputImagePath, options, maskImagePath);
    } catch (err) {
        console.log(err);
        return next(err);
    }
    return res.send('OK');
});
app.post('/server/select-keyframes', async (req, res, next) => {
    const body = req.body || {};
    const { projectDir, desiredFrames, maskMode } = body;
    console.log("selectKeyframes:projectDir", projectDir); 
    console.log("selectKeyframes:desiredFrames", desiredFrames); 
    console.log("selectKeyframes:maskMode", maskMode);
    try {
       const resp = await selectKeyframes(projectDir, desiredFrames, maskMode);
       return res.send(resp)
    } catch (err) {
        console.log(err);
        return next(err);
    }
});


app.listen(port, () => {
    console.log(`Server listening on port ${port}`)
});