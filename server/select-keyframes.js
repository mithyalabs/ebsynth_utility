const fs = require('fs');
const path = require('path');
const axios = require('axios');

const selectKeyframes = async (projectDir, desiredFrames, maskMode) => {

    const keyframesDir = path.join(projectDir, maskMode === 'Invert' ? 'inv':'', 'video_key');
    const options = {
        stage_index: 1,
        project_dir: projectDir,
        original_movie_path: projectDir + "/preprocessed-video.mp4",
        key_min_gap: 2,
        key_max_gap: 300,
        key_add_last_frame: false,
        mask_mode: maskMode
    }
    let low_key_th = 0;
    let high_key_th = 100;
    let keyframes = [];
    let iter = 0
    do {
        options.key_th = low_key_th + (high_key_th - low_key_th) / 2;
        console.log(`applying key_th: ${options.key_th}`)
        await axios.post(
            'http://localhost:7860/ebsynth/process',
            options
        );
        keyframes = (await fs.promises.readdir(keyframesDir))
        .filter(fileName => fileName.endsWith('.png')).map(k => parseInt(k));

        if(keyframes.length === desiredFrames) break;

        if (keyframes.length > desiredFrames) {
            low_key_th = options.key_th;
        }
        else {
            high_key_th = options.key_th;
        }
        iter++;
    } while (high_key_th > low_key_th && keyframes.length !== desiredFrames && iter < 20)

    return { keyframes, options };
}


module.exports = {
    selectKeyframes
}