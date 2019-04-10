import ffmpeg
import imageio
import numpy as np
import time
from matplotlib import pyplot as plt
from ipywidgets import interact
import ipywidgets as widgets
from skimage import data, img_as_float, io
from skimage.measure import compare_ssim as ssim
from skimage.color import rgb2gray
# start time to calculate total run time
start_t = time.time()
file_name = 'in_2.mp4' # file name this will be replaced with an arg parse argument

# Get information about the video
probe = ffmpeg.probe(file_name)
video_info = next(x for x in probe['streams'] if x['codec_type']== 'video')
frame_rate = int(video_info['avg_frame_rate'][:video_info['avg_frame_rate'].find("/")])
width = int(video_info['width'])
height = int(video_info['height'])
num_frames = int(video_info['nb_frames'])

out, err = (
    ffmpeg
    .input(file_name)
    .output('pipe:', format='rawvideo', pix_fmt='rgb24')
    .run(capture_stdout=True)
)
video = np.frombuffer(out, np.uint8).reshape([-1, height, width, 3])


ssim_list = []
breaks = []
cut_off = 12 # number of frames of action needed to start and end a cut


for frame_num in range(num_frames-1):
    frame1 = video[frame_num, :, :, :]
    frame2 = video[frame_num+1, :, :, :]
    frame1 = rgb2gray(frame1)
    frame2 = rgb2gray(frame2)
    ssim_i = abs(1- ssim(frame1, frame2, data_range=frame2.max() - frame2.min()))
    ssim_list.append(ssim_i)
    print(f"frame: {frame_num} and frame: {frame_num +1}, SSIM: {ssim_i:.3f}")
    if ssim_i >= .25:
        breaks.append(frame_num)

clean_breaks = []
start = True
break_i = 0
for f_break in breaks:
        new_list = [f_break+y for y in range(1,(frame_rate//2))]
        if start:
                clean_breaks.append([f_break])
                start = False
                if not any(x in breaks for x in new_list):
                        clean_breaks[break_i].append(f_break)
                        start = True
                        break_i += 1
        else:
                if any(x in breaks for x in new_list):
                        pass
                else:
                        clean_breaks[break_i].append(f_break)
                        start = True
                        break_i += 1

print(clean_breaks)


out_v = []
for break_f in clean_breaks:
    begin = break_f[0] - frame_rate if (break_f[0] - frame_rate) > 0 else 0
    end = break_f[1] + frame_rate if (break_f[1] + frame_rate) < num_frames  else num_frames
    print(break_f, end, begin, frame_rate)
    for _ in range(begin,end):
        out_v.append(video[_,:,:,:])

imageio.mimwrite("test.mp4", out_v, fps=25)
# print(ssim_list)
plt.plot(ssim_list)
print(time.time() - start_t)

# frame = video[0, :, :, :]
# frame2 = video[30, :, :, :]
# frame = rgb2gray(frame)
# frame2 = rgb2gray(frame2)
#fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(10, 4),
#                         sharex=True, sharey=True)
#ax = axes.ravel()

# label = 'MSE: {:.2f}, SSIM: {:.2f}'

# ax[0].imshow(frame, cmap= plt.cm.gray, vmin=0, vmax=1)
# ax[1].imshow(frame2, cmap= plt.cm.gray, vmin=0, vmax=1)
# ax[0].set_xlabel(label.format(mse_none, ssim_none))
# ax[0].set_title('Original image')
plt.show()
