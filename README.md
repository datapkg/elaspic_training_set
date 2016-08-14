# Readme

## Flowchart

<div align="center" >
<p><b>Core</b></p>
<img src='http://g.gravizo.com/g?
 digraph G {
  elaspic_standalone_core -> core_load_data;
  elaspic_training_core -> core_load_data;
  core_load_data -> core_data_statistics;
  core_load_data -> core_vs_interface_data_statistics;
  core_load_data -> core_machine_learning;
 }
'/>

<br><br><br>

<p><b>Interface</b></p>
<img src='http://g.gravizo.com/g?
 digraph G {
  elaspic_standalone_interface -> interface_load_data;
  elaspic_training_interface -> interface_load_data;
  interface_load_data -> interface_data_statistics;
  interface_load_data -> core_vs_interface_data_statistics;
  interface_load_data -> interface_machine_learning;
 }
'/>
</div>
