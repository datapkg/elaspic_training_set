# Readme

## Notes

Mutation deleteriousness is best correlated with the *raw* ΔΔG values, rather than the *absolute* ΔΔG values.

  - i.e. it's better to use the *raw* score when correlating with humsavar / clinvar / cosmic.

**However**: Provean score is best correlated with the *absolute* ΔΔG value in the core training set, and with the *raw* ΔΔG values in the interface training set.


## Flowchart

<div align="center">
<p><b>Core</b></p>
<img width="600px" src='http://g.gravizo.com/g?
 digraph G {
  standalone_pipeline -> load_data;
  elaspic_database_core -> load_data;
  elaspic_database_interface -> load_data;
  load_data -> data_statistics;
  load_data -> machine_learning;
  machine_learning -> validation
 }
'/>
</div>
