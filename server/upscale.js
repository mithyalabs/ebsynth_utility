const fs = require('fs');
const path = require('path');
const axios = require('axios');


const upscale = async (inputFolder, outputFolder, options) => {
    if(!inputFolder || !outputFolder || !options) {
        throw new Error('Missing arguments');
    }


    const inputImageNames = await fs.promises.readdir(inputFolder);

    for(let imageName of inputImageNames) {
        const imagePath = path.join(inputFolder, imageName);
        let image = (
            await fs.promises.readFile(imagePath)
        ).toString('base64'); 
        options.imageList = [
            {
                data: 'data:image/png;base64,' + image.toString('base64'),
                name: 'upscale',
            },
        ];
        const { data } = await axios.post(
            'http://localhost:7860/sdapi/v1/extra-batch-images',
            options,
            {
                timeout: 1000 * 60 * 10, // 10 min
            }
        );
        const upscaleImage = data.images[0];
        await fs.promises.writeFile(
            path.join(outputFolder, imageName),
            upscaleImage,
            'base64'
        );
    }
}

module.exports = {
    upscale
}