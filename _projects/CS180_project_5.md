---
layout: page
title: CS180 Project 5
description: Fun Wth Diffusion Models!
img: assets/img/CS180/Project_5/Part_1/results/1.11.3_3.png
importance: 1
category: work
related_publications: false
---

# Part A: Pretrained Models

First, we'll use a pretrained model from HuggingFace, with some modifications, to create a variety of AI-generated images.

Let's use the prompts "a man wearing a hat", "a rocket ship", and "an oil painting of a snowy mountain village" for two different num_inference_steps: 20 and 50. Here are the results (seed = 180180180), which were afterwards upsampled for higher resolution:

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.0.4.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Snowy village, steps=20
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.0.5.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Old man, steps=20
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.0.6.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Rocket Ship, steps=20
        </div>
    </div>
</div>

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.0.1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Snowy village, steps=50
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.0.2.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Old man, steps=50
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.0.3.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Rocket Ship, steps=50
        </div>
    </div>
</div>

We can clearly see that a higher number of inference steps provides higher quality/detailed images.

## Task 1: Forward Process

As diffusion models work by essentially denoising a noisy image, our first step is to actually blur an image. We'll use the formula:

$$ x_t = \sqrt{\bar\alpha_t} x_0 + \sqrt{1 - \bar\alpha_t} \epsilon \quad \text{where} \quad \epsilon \sim N(0, 1) $$

To blur an image $$ x_0 $$. The $$ \bar\alpha_t $$ can be adjusted based on a noise level variable that ranges from [0, 1000], with 0 being a clean image and 1000 being pure noise.

With the given test image below, we can try 3 different noise levels:

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.1.1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            test image, blue=0
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.1.2.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            test image, blur=250
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.1.3.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            test image, blur=500
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.1.4.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            test image, blur=750
        </div>
    </div>
</div>

## Task 2: Classical Denoising

Since the noise we added follows a guassian distribution, a simple way to denoise is to simply use a gaussian blur! Theoretically, this would average out much of the noise of the image, and although it'll become blurry we can ignore some of the blur that was added. As we can see below, this works decently well for lower noises but at higher noises, we can really only make out the silhouette of the Campanile.


<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.2.1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            test image, base
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.2.2.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            denoised test image, blur=250
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.2.3.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            denoised test image, blur=500
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.2.4.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            denoised test image, blur=750
        </div>
    </div>
</div>

## Task 3: One Step Denoising

A properly trained diffusion model can pretty accurately predict the noise that was added to any image, and thus by simply subtrating off the estimated noise, we should get a picture that is close to the original image. Using the same formula above, we can perform some algebra to get $$ x_0 $$ from $$ x_t $$ and $$ \epsilon $$, our estimated noise.

$$ x_0 = \frac{x_t - \sqrt{1 - \bar\alpha_t} \epsilon}{\sqrt{\bar\alpha_t}} $$

Here are the results for each of the noise levels above:

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.2.1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            test image, base
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.3.1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            1-step denoised test image, blur=250
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.3.2.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            1-step denoised test image, blur=500
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.3.3.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            1-step denoised test image, blur=750
        </div>
    </div>
</div>

