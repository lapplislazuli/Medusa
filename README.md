# Project Medusa
**Irritating Image-Based AIs with Style**

This Project achieved the 4th place in [2018's Informaticup](https://gi.de/informaticup/) and recieved additional honour for the best scientific elaboration. 

The goal was to produce *false positives* for a street-sign detecting neural network. We accomplished it with 3 different approaches, found in the root-folders of this repository. 
For the quickest intro to this topic, refer to the [*presentation_gi*](/presentation_GI).

The documentation is done in german language only, except for the abstract. The code is done in english. 
## Structure
The [Degeneration](/Degeneration/Degeneration.ipynb) is found in the folder Degeneration. 
It contains an elaborate notebook with additional commentary and conception insights, and it`s readable from your browser. We therefore recommend to first dive in here. 
The *Degeneration.py* holds the same code as a common python file. 
Additional python files are used for several sub-tasks, such as imagealternation and remote-communication. 

[Saliency Maps](/SaliencyMaps/Saliency-Map-Image-Generation.ipynb) contains a jupyter-notebook which performs every required task. 
The used methods for saliency-generation are found in the subfolder *aux_functions* and contain core-logic of this approach. 
The subfolder *data* contains some sample input-images and some sample output for visualisation - so the user doesn`t need to search for the gtsrb-dataset. 

[GradientAscent](/GradientAscent/Gradient-Ascent-Image-Generation.ipynb) contains the training of the AlexNet and performs the gradient-ascent method for every of the 43 classes. 
In the folder *data* there are some example images. 

The folder *Latex* in root contains our [scientific work](https://github.com/Twonki/Medusa/blob/master/Latex/Projekt_Medusa.pdf) and the required tex-files to compile it. 
The only other notable instance there [bib-file}(/Latex/src.bib), which contains all our used sources and further reading.  

The presentations are found in the root-folder, the *presentation_GI* is a slimmed version for the informaticup-jury, while the *presentation* was for the university. 
## Requirements
All sub-projects are build with python in Jupyter-Notebooks. 
The used python version was 3.6 and several anaconda-packages are required. 

The exact required packages are denoted (and downloaded) by the saliency-maps and gradient ascent in the notebooks themselves, 
for degeneration it`s put in the scientific work chapter 3.1 table 3.1, which also summarizes all required technologies in detail. 

To rebuild Aphrodite and the AlexNet you will require the GTRSB data-set.  
For further instructions on training aphrodite see the [trainingfile](/Degeneration/Training.py).

To run the Degeneration you will need a real street-sign in size 64x64, we therefore recommend using the test-data of the gtsrb-set. 
Some images are provided in the degeneration-subfolder *images*
Images from the training-set performed badly, probably due to overfitting of the remote-ai.  

To run the saliency map the whole gtsrb-dataset is used. 
## Contributing 
Please don`t. After our final presentation this repository will be archived. 

However it`s completely open to you, so feel free to fork it and reach out to us.