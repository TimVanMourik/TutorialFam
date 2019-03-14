#This is a Nipype generator. Warning, here be dragons.
#!/usr/bin/env python

import sys
import nipype
import nipype.pipeline as pe

import nipype.interfaces.io as io
import nipype.interfaces.fsl as fsl
import nipype.interfaces.spm as spm

#Flexibly collect data from disk to feed into workflows.
io_SelectFiles = pe.Node(io.SelectFiles(templates={}), name='io_SelectFiles')

#Wraps the executable command ``bet``.
fsl_BET = pe.Node(interface = fsl.BET(), name='fsl_BET')

#Use spm_realign for estimating within modality rigid body alignment
spm_Realign = pe.Node(interface = spm.Realign(), name='spm_Realign')

#Wraps the executable command ``flirt``.
fsl_FLIRT = pe.Node(interface = fsl.FLIRT(), name='fsl_FLIRT')

#Generic datasink module to store structured outputs
io_DataSink = pe.Node(interface = io.DataSink(), name='io_DataSink')

#Create a workflow to connect all those nodes
analysisflow = nipype.Workflow('MyWorkflow')


#Run the workflow
plugin = 'MultiProc' #adjust your desired plugin here
plugin_args = {'n_procs': 1} #adjust to your number of cores
analysisflow.write_graph(graph2use='flat', format='png', simple_form=False)
analysisflow.run(plugin=plugin, plugin_args=plugin_args)
