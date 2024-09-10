---
layout: page
title: CS180 Project 1
description: Colorizing the Prokudin-Gorskii photo collection
img: assets/img/CS180/Project_1/emir.jpg
importance: 1
category: work
related_publications: false
---

## Task 1: Exhaustive Search

For smaller images, we can use an exhaustive search to try all possible "offsets", in which we shift an image in the x or y direction, within a range to find an optimal alignment for overlaying the three images together. The pseudocode is pretty straightforward:

1. Select one image as the reference image. We use the B channel here.
2. For all other images, perform an exhaustive search in the range -N to +N pixels for the x and y direction. We use N=20 here.
3. Shift the image by the specified displacement, and use some sort of metric to determine the quality of this alignment. Record the highest score.

We tried three different metrics, with varying runtimes and effectiveness:

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        <div class="text-center">
            Inverse Euclidean Distance
        </div>
        $$ \text{inv}(m1, m2) = \frac{1}{\lVert m1 - m2 \rVert} $$
        <div class="caption">
            The simplest metric. Worked surprisingly well and was the fastest metric by far.
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        <div class="text-center">
            Structural Similarity Index
        </div>
        $$ \text{SSIM}(m1, m2) = \frac{(2 \mu_{m1} \mu_{m2} + C1)(2 \text{cov}(m1, m2) + C2)}{(\mu_{m1}^2 + \mu_{m2}^2 + C1)(\sigma_{m1}^2 + \sigma_{m2}^2 + C2)} $$
        <div class="caption">
            The slowest and most complicated, the SSIM measures the similarity between two images. Unfortunately, it was too slow, as it required creating multiple windows within the image itself to compare. Thus, it was discarded in favor of faster metrics
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        <div class="text-center">
            Normalized Cross Correlation (chosen)
        </div>
        $$ \text{ncc}(m1, m2) = \sum \left( \frac{m1_{\text{flat}} - \mu_{m1}}{\sigma_{m1}} \cdot \frac{m2_{\text{flat}} - \mu_{m2}}{\sigma_{m2}} \right) $$
        <div class="caption">
            Normalize first to deal with different average levels of pixel brightness before applying a dot product. This worked very well on cropped images and could be sped up by flattening into a vector before doing a dot product. We ended up choosing this one as it was reasonably fast and worked quite well on all images.
        </div>
    </div>
</div>

In addition to this, we also cropped images before applying the exhaustive search. This is because each image had black borders around the outer edges which heavily influenced the metrics, as it would optimize trying to align the black pixels with each other as a way to improve the score. Taking the center 80% of the image, removing the borders, improved image quality heavily. We then use the displacement that we get from the cropped images and apply it to the uncropped images, to get the final result:

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_1/tobolsk.jpg" title="tobolsk" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            tobolsk <br>
            r displacement: (12, 3) <br>
            g displacement: (5, 2)
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_1/cathedral.jpg" title="cathedral" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            cathedral <br>
            r displacement: (3, 2) <br>
            g displacement: (-3, 2)
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_1/monastery.jpg" title="monastery" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            monastery <br>
            r displacement: (6, 3) <br>
            g displacement: (3, 3)
        </div>
    </div>
</div>

## Task 2: Image Pyramid

With larger images however, an exhaustive search would take too much time. After all, it's an N^2 runtime. Some images had an optimal offset in the 100s, and increasing the search range to 100 would require 40000+ calls to normalized cross correlation for each alignment.

Therefore, we'll use an image pyramid in order to speed up the runtime, with little sacrifice in how we run the search.

1. First, we scale down the image in factors of 2 until we reach a low enough resolution. Here, we specify this as having a width or height below 360 pixels.
2. We run our exhaustive search algorithm on this scaled down image, with a search range of -36 and 36. This gives us the optimal displacement for this scaled down image.
3. Take the current optimal displacement and double it in both directions. Halve the search range and scale up the image by 2x in each direction and rerun the exhaustive search, searching in the range centered around our current optimal displacement.
4. Repeat step 3 until we reach the original image's resolution, and return the optimal displacement.

As it's much faster to compute the metric when our image is small, this method is way faster and still allows us to search a huge range of our image for an optimal displacement.

For the large images in particular, cropping was essential. Cropping away 20% of the edges ensured that only the important center areas of each image was used to determine if an alignment is appropriate, resulting in images with far better alignments. Cropping also had the secondary effect of reducing the image size, reducing the number of times we need to scale down.

The results were promising, and each image took at most 40 seconds to align.

<div class="row justify-content-sm-center">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path="/assets/img/CS180/Project_1/large_church.jpg" title="Church" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Church <br>
            r displacement: (59, -4) <br>
            g displacement: (25, 4)
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path="/assets/img/CS180/Project_1/large_emir.jpg" title="Emir" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Melons <br>
            r displacement: (103, 55) <br>
            g displacement: (49, 24)
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path="/assets/img/CS180/Project_1/large_harvesters.jpg" title="Harvesters" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Harvesters <br>
            r displacement: (124, 13) <br>
            g displacement: (59, 16)
        </div>
    </div>
</div>
<div class="row justify-content-sm-center">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path="/assets/img/CS180/Project_1/large_icon.jpg" title="Icon" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Icon <br>
            r displacement: (89, 23) <br>
            g displacement: (41, 17)
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path="/assets/img/CS180/Project_1/large_lady.jpg" title="Lady" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Lady <br>
            r displacement: (112, 11) <br>
            g displacement: (51, 9)
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path="/assets/img/CS180/Project_1/large_melons.jpg" title="Melons" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Melons <br>
            r displacement: (58, -4) <br>
            g displacement: (25, 4)
        </div>
    </div>
</div>
<div class="row justify-content-sm-center">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path="/assets/img/CS180/Project_1/large_onion_church.jpg" title="Onion Church" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Onion Church <br>
            r displacement: (139, -26) <br>
            g displacement: (33, -11)
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path="/assets/img/CS180/Project_1/large_sculpture.jpg" title="Sculpture" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Monastery <br>
            r displacement: (130, -26) <br>
            g displacement: (33, -11)
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path="/assets/img/CS180/Project_1/large_self_portrait.jpg" title="Self Portrait" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Self Portrait <br>
            r displacement: (141, 33) <br>
            g displacement: (78, 29)
        </div>
    </div>
</div>
<div class="row justify-content-sm-center">
    <div class="col-sm mt-3 mt-md-0">
       {% include figure.liquid path="/assets/img/CS180/Project_1/large_three_generations.jpg" title="Three Generations" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Three Generations <br>
            r displacement: (112, 11) <br>
            g displacement: (53, 14)
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path="/assets/img/CS180/Project_1/large_train.jpg" title="Train" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Train <br>
            r displacement: (87, 32) <br>
            g displacement: (42, 5)
        </div>
    </div>
</div>