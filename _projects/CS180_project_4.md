---
layout: page
title: CS180 Project 4
description: Image Warp + Mosaic
img: assets/img/CS180/Project_4/5_5.png
importance: 1
category: work
related_publications: false
---

## Task 1: Taking Pictures (Rectification)

Our first task is to take a couple of pictures of rectangle-shaped objects from different angles, and try to rectify them. I chose 3 different pictures below: a vinyl cd, a no-smoking sign, and finally a rectangular window. I'm particularly interested in the window as the effect of rectifying gives the illusion that we're standing right in front of the object thus making it rectangular, but we obviously can't see straight out the window as our view is from the side, so what would the effect look like in the finished image?

<div class="row">
<div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/1_1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/2_1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/3_1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

## Task 2: Recover Homographies

Next, we need to recover a homography to transform the images. In our first problem of rectification, the idea is simple: Label the 4 corners of the images, select 4 additional points to create a rectangle (roughly the same shape as the original object), and recover a homography from the image's 4 corners to the rectangle.

Here are the pairs of points that were chosen for the images:

<div class="row align-items-end">
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/1_3.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/1_4.png" title="camera man x" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

<div class="row align-items-end">
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/2_3.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/2_4.png" title="camera man x" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

<div class="row align-items-end">
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/3_3.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/3_4.png" title="camera man x" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

After setting the points, we set up the equation p’=Hp, where p’ is our destination points and p is our source points, and solve for H. In this case, since we have 4 points, there is only one possible H that can satisfy the equation. For mosaics though, we'll choose more points for stability, so we'll make an overdetermined system and use least squares (or SVD) in order to find the best solution.

To solve for H, we'll use the equation we learned in lecture, and use SVD to find the least squares solution:

$$
   A = \begin{bmatrix}
   x_1 & y_1 & 1 & 0 & 0 & 0 & -x_2 x_1 & -x_2 y_1 & -x_2 \\
   0 & 0 & 0 & x_1 & y_1 & 1 & -y_2 x_1 & -y_2 y_1 & -y_2
   \end{bmatrix}
$$

By then using SVD, decomposing the matrix into the form:

$$
   A = U S V^T
$$

The least squares solution will be in $$ V^T $$, which has 9 variables

We reshape this into a 3x3 matrix, and then by dividing the entire matrix by the last variable (I), we get an H of the form

$$
H = \begin{bmatrix}
   h_1 & h_2 & h_3 \\
   h_4 & h_5 & h_6 \\
   h_7 & h_8 & 1
   \end{bmatrix}
$$

Now, if we plug in a particular point (with a one appended to it) from the image, the resulting point will look like:

$$
\begin{bmatrix}
wx_2 \\
wy_2 \\
w
\end{bmatrix}
=
H
\begin{bmatrix}
x_1 \\
y_1 \\
1
\end{bmatrix}
$$

Dividing the resulting point by w yields $$ x_2 $$ and $$ y_2 $$, giving our new coordinates.

## Task 3: Warping the image (Image Rectification)

Now that we have the homography, it seems trivial to simply pipe each point of the original image through the homography to get the new coordinates of that pixel, giving us our result. However, this is forward warping, and as we've seen in project 3 this results in tons of holes. Therefore, we need to use inverse warping instead. Thus, the algorithm looks very similar with our triangle warping function from Project 3:

1. Find the homography H from src_points to dst_points
2. Take the inverse, yielding H'
3. Determine the dimensions of the resulting image by warping the 4 corners of the src image through H. Shift the entire image if there are any negative values so that the negative values become 0. 
4. For each point in the resulting image, apply H' and interpolate to find the src image's corresponding pixel value, and apply it.

We can also vectorize 4 by making a 2D matrix of all the points in our result image, yielding a way faster result. We'll ignore any points that are outside of the convex hull of the warped bounding box.

<div class="row align-items-end">
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/1_1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/1_2.png" title="camera man x" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

<div class="row align-items-end">
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/2_1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/2_2.png" title="camera man x" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

<div class="row align-items-end">
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/3_1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/3_2.png" title="camera man x" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

The results surprised me, giving us the illusion that we're looking at the images from a new point of view. The window one shocked me the most. We weren't able to see more of the scenery outside of the window (of course), but a shift in the perspective and perceived distance from the window warped the window to a rectangular shape.

## Task 4: Image Stitching (Manual)

Lastly, we come to image stitching. At a high level the steps are to:

1. Take a pair of images with significant overlap. Label common features/points between the two images
2. Create a homography to map the second image's points to the corresponding points in the first image
3. Warp the second image using what we created in Task 3
4. Align the images together, and blend.

First, let's take a couple of pictures:

<div class="row align-items-end">
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/4_1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/4_2.png" title="camera man x" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

<div class="row align-items-end">
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/5_1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/5_3.png" title="camera man x" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

Next, let's label some correspondences between them manually.

<div class="row align-items-end">
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/4_6.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Working on the project
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/4_7.png" title="camera man x" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Working on the project side view
        </div>
    </div>
</div>

<div class="row align-items-end">
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/5_6.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Balcony
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/5_7.png" title="camera man x" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Balcony side view
        </div>
    </div>
</div>

Then, we warp the second image using the homography recovered

<div class="row align-items-end">
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/5_1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/5_2.png" title="camera man x" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

<div class="row align-items-end">
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/4_1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/4_3.png" title="camera man x" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

Now, we need to align. Unfortunately if we stacked one image atop the other, the borders will be really obvious. Therefore, we need some form of blending. The algorithm I came up with is:

1. Recover x_shift and y_shift from inverse warping. We found this when applied H to the bounding box of image 2 while inverse warping.
2. Reshape image 1 so that the height of the image is the same as image 2, and apply y_shift so that they are aligned in the y_axis.
3. Apply x_shift to image 2 so that the x_axis is aligned.
4. Find the overlapping image (all points with x value between x_shift and im1.width)
5. Fill in the non-overlapping areas with image 1 on the left and image 2 on the right.
6. In the overlapping area, use an alpha value that begins at 0 at the left side and increases to 1 on the right side. Use a weighted sum of image 1 and image 2, multiplying image 1's pixel values by (1 - alpha) and image 2's by alpha.

This results in the following images:

<div class="row align-items-end">
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/4_4.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Working on the project finished
        </div>
    </div>
</div>

<div class="row align-items-end">
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/5_4.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            balcony finished
        </div>
    </div>
</div>

One issue is the strange triangular gray areas in the overlapping region. We can fix this by using a for loop to detect points in the overlapping region where one image is out of bounds. If that's the case, use only the pixel values from the image that isn't out of bounds.

<div class="row align-items-end">
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/4_5.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Working on the project improved
        </div>
    </div>
</div>

<div class="row align-items-end">
    <div class="col-sm mt-3 mt-md-0" style="height: 50%;">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_4/5_5.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Balcony improved
        </div>
    </div>
</div>

Overall, this project was immensely satisfying and it was fun taking some of the functions and logic that was written in project 3 and reusing it. As a kid I always thought it'll be easy to make panoramic shots - just blend many images together! But this project proved otherwise, and showed that there are many optimizations and changes needed before it looks decent.

Another key learning from this was the importance of good labeling. I tried only using 4-5 points for the balcony picture and that resulted in disaster, where the roads were obviously not lined up. I realized it's because I was mostly using features at the top of the image and neglected points at the bottom. I was surprised that adding twice the number of points and adding more points at the bottom of the image made the stitching far far better.