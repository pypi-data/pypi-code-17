import argparse

import scipy
import numpy as np

from moviepy.editor import (
    VideoFileClip, ImageSequenceClip, concatenate_videoclips, vfx)


TEST_MERGE = False


def debug_frame(frame, frame_count=0):
    scipy.misc.imsave('debug_frame_{0:0>3}.jpg'.format(frame_count), frame)


def debug_clip(clip, clip_count):
    clip.write_videofile("debug_clip_{0:0>3}.mp4".format(clip_count))


def debug_frame_diff(f1, f2):
    return np.linalg.norm(f1 - f2)


class YiMerge(object):
    """docstring for YiMerge"""

    def __init__(self, clips_filenames):
        super(YiMerge, self).__init__()
        self.clips_filenames = clips_filenames
        self.clips = []
        self.final_clip = None

    def load(self):
        self.clips = [
            # VideoFileClip(fn).fx(vfx.resize, 0.3).fx(vfx.speedx, 4)
            VideoFileClip(fn)
            for fn in self.clips_filenames]

        if TEST_MERGE:
            self.clips[0] = self.clips[0].subclip(self.clips[0].end - 5)
            self.clips[1] = self.clips[1].subclip(0, 5)
            self.clips = self.clips[:2]

    @classmethod
    def trim_clip_to_frame(cls, clip, frame, overlap=3):
        audio_clip = clip.audio
        clip_tail = clip.subclip(max(clip.end - overlap, 0))
        clip = clip.subclip(0, max(clip.end - overlap, 0))
        frames = []

        for tail_frame in clip_tail.iter_frames():
            if np.array_equal(frame, tail_frame):
                break
            frames.append(tail_frame)

        if frames:
            clip_tail = ImageSequenceClip(frames, fps=clip.fps)
            clip = concatenate_videoclips([clip, clip_tail])

            # Mix correct audio
            audio_clip = audio_clip.subclip(0, clip.end)
            clip = clip.set_audio(audio_clip)

        return clip

    def merge(self):
        for i, c in enumerate(self.clips[1:]):
            cut_frame = next(c.iter_frames())

            # for f in c.iter_frames():
            #     dist = np.linalg.norm(cut_frame - f)
            #     print(dist)

            clip = self.trim_clip_to_frame(self.clips[i], cut_frame)

            # TODO: remove second frame from begining (option)

            # Update previous clip with trimmed version
            self.clips[i] = clip

        self.final_clip = concatenate_videoclips(self.clips)

    def save(self, target=None):
        self.final_clip.write_videofile("my_concatenation.mp4")


def main():
    # Construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-c", "--clips", nargs='+', required=True,
        help="Path to the clips to be merged")
    args = vars(ap.parse_args())

    yi = YiMerge(args['clips'])
    yi.load()
    yi.merge()
    yi.save()


if __name__ == '__main__':
    main()
