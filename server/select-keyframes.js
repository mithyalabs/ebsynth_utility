const fs = require('fs');
const path = require('path');
const axios = require('axios');

const selectKeyframes = async (projectDir, desiredFrames, maskMode) => {

    const keyFramesDir = path.join(projectDir, maskMode === 'Invert' ? 'inv':'', 'video_key');
    const videoFramesDir = path.join(projectDir, maskMode === 'Invert' ? 'inv':'', 'video_frame');

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
    let extraFrames = [];
    let iter = 0
    do {
        options.key_th = low_key_th + (high_key_th - low_key_th) / 2;
        console.log(`applying key_th: ${options.key_th}`)
        await axios.post(
            'http://localhost:7860/ebsynth/process',
            options
        );
        keyframes = (await fs.promises.readdir(keyFramesDir))
        .filter(fileName => fileName.endsWith('.png'));

        console.log(`got ${keyframes.length} frames`);

        if(keyframes.length > desiredFrames) {
            extraFrames = [...keyframes];
        }
        if(keyframes.length === desiredFrames) break;

        if (keyframes.length > desiredFrames) {
            low_key_th = options.key_th;
        }
        else {
            high_key_th = options.key_th;
        }
        iter++;
    } while (iter < 12 || keyframes.length < desiredFrames)

    if(keyframes.length < desiredFrames) {
        for(let frame of extraFrames) {
            if(!keyframes.includes(frame)) {
                console.log(`Adding frame ${frame}`);
                await fs.promises.copyFile(
                    path.join(videoFramesDir, frame),
                    path.join(keyFramesDir, frame)
                );
                keyframes.push(frame);
                break;
            }
        }
    }
    keyframes = keyframes.map(k => parseInt(k));
    keyframes.sort();
    return { keyframes, options };
}


module.exports = {
    selectKeyframes
}