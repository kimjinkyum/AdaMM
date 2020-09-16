from multiprocessing import Process
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
import argparse
import cv2
import logging

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

def init_logger():
    logger = logging.getLogger('TfPoseEstimator-WebCam')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

class ChildProcess(Process):
    def __init__(self,queue):
        super().__init__()
        self.image_queue=queue

    def __del__(self):
        pass

    # Start 혹은 run 메소드 실행 시
    def run(self):
        args,w,h,e=self.init_model()
        i=0
        print("child process",id(self))
        while True:
            image=self.image_queue.get()
            print("Process value",image)
            print("tensorflow model",e)
            i=i+1


    def init_model(self):
        parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')
        parser.add_argument('--resize', type=str, default='0x0',
                            help='if provided, resize images before they are processed. default=0x0, Recommends : 432x368 or 656x368 or 1312x736 ')
        parser.add_argument('--resize-out-ratio', type=float, default=4.0,
                            help='if provided, resize heatmaps before they are post-processed. default=1.0')

        parser.add_argument('--model', type=str, default='mobilenet_thin',
                            help='cmu / mobilenet_thin / mobilenet_v2_large / mobilenet_v2_small')
        parser.add_argument('--show-process', type=bool, default=False,
                            help='for debug purpose, if enabled, speed for inference is dropped.')

        parser.add_argument('--tensorrt', type=str, default="False",
                            help='for tensorrt process.')
        args = parser.parse_args()
        w, h = model_wh(args.resize)
        if w > 0 and h > 0:
            e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h),
                                             trt_bool=str2bool(args.tensorrt))
        else:
            e = TfPoseEstimator(get_graph_path(args.model), target_size=(432, 368),
                                             trt_bool=str2bool(args.tensorrt))
        return args,w,h,e
