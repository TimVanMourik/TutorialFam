#This is a Nipype generator. Warning, here be dragons.
#!/usr/bin/env python

import sys
import nipype
import nipype.pipeline as pe

import nipype.interfaces.io as io
import nipype.interfaces.fsl as fsl
import nipype.interfaces.spm as spm

#Flexibly collect data from disk to feed into workflows.
io_SelectFiles = pe.Node(io.SelectFiles(templates={'func':'{subj_id}/func/filtered_func_data_run*.nii','anat':'{subj_id}/anat/anat.nii'}), name='io_SelectFiles', iterfield = ['subj_id'])
io_SelectFiles.inputs.base_directory = '/project/3015003.04/TutorialFam/SubjectData'
io_SelectFiles.inputs.func = '{subj_id}/func/filtered_func_data_run*.nii'
io_SelectFiles.inputs.anat = '{subj_id}/anat/anat.nii'
io_SelectFiles.iterables = [('subj_id', ['sub-001', 'sub-002'])]

#Wraps the executable command ``bet``.
fsl_BET = pe.Node(interface = fsl.BET(), name='fsl_BET')

#Use spm_realign for estimating within modality rigid body alignment
spm_Realign = pe.Node(interface = spm.Realign(), name='spm_Realign')

#Wraps the executable command ``flirt``.
fsl_FLIRT = pe.Node(interface = fsl.FLIRT(), name='fsl_FLIRT')

#Generic datasink module to store structured outputs
io_DataSink = pe.Node(interface = io.DataSink(), name='io_DataSink')
io_DataSink.inputs.base_directory = '/project/3015003.04/TutorialFam/Results'

#Create a workflow to connect all those nodes
analysisflow = nipype.Workflow('MyWorkflow')
analysisflow.connect(io_SelectFiles, "anat", fsl_BET, "in_file")
analysisflow.connect(io_SelectFiles, "func", spm_Realign, "in_files")
analysisflow.connect(spm_Realign, "mean_image", fsl_FLIRT, "reference")
analysisflow.connect(fsl_BET, "out_file", fsl_FLIRT, "in_file")
analysisflow.connect(fsl_FLIRT, "out_file", io_DataSink, "coregistered")
analysisflow.connect(spm_Realign, "realigned_files", io_DataSink, "mc_files")

#Run the workflow
plugin = 'MultiProc' #adjust your desired plugin here
plugin_args = {'n_procs': 1} #adjust to your number of cores
analysisflow.write_graph(graph2use='flat', format='png', simple_form=False)
analysisflow.run(plugin=plugin, plugin_args=plugin_args)