Much better! But the image for the highest noise level is still quite blurry (and doesn't resemble the campanile very well). Can we do better?

## Task 3: Iterative Denoising

Instead of doing all the denoising one step, we can take iterative steps to slowly denoise an image bit by bit, to hopefully get a better result. The formula here:

$$ x_{t'} = \frac{\sqrt{\bar\alpha_{t'}}\beta_t}{1 - \bar\alpha_t} x_0 + \frac{\sqrt{\alpha_t}(1 - \bar\alpha_{t'})}{1 - \bar\alpha_t} x_t + v_\sigma $$

gives us $$ x_t' $$, which should be a slightly more denoised image compared to $$ x_t $$, until we eventually reach $$ x_0 $$, the completely denoised image. Here's the process on our most noisy image for t=750, showing a couple of steps in between. 

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.1.4.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            test image, t=750
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.4_noised_690.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            iteratively denoised test image, t=690
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.4_noised_540.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            iteratively denoised test image, t=540
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.4_noised_390.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            iteratively denoised test image, t=390
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.4_noised_240.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            iteratively denoised test image, t=240
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.4_noised_90.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            iteratively denoised test image, t=90
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.4_blur.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            iteratively denoised test image, t=0 (finished)
        </div>
    </div>
</div>

Here are the 3 different technique's results side by side.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.1.1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            base campanile
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.2.4.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            blur denoised campanile
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.3.3.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            1-step denoised campanile
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.4_clean.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            iteratively denoised campanile
        </div>
    </div>
</div>

We can see that the iteratively denoised campanile provided superior results: in both being less blurry and being more detailed (there are actual couds in the background!). The overall shape was also slightly better.

## Task 4: Diffusion Model Sampling

Now, instead of passing in a blurred image, we can simply pass in what is essentially pure noise and see what the model comes up with.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.5_generated_0.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.5_generated_1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.5_generated_2.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.5_generated_3.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.5_generated_4.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

Without any prompting or a base image to go with, the model just hallucinates some random images out. While we can make out some details in these images (street in the second image, scenery in the third and fourth?) this is mostly nonsense. They do definitely look feasible though, which is impressive.

## Task 5: Classifier-Free Guidance

To improve on the quality and make the images look better, at the cost of "creativity", we can use classifier free guidance. We'll use our model to generate an unconditional prediction of the noise given an image, and a conditional prediction. Then, we can use the magical formula:

$$ \epsilon = \epsilon_u + \gamma (\epsilon_c - \epsilon_u) $$

To get our new noise which we will plug into the same equation above. We can clearly see here that at gamma=0, we just get the unconditional noise. At gamma=1, we get only conditional noise. Somehow, by setting gamma to some large number (we used 7), we get really good images! Here are the results:

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.6_generated_0.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.6_generated_1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.6_generated_2.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.6_generated_3.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.6_generated_4.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

As we can see, the images are now of much higher quality, although the variety has suffered a bit. Most of it has become either close-up shots of people or scenic imagery. 

## Task 6: Image to Image Translation

Now we can do something even more interesting - rather than passing in pure noise, what if we just took an image, add some noise, and then denoise it? This is really similar to what we did in task 3 except we're now also using classifier-free guidance. We'll try this at different noise levels, so that at lower noise levels we'll get images that closely resemble the original image, and at higher noise levels we get almost completely different images instead.

Here are the original images;


<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.1.1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            campanile
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/man.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            my funny cat
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/man_2.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Batman without the Bat
        </div>
    </div>
</div>

And here are the denoised images, from most noise added to least noise added.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.7.1_0.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=1
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.7.1_1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=3
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.7.1_2.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=5
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.7.1_3.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=7
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.7.1_4.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=10
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.7.1_5.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=20
        </div>
    </div>
</div>

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.7.2_0.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=1
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.7.2_1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=3
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.7.2_2.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=5
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.7.2_3.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=7
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.7.2_4.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=10
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.7.2_5.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=20
        </div>
    </div>
</div>

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.7.3_0.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=1
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.7.3_1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=3
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.7.3_2.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=5
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.7.3_3.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=7
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.7.3_4.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=10
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.7.3_5.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=20
        </div>
    </div>
</div>

The Campanile managed to stay pretty much the same even with higher noise levels, but the same couldn't be said for the other images. Perhaps it's because there's more buildings in the training set than the other two - almost immediately my cat became some bear hybrid and although Not-Batman pretty much stayed the same for the first couple of low-noise examples, it quickly became pictures of people again.

## Task 7.1: Handdrawn and Web images

Although the image to image translation didn't work too too well, what the model excels at doing is taking a nonrealistic image and making it into a more natural looking image. We're going to use a couple of hand-drawn image and see how much noise it needs until it becomes a realistic picture, with an additional hyper-realistic image of a flower I found online as I'm curious how much noise needs to be added to that before it becomes something different.

original images:

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.8.2_original.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Drawing 1: (Crown)
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.8.3_original.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Drawing 2: (Bread)
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/flower.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Very nice flower
        </div>
    </div>
</div>


<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.8.2_0.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=1
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.8.2_1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=3
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.8.2_2.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=5
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.8.2_3.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=7
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.8.2_4.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=10
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.8.2_5.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=20
        </div>
    </div>
</div>


<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.8.3_0.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=1
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.8.3_1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=3
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.8.3_2.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=5
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.8.3_3.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=7
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.8.3_4.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=10
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.8.3_5.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=20
        </div>
    </div>
</div>

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.8.1_0.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=1
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.8.1_1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=3
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.8.1_2.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=5
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.8.1_3.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=7
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.8.1_4.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=10
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.8.1_5.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=20
        </div>
    </div>
</div>

Perhaps the most interesting things that happened here was how the crown and bread became ignored starting at i=10, becoming something completely different. Interestingly, the flower became 2 humans at i=7 but then returned as a near-identical flower at i=5, showing the randomness of diffusion models.

## Task 7.2: Inpainting

Next we can attempt something interesting: Make a mask for an image, use the diffusion model to denoise the image, and after each iterative step we'll leave everything inside the mask alone, but replace everything outside the mask with our original image. The end result will be that the denoising uses the surrounding pixels for denoising, but everything outside the mask is left alone.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/inpaint_0.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Campanile
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.9.1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Result
        </div>
    </div>
</div>

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/inpaint_1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            My funny cat
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.9.2.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Result (absolute tragedy)
        </div>
    </div>
</div>

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/inpaint_2.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Not-Batman
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.9.3.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Result (surprisingly good)
        </div>
    </div>
</div>

I intended the cat example to have made the facial expression different or replace it with some other animal, but it ended up looking like some eldritch horror. Truly traumatizing. The not-batman example was amazing though, providing a new face that could very much be a new villain.

## Task 7.3: Text conditioned Image-to-Image Translation

Since we also have some text prompt embeddings loaded in, we can redo our timage to image translation but add some text for the diffusion model to work with. Again, we can use different noise levels for varying levels of editing.

<div class="caption">
    Campanile, prompt: Rocket Ship
</div>

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.10.1_0.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=1
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.10.1_1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=3
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.10.1_2.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=5
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.10.1_3.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=7
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.10.1_4.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=10
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.10.1_5.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=20
        </div>
    </div>
</div>

<div class="caption">
    My funny cat, prompt: dog
</div>

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.10.2_0.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=1
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.10.2_1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=3
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.10.2_2.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=5
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.10.2_3.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=7
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.10.2_4.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=10
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.10.2_5.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=20
        </div>
    </div>
</div>

<div class="caption">
    Not-Batman, prompt: Photo of a Man
</div>

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.10.3_0.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=1
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.10.3_1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=3
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.10.3_2.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=5
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.10.3_3.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=7
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.10.3_4.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=10
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.10.3_5.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            start i=20
        </div>
    </div>
</div>

## Task 8: Visual Anagrams

An even cooler way we can use the diffusion model is to make optical illusions. First, we take two prompts and get noise estimates for each. We then apply one normally and apply the other to a flipped version of the image instead. The result is that we get an image that looks like the original prompt when looked at normally, and something completely different otherwise.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.11.1_1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            An old man
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.11.1_1_flip.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Oil painting of people around a campfire
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.11.2_1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Waterfalls
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.11.2_1_flip.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            A skull
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.11.3_3.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            An old man
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.11.3_3_flip.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            An oil painting of snowy mountains
        </div>
    </div>
</div>


## Task 9: Hybrid 

Lastly, we can combine what we did in the earlier projects and make hybrid images. By using a low pass filter and a high pass filter, we can create hybrid images that will look different when viewed from afar vs viewed from nearby.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.12.1_4.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Closeby: waterfalls
            Far: skull
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.12.2_1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Closeby: waterfalls
            Far: people around a campfire
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_1/results/1.12.3_3.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Closeby: snowy mountains
            Far: skull
        </div>
    </div>
</div>

Trying different combinations of prompts together, it seems like similar prompts gave much much better results than others. The prompts used above all had similar mediums - oil paintings, lithographs, etc. - which made the end result more realistic. 

# Part B: Training our own Model!

All of the above depended on a great diffusion model that HuggingFace created, now, let's make our own simple diffusion model. We can use the DDPM paper to implement a denoiser, providing the model architecture:

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_2/results/arch.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

We need to feed in some noisy images for the model to predict the noise. 

$$ z = x + \sigma \epsilon,\quad \text{where }\epsilon \sim N(0, I). \tag{B.2} $$

We can then optimize over L2 loss.

Here's an example of digits being noised at different levels

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_2/results/noisy_images_grid.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            From left to right: [0.0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0]
        </div>
    </div>
</div>

## Task 1: Training

By noising a bunch of images with sigma=0.5 from the MNIST dataset and performing regression, we can train our model. Here's the training loss curve over 5 epochs, with 256 batch size.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_2/results/training_losses.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

Now, our model is great at denoising mnist images with sigma=0.5! Here are some examples, for our model when we only trained for 1 epoch vs 5 epochs. We can see a clear improvement as we train for longer.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_2/results/1.2.1.1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Model results after 1 epoch
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_2/results/1.2.1.2.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Model results after 5 epochs
        </div>
    </div>
</div>

We can also test to see if it's able to deal with other noise levels. Below, we take one MNIST image and run it through 6 different levels of sigma, then use our model to denoise.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_2/results/1.2.2.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            From left to right: sigma=[0.0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0]. Noised image above, denoised below.
        </div>
    </div>
</div>

As we can see, the model is decent at dealing with lower sigma values but falls short at higher values.

## Task 2: Time Conditioning

To actually train our model, we'll need to add time conditioning. We'll modify our architecture to add two FCBlocks that allow our model to be conditioned based on t. Architecture and training pseudocode below:

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_2/results/time_conditioned.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_2/results/training_time.png" title="camera man" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

We'll train with a batch size of 128 for 20 epochs using an exponential learning rate and the Adam optimizer. Here's the training curve:

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_2/results/2.2.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Training curve for time conditioned UNet
        </div>
    </div>
</div>

Now, we can sample form the Unet by passing in some pure noise and see what it comes up with. The algorithm for sampling is showed below, along with the results for 40 different tries at epoch 5 and at epoch 20.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_2/results/sampling.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Sampling Algorithm
        </div>
    </div>
</div>

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_2/results/2.2.2.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Samples at epoch=5
        </div>
    </div>
</div>

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_2/results/2.2.5.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Samples at epoch=20
        </div>
    </div>
</div>

We can see that at epoch 20, our digits are much much better - there's way fewer artifacts and lots of pretty well drawn numbers. It's still not perfect though, and there are many nonsense digits. Can we do better?

## Task 3: Class Conditioning

In addition to time conditioning, we can add 2 more FCBlocks to take in a class - the digit we want to create. We'd want to one-hot encode the digit first and pass in an array of size 10, one slot for each digit, and set the array to 1 at the index for the digit we want to generate. While training, we'll also take a 10% chance to drop the entire array - so that it's all 0s - so that the UNet can still perform unconditioned sampling. We'll then use the same technique above with CFG and denoise using 

$$ \epsilon = \epsilon_u + \gamma (\epsilon_c - \epsilon_u) $$

with a gamma of 5, to get our digit.

Here's the training curve over 20 epochs:

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_2/results/3.1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Class and Time conditioned Training Losses
        </div>
    </div>
</div>

And the results, for epoch 5 and 20, where we try each digit 4 times:

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_2/results/3.2.1.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Class conditioned sampling, epochs=5
        </div>
    </div>
</div>

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/CS180/Project_5/Part_2/results/3.2.2.png" title="camera man" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Class conditioned sampling, epochs=20
        </div>
    </div>
</div>

The accuracy at epoch=20 was pretty amazing - each digit is clearly visible and although there are a few artifacts, even their thicknesses were pretty uniform.

## Conclusion

Overall, this project was a blast. It's always super satisfying to understand something after being amazed by it for so long. Dall-E has been something I've been playing with since Freshman year and I've always wondered how it works, but never bothered to look deeply into it. This project gave a great introduction and idea of how things work under the hood, and it's exciting to see what generative models will be able to achieve in the years to come.