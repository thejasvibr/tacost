TACOST: Test ACOustic Tracking
============================

`tacost` allows you to thoroughly test your acoustic tracking system. 
It allows you to create audio recordings to simulate sound emission from 
points of your choice, and thus allow you to test the ins and outs of your 
acoustic tracking system of choice. 

Getting started
>>>>>>>>>>>>>>>

Creating an audio file to test your system is as simple as opening up your shell/command line and typing:

`NOTYETIMPLEMENTED!!`

.. code-block:: shell

   python -m tacost -example_track


The command above will generate a four channel WAV file with `X` Hz sampling rate based on the default array geometry and source positions. 
See the page on default array geometry and source position. 

.. toctree::
   default_array_source.rst

.. include:: using_paramfile.rst



API Reference 
>>>>>>>>>>>>>
.. automodule:: tacost.simulate_LMU_playback_setup
	:members:

