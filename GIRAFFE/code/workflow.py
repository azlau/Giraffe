#This is a Nipype generator. Warning, here be dragons.
#!/usr/bin/env python

import sys
import nipype
import nipype.pipeline as pe

import nipype.interfaces.io as io
import nipype.interfaces.fsl as fsl

#Flexibly collect data from disk to feed into workflows.
io_select_files = pe.Node(io.SelectFiles(templates={'func':'func.nii.gz'}), name='io_select_files')
io_select_files.inputs.base_directory = '/data'
io_select_files.inputs.func = 'func.nii.gz'

#Wraps the executable command ``fslroi``.
fsl_extract_roi = pe.Node(interface = fsl.ExtractROI(), name='fsl_extract_roi')
fsl_extract_roi.inputs.t_min = 0
fsl_extract_roi.inputs.t_size = 1

#Generic datasink module to store structured outputs
io_data_sink = pe.Node(interface = io.DataSink(), name='io_data_sink')
io_data_sink.inputs.base_directory = '/data/results'

#Create a workflow to connect all those nodes
analysisflow = nipype.Workflow('MyWorkflow')
analysisflow.connect(io_select_files, "func", fsl_extract_roi, "in_file")
analysisflow.connect(fsl_extract_roi, "roi_file", io_data_sink, "extract")

#Run the workflow
plugin = 'MultiProc' #adjust your desired plugin here
plugin_args = {'n_procs': 1} #adjust to your number of cores
analysisflow.write_graph(graph2use='flat', format='png', simple_form=False)
analysisflow.run(plugin=plugin, plugin_args=plugin_args)
