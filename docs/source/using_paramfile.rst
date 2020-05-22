tacost without coding - the parameter file
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
You can use `tacost` without any coding at all through the parameter file!
All optional parameters can be fine tuned in the 'parameter' file. A parameter file 
is a YAML file. A YAML file basically looks and feels like 
a .txt file, except that it ends with .yml or .yaml. You can make your own parameters file in Windows
by right-clicking and creating a new .txt file, and then changing the extension to .yml! In Unix 
systems you can do this with :code:`touch yourparamfile.yml`. 

A basic parameter file consists of the parameter to be specified and the entry in one row separated by a colon. 
If a certain parameter is not specified explicitly by the user, the default value is assumed. This can either save you 
a lot of work OR add a lot of agony - so please check the default values for each parameter to see if they make sense for 
your use case. 

Using tacost
<<<<<<<<<<<<
This is what an example parameter file would look like if you wanted the emitted sound 
to be a bird call (stored in a wav file), the final audio to have a sampling rate of 44.1kHz,
and to generate the simulated sound arrival for your own
microphone array. You also want to name this simulation run is called 'birdsim'. This is what your parameter file would look like. 

:code:`yourparameterfile.yml` :

.. code-block:: shell

	array_geometry : agm_yourcoolgeometry.csv
	sample_rate    : 44100            
	source_sound   : bird_call.wav     	
	sim_name       : bird_sim             

Next, open up your Command Prompt (Windows)  or Terminal (Unix)
and feed the parameter file into `tacost` with the simple command below

.. code-block:: shell
   
   python -m tacost -paramfile yourparameterfile.yml

And voila - you should get a wav file named :code:`bird_sim.wav` that simulates sound sources as recorded by the mics in your cool array geometry. 
The sound simulated will the audio in the `bird_call.wav` file as played back from each of the positions. Here the default LMU position set is 
used because the source positions were not explicitly specified.

`Attention`
-----------
As of version 0.0.1 there is `no` spherical spreading or atmospheric absorption implemented in `tacost`. Only the time of arrivals 
are calculated. This means `tacost` is a tool for testing the `inherent` accuracy of your tracking system over different parts of space. 
Acoustic arrays are known to have non-uniform accuracies - and these may be picked up for your own custom array! `tacost` allows
you to uncover the tracking accuracies under 'best case' scenarios, and not so much the real-world performance of your system. 

You could of course implement a form of spherical spreading or atmospheric absorption by using a scaled version of the same source sound (see source sound). The better
alternative is to interact with `tacust` through a script of course.

Array geometry
<<<<<<<<<<<<<<

.. code-block:: shell

	array_geometry : agm_yourownarraygeometry.csv

`Attention` :  An array geometry file must contain at least 2 microphones with their x,y,z positions.
The first row of the array geometry file must be named (eg.'x', 'y' and 'z') with each microphone 
in a separate row. 

Source positions
<<<<<<<<<<<<<<<<

.. code-block:: shell

	source_position : sourcepos_yourownsourcepositions.csv

`Attention` :  An source position file must contain at least 1 position with its x,y,z positions.
The first row of the source position file must be named (eg.'x', 'y' and 'z') with each source position  
in a separate row. 


Sampling rate
<<<<<<<<<<<<<
By default the sampling rate is set to 500 kHz (because, the package author works with ultrasound a lot).
To set it to 44.1kHz for instance - add this in the parameter file. 

.. code-block:: shell
	
	sample_rate: 44100



Source sound
<<<<<<<<<<<<<
By default the sound assumed to be emitted is a linear frequency modulated chirp. 
You can provide your own sound in the form of a wav file. In the parameter file 
the entry would be 

.. code-block:: shell

	source_sound: example_sound.wav


`Attention` : The sampling rate of the input wav file `must` match the sampling rate of the output wav file! There is no
explicit checking for a match between the default/user-set final sampling rate and the source sound's sampling rate.

Inter-sound interval
<<<<<<<<<<<<<<<<<<<<
Each simulated source position corresponds to a single sound in the multichannel audio file. 
The time gap between one sound to the next is the inter-sound interval. The default value is 
100ms, and it can be specified in seconds so:

.. code-block:: shell

	intersound_interval: 0.05


Here the inter sound interval has been set to 50ms.

Signal-to-Noise-Ratio
<<<<<<<<<<<<<<<<<<<<<
By default the signal-to-noise ratio of the emitted sound is assumed to be very high (>120dB). 
If you wish to set it to something else, then enter the SNR of your choice like so:

.. code-block:: shell

	sound_snr: [30]

Here we've set the overall SNR to 30dB for all channels. 
`Note` : SNR values must be set inside a list (within square brackets). If all channels are to have the same SNR values,
then one value in a list is enough.

If you'd like to define channel-specific SNR's then specify unique values for each  channel, eg:
 
.. code-block:: shell

	sound_snr: [30, 20, 10,40]