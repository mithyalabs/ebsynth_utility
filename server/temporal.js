const fs = require('fs');
const path = require('path');
const axios = require('axios');


const temporalRequest = async (currentImage, lastImage, options, mask) => {
    options.script_args = [];
    options.script_name = '';
    options.mask = mask ? mask : '';
    options.init_images = [lastImage];
    options.alwayson_scripts.ControlNet.args[0].input_image = currentImage;
    options.alwayson_scripts.ControlNet.args[1].input_image = lastImage;
    try {
        const { data } = await axios.post(
            'http://localhost:7860/sdapi/v1/img2img',
            options,
            {
                timeout: 1000 * 60 * 10, // 10 min
            }
        );
        return data.images[0];
    } catch (error) {
        console.error(error);
        throw error;
    }
}


const temporal = async (initImagePath, inputFolder, outputFolder, options, maskFolder) => {
    if(!initImagePath || !inputFolder || !outputFolder || !options) {
        throw new Error('Missing arguments');
    }
    console.log("initImagePath", initImagePath);
    let lastImage = (
        await fs.promises.readFile(initImagePath)
    ).toString('base64'); 

    const inputImageNames = await fs.promises.readdir(inputFolder);

    for (let i = 0; i < inputImageNames.length; i++) {
        const currentImagePath = path.join(inputFolder, inputImageNames[i]);
        console.log("currentImagePath", currentImagePath);
        const currentImage = (
            await fs.promises.readFile(currentImagePath)
        ).toString('base64');

        let maskImagePath, maskImage;
        if(maskFolder) {
            maskImagePath = path.join(maskFolder, inputImageNames[i]);
            console.log("maskImagePath", maskImagePath);
            maskImage = (
                await fs.promises.readFile(maskImagePath)
            ).toString('base64');
        }


		lastImage = await temporalRequest(currentImage, lastImage, options, maskImage);
        await fs.promises.writeFile(
            path.join(outputFolder, inputImageNames[i]),
            lastImage,
            'base64'
        );
    }
}


module.exports = {
    temporal
}