from pytz import timezone

DOCKER_IMAGES = {
    "cpu": {
        "tensorflow": "russellcloud/tensorflow:latest-py3",
        "tensorflow:py2": "russellcloud/tensorflow:latest-py2",
        "theano": "russellcloud/theano:latest-py3",
        "theano:py2": "russellcloud/theano:latest-py2",
        "keras": "russellcloud/tensorflow:latest-py3",
        "keras:py2": "russellcloud/tensorflow:latest-py2",
        "caffe": "russellcloud/caffe:latest-py3",
        "caffe:py2": "russellcloud/caffe:latest-py2",
        "torch": "russellcloud/torch:latest-py3",
        "torch:py2": "russellcloud/torch:latest-py2",
        "pytorch": "russellcloud/pytorch:latest-py3",
        "pytorch:py2": "russellcloud/pytorch:latest-py2",
        "chainer": "russellcloud/chainer:latest-py3",
        "chainer:py2": "russellcloud/chainer:latest-py2",
        "mxnet:py2": "russellcloud/mxnet:latest-py2",
        "kur": "russellcloud/kur:latest-py3",
    },
    "gpu": {
        "tensorflow": "russellcloud/tensorflow:latest-gpu-py3",
        "tensorflow:py2": "russellcloud/tensorflow:latest-gpu-py2",
        "theano": "russellcloud/theano:latest-gpu-py3",
        "theano:py2": "russellcloud/theano:latest-gpu-py2",
        "keras": "russellcloud/tensorflow:latest-gpu-py3",
        "keras:py2": "russellcloud/tensorflow:latest-gpu-py2",
        "caffe": "russellcloud/caffe:latest-gpu-py3",
        "caffe:py2": "russellcloud/caffe:latest-gpu-py2",
        "torch": "russellcloud/torch:latest-gpu-py3",
        "torch:py2": "russellcloud/torch:latest-gpu-py2",
        "pytorch": "russellcloud/pytorch:latest-gpu-py3",
        "pytorch:py2": "russellcloud/pytorch:latest-gpu-py2",
        "chainer": "russellcloud/chainer:latest-gpu-py3",
        "chainer:py2": "russellcloud/chainer:latest-gpu-py2",
        "mxnet:py2": "russellcloud/mxnet:latest-gpu-py2",
        "kur": "russellcloud/kur:latest-gpu-py3",
    }
}

DEFAULT_DOCKER_IMAGE = "floydhub/tensorflow:latest-py3"

PST_TIMEZONE = timezone("Asia/Shanghai")

DEFAULT_FLOYD_IGNORE_LIST = """
# Directories to ignore when uploading code to floyd
# Do not add a trailing slash for directories

.git
.eggs
eggs
lib
lib64
parts
sdist
var
"""

CPU_INSTANCE_TYPE = "cpu_high"
GPU_INSTANCE_TYPE = "gpu_high"

FIRST_STEPS_DOC = """
Start by cloning the sample project
    git clone https://github.com/russellcloud/tensorflow-examples.git
    cd tensorflow-examples

And create a russell project inside that.
    russell create --project example-proj
"""

# SimCity4 Loading messages
# https://www.gamefaqs.com/pc/561176-simcity-4/faqs/22135
# Credits: EA Games
LOADING_MESSAGES = [
    "Adding Hidden Layers",
    "Adjusting Bell Curves",
    "Aesthesizing Industrial Grade Containers",
    "Aligning Covariance Matrices",
    "Applying Feng Shui Backprops",
    "Applying Theano Soda Layer",
    "Asserting Packed Exemplars",
    "Attempting to Lock Back-Buffer",
    "Binding Sampling Root System",
    "Breeding Neural Nets",
    "Building Deep Data Trees",
    "Bureacritizing Deep Learning Bureaucracies",
    "Calculating Inverse Probability Matrices",
    "Calculating SGD Expectoration Trajectory",
    "Calibrating Blue Skies",
    "Charging Ozone Layer",
    "Coalescing Cloud Formations",
    "Cohorting Exemplars",
    "Collecting Meteor Particles",
    "Compounding Inert Tessellations",
    "Compressing Fish Files",
    "Computing Optimal Bin Packing",
    "Concatenating Sub-Contractors",
    "Containing Existential Buffer",
    "Debarking Ark Ramp",
    "Debunching Unionized Commercial Services",
    "Deciding What Message to Display Next",
    "Decomposing Singular Values",
    "Decrementing Tectonic Plates",
    "Deleting Ferry Routes",
    "Depixelating Inner Mountain Surface Back Faces",
    "Depositing Slush Funds",
    "Destabilizing Economic Indicators",
    "Determining Width of Blast Fronts",
    "Deunionizing Bulldozers",
    "Dicing Trained Models",
    "Diluting Livestock Nutrition Variables",
    "Downloading Satellite Terrain Data",
    "Exposing Flash Variables to Streak System",
    "Extracting Gradient Resources",
    "Factoring Pay Scale",
    "Fixing Election Outcome Matrix",
    "Flood-Filling Ground Water",
    "Flushing Pipe Network",
    "Gathering Particle Sources",
    "Generating Scheduled Jobs",
    "Gesticulating Mimes",
    "Graphing Container Migration",
    "Hiding Willio Webnet Mask",
    "Implementing Impeachment Routine",
    "Increasing Accuracy of RCI Simulators",
    "Increasing Neural Magmafacation",
    "Initializing My Sim Tracking Mechanism",
    "Initializing CNN Timetable",
    "Initializing Robotic Click-Path AI",
    "Inserting Sublimated Messages",
    "Integrating Multidimensional Curves",
    "Integrating Illumination Form Factors",
    "Integrating Population Graphs",
    "Iterating Cellular Automata",
    "Lecturing Errant Subsystems",
    "Mixing Dropouts in Genetic Pool",
    "Modeling Object Components",
    "Mopping Occupant Leaks",
    "Normalizing Power",
    "Obfuscating Quigley Matrix",
    "Overconstraining Dirty Industry Calculations",
    "Partitioning City Grid Singularities",
    "Perturbing Matrices",
    "Pixalating Overfitting Patches",
    "Polishing Water Highlights",
    "Populating Lot Templates",
    "Preparing Sprites for Random Walks",
    "Prioritizing Landmarks",
    "Projecting Law Enforcement Pastry Intake",
    "Realigning Alternate Time Frames",
    "Reconfiguring User Mental Processes",
    "Relaxing Splines",
    "Removing Road Network Speed Bumps",
    "Removing Texture Gradients",
    "Removing Vehicle Avoidance Behavior",
    "Resolving GUID Conflict",
    "Reticulating Splines",
    "Retracting Phong Shader",
    "Retrieving from Back Store",
    "Reverse Engineering Image Consultant",
    "Routing Neural Network Infanstructure",
    "Scrubbing Terrain",
    "Searching for Llamas",
    "Seeding Architecture Simulation Parameters",
    "Sequencing Particles",
    "Setting Advisor Moods",
    "Setting Inner Deity Indicators",
    "Setting Universal Physical Constants",
    "Sonically Enhancing Occupant-Free Timber",
    "Speculating Stock Market Indices",
    "Splatting Transforms",
    "Stratifying Ground Layers",
    "Sub-Sampling Water Data",
    "Synthesizing Gravity",
    "Synthesizing Wavelets",
    "Time-Compressing Simulator Clock",
    "Unable to Reveal Current Activity",
    "Weathering Buildings",
    "Zeroing Crime Network"
]
