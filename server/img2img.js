const _ = require('lodash');
const fs = require('fs');

const img2img = async (inputImagePath, outputImagePath, options, maskImagePath) => {


    let inputImage = (
        await fs.promises.readFile(inputImagePath)
    ).toString('base64');

    if(maskImagePath) {
        let maskImage = (
            await fs.promises.readFile(maskImagePath)
        ).toString('base64');
        options.mask = maskImage;
    }

    options.init_images = [inputImage];
    if(_.get(options, 'alwayson_scripts.ControlNet.args.0')){
        options.alwayson_scripts.ControlNet.args[0].input_image = inputImage;
    }
    try {
        const { data } = await axios.post(
            'http://localhost:7860/sdapi/v1/img2img',
            options,
            {
                timeout: 1000 * 60 * 10, // 10 min
            }
        );
        const outputImage = data.images[0];
        await fs.promises.writeFile(
            outputImagePath,
            outputImage,
            'base64'
        );
    } catch (error) {
        console.error(error);
        throw error;
    }
}

module.exports = {
    img2img
}