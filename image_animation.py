import sys
sys.path.append("/home/esbern/first-order-model")

import imageio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from skimage import img_as_ubyte
from skimage.transform import resize
from IPython.display import HTML
from demo import load_checkpoints, make_animation
import warnings
import argparse
warnings.filterwarnings("ignore")


def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start Image Animation')
    parser.add_argument("--image_path", type=str, default='./data/images/02.png')
    parser.add_argument("--video_path", type=str, default='./data/videos/04.mp4')
    parser.add_argument("--use_relative",type=str2bool, nargs='?',
                        const=True, default=True)
    #parser.add_argument("--exclude_pattern", nargs="+", default=[""])
    args = parser.parse_args()


    image_path = args.image_path
    video_path = args.video_path
    source_image = imageio.imread(image_path)
    driving_video = imageio.mimread(video_path, memtest=False)


    #Resize image and video to 256x256

    source_image = resize(source_image, (256, 256))[..., :3]
    driving_video = [resize(frame, (256, 256))[..., :3] for frame in driving_video]

    imageio.imwrite('./generated/downscaled_image.png',source_image)
    generator, kp_detector = load_checkpoints(config_path='config/vox-256.yaml',
                                checkpoint_path='./models/vox-cpk.pth.tar')

    predictions = make_animation(source_image, driving_video, generator, kp_detector, relative=args.use_relative)

    #save resulting video
    imageio.mimsave('./generated/generated.mp4', [img_as_ubyte(frame) for frame in predictions])