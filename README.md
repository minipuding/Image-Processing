A simple image processing app (emm..., it is also a homework...). There are four page including,

- **Threshold**, like Otsu, Entropy

- **Filters**, like classical edge operators (sobel, prewitt, robert), classical filters (mean filter, median filter, gaussian filter), you can define the filter by youself.

- **Morphological Operations**, like dilation, erosion, opening and closing for both binary image and grascale image. You can change the structure element shape, size and origin even defined by youself.

- **Morphological Functions**, like distance transform, skeleton extraction, distance reconstruction, edge detection by morphological methods and conditional dilation for binary image. There are also morphological reconstruction and gradient detection for grayscale image.

## Functions

### 0. Basic Functions

- Input image

- export result image

- send to other pages

> !['send to' windows](https://github.com/minipuding/Image-Processing/blob/main/Homework01/resource/images/2022-05-05-14-35-07-image.png)

### 1. Threshold Page

![threshold image](https://github.com/minipuding/Image-Processing/blob/main/Homework01/resource/images/2022-05-05-14-14-12-image.png)

- show threshold image

- show histgram

- apply Otsu algorithm

- apply Entropy algorithm

### 2. Filters Page

![sobel operation](https://github.com/minipuding/Image-Processing/tree/main/Homework01/resource/images/2022-05-05-15-05-41-image.png)

![gaussian filter](https://github.com/minipuding/Image-Processing/tree/main/Homework01/resource/images/2022-05-05-14-36-26-image.png)

![user-defined filter](https://github.com/minipuding/Image-Processing/tree/main/Homework01/resource/images/2022-05-05-15-07-00-image.png)

- apply roberts operation and show them

- apply prewitt operation and show them

- apply sobel operation and show them

- apply mean filter, change filter size and show them

- apply median filter, change filter size and show them

- apply gaussian filter, change filter size, change sigma and show them

- apply user defined filter, change size and show them

### 3. Morphological Operations Page

![dilation of binary image](https://github.com/minipuding/Image-Processing/tree/main/Homework01/resource/images/2022-05-05-14-48-48-image.png)

![closing of grayscale image](https://github.com/minipuding/Image-Processing/tree/main/Homework01/resource/images/2022-05-05-14-50-12-image.png)

- apply dilation operation

- apply erosion operation

- apply opening operation

- apply closing operation

- change shape of structure element  and show

- change origin of structure element and show

- change size (width and height) of structure element and show

- show result with colorful difference (checkbox -- 'Show Diff')

### 4. Motphological Functions Page

![distance transform](https://github.com/minipuding/Image-Processing/tree/main/Homework01/resource/images/2022-05-05-14-51-36-image.png)

![skeleton extraction](https://github.com/minipuding/Image-Processing/tree/main/Homework01/resource/images/2022-05-05-14-52-08-image.png)

![edge detection](https://github.com/minipuding/Image-Processing/tree/main/Homework01/resource/images/2022-05-05-14-52-31-image.png)

![conditional dilation](https://github.com/minipuding/Image-Processing/tree/main/Homework01/resource/images/2022-05-05-14-53-13-image.png)

![OBR](https://github.com/minipuding/Image-Processing/tree/main/Homework01/resource/images/2022-05-05-14-54-39-image.png)

![gradient extraction](https://github.com/minipuding/Image-Processing/tree/main/Homework01/resource/images/2022-05-05-14-55-10-image.png)

- apply distance transform with chess coard, city block and Euclidian

- apply skeleton extraction with animation

- apply skeleton reconstruction

- apply edge detection with external, internal and standard

- apply morphological reconstruction for binary image (conditional dilation)

- apply morphological reconstruction for grayscale image (opening by reconstruction, OBR or closing by reconstruction, CBR)

- apply gradient extraction with internal gradient and external gradient.
