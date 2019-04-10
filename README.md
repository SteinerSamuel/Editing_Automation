# Editing_Automation
A small automated editor script for finding action in videos and splicing those clips together

### Why do this?
The reason I decided to work on this project was to better get a grasp on tools such as mmpeg and scikit learn. Another reason why I decided to create this was a video by Devin Crawford. In his video he used RGB values of each pixel to discover action. I thought well I know about SSIM I wonder how it would work with SSIM. So I was off to creating this code.


### How does it work?
So right now the program only takes one video file, eventually I would like it to take an entire folder of vides but a lot of optimization will be needed to get there. Roughly FFMPEG reads the video file frame by frame converting it into numpy arrays from there we run each concurrent frame into scimage's SSIM to get a similarity index. From there we can then decide how similar or dissimilar we want our cuts to be. After that we simplify the cuts by creating starts and ends for each clip. Finally we take a bit before the start and a bit after and splice them all together down into a final piece.

Right now the code does no handle audio this will be something that I would like to add in the future.
