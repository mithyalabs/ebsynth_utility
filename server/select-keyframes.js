const fs = require('fs');
const path = require('path');
const axios = require('axios');

const selectKeyframes = async (projectDir, desiredFrames, maskMode) => {

    const keyFramesDir = path.join(projectDir, maskMode === 'Invert' ? 'inv':'', 'video_key');
    const videoFramesDir = path.join(projectDir, 'video_frame');
    
    const totalFrames = (await fs.promises.readdir(videoFramesDir))
        .filter(fileName => fileName.endsWith('.png')).length;

    const options = {
        stage_index: 1,
        project_dir: projectDir,
        original_movie_path: projectDir + "/preprocessed-video.mp4",
        key_min_gap: Math.max(2, Math.floor((totalFrames / desiredFrames) / 4)),
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
    } while (iter < 10 || keyframes.length > desiredFrames)

    keyframes.sort();
    extraFrames.sort();
    if(keyframes.length < desiredFrames) {
        let maxDist = 0, maxDistFrame;
        for(const frame of extraFrames) {
            const frameNumber = parseInt(frame);
            if(!keyframes.includes(frame)) {
                let lowFrameNumber = parseInt(keyframes[0]);
                let highFrameNumber = parseInt(keyframes[keyframes.length-1]);
                
                for(const keyFrame of keyframes) {
                    const keyFrameNumber = parseInt(keyFrame);
                    if(keyFrameNumber < frameNumber && keyFrameNumber > lowFrameNumber) {
                        lowFrameNumber = keyFrameNumber;
                    }
                    if(keyFrameNumber > frameNumber && keyFrameNumber < highFrameNumber) {
                        highFrameNumber = keyFrameNumber;
                    }
                }
                const lowDist = frameNumber - lowFrameNumber;
                const upDist = highFrameNumber - frameNumber;
                
                if(maxDist < lowDist && maxDist < upDist) {
                    maxDist = Math.min(lowDist, upDist);
                    maxDistFrame = frame;
                }
            }
        }
        console.log(`Adding frame ${maxDistFrame}`);
        await fs.promises.copyFile(
            path.join(videoFramesDir, maxDistFrame),
            path.join(keyFramesDir, maxDistFrame)
        );
        keyframes.push(maxDistFrame);
    }
    keyframes = keyframes.map(k => parseInt(k));
    keyframes.sort();
    return { keyframes, options };
}


module.exports = {
    selectKeyframes
}