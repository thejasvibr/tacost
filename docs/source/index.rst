TACOST: Test ACOustic Tracking
============================

`tacost` allows you to test and characterise the accuracy of your acoustic tracking system. 
It allows you to create audio recordings to simulate sound emission from known points of your choice,
and uncover the maximum expected accuracy of your acoustic tracking system.

What TACOST does
>>>>>>>>>>>>>>>>

* Creates audio files which simulate sound arrival at each microphone in an array from user-specified points

* Allows customisation of multiple parameters that may affect acoustic tracking accuracy

What TACOST does `not` do
>>>>>>>>>>>>>>>>>>>>>>>>>

* Perform the actual acoustic tracking. You need to use a separate system (eg. TOADSuite, Batalef, or the
  tracking system of your choice)

* Simulate complex sound propagation (reflection, reverberation,etc). Sound is assumed to travel 
  in straight line paths. In version 0.0.1 there's no spherical spreading too!

About the logo
>>>>>>>>>>>>>>
The two T's in the logo are tristar arrays (shaped like T's) with four microphones each on them 
(blue dots). The red dots are positions from where sound was emitted. In this case, I like to 
imagine it to be a bat's calls as it flew past two arrays!

Getting started
>>>>>>>>>>>>>>>

Creating an audio file to test your system is as simple as opening up your shell/command line and typing:

.. code-block:: shell

   python -m tacost -run_example


The command above will generate a four channel WAV file with `X` Hz sampling rate based on the default array geometry and source positions. 
See the page on default array geometry and source position. 

Installation
>>>>>>>>>>>>
`tacost` is currently pre-PyPi and it'll be some time before you can :code:`pip install tacost`!
However, you `can` use :code:`tacost` with a local install! Head `here https://github.com/thejasvibr/tacost` and download the repo. From the downloaded
repo open up a shell/prompt and type :code:`pip install ./` . 

.. toctree::
   default_array_source.rst

.. include:: using_paramfile.rst



API Reference 
>>>>>>>>>>>>>
.. automodule:: tacost.simulate_LMU_playback_setup
	:members:

