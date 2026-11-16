import io
import os
from orangecanvas.scheme.readwrite import parse_ows_stream

ows_xml = """<?xml version="1.0" encoding="utf-8"?>
<scheme version="2.0" title="Marine Condition Analysis and Classification">
  <nodes>
    <node id="0" name="File" position="(80, 200)" project_name="Orange3" qualified_name="Orange.widgets.data.owfile.OWFile" title="File (data/cleaned_core.csv)"/>
    <node id="1" name="Data Info" position="(220, 90)" project_name="Orange3" qualified_name="Orange.widgets.data.owdatainfo.OWDataInfo" title="Data Info"/>
    <node id="2" name="Select Columns" position="(240, 200)" project_name="Orange3" qualified_name="Orange.widgets.data.owselectcolumns.OWSelectColumns" title="Select Columns"/>
    <node id="3" name="Preprocess" position="(390, 200)" project_name="Orange3" qualified_name="Orange.widgets.data.owpreprocess.OWPreprocess" title="Preprocess (Standardize)"/>
    <node id="4" name="k-Means" position="(540, 100)" project_name="Orange3" qualified_name="Orange.widgets.unsupervised.owkmeans.OWKMeans" title="k-Means (k=2)"/>
    <node id="5" name="Scatter Plot" position="(700, 100)" project_name="Orange3" qualified_name="Orange.widgets.visualize.owscatterplot.OWScatterPlot" title="Scatter Plot (Clusters)"/>
    <node id="6" name="Tree" position="(540, 240)" project_name="Orange3" qualified_name="Orange.widgets.model.owtree.OWTree" title="Tree (depth 5, leaf 20)"/>
    <node id="7" name="Random Forest" position="(540, 340)" project_name="Orange3" qualified_name="Orange.widgets.model.owrandomforest.OWRandomForest" title="Random Forest (100 trees)"/>
    <node id="8" name="Naive Bayes" position="(540, 440)" project_name="Orange3" qualified_name="Orange.widgets.model.ownaivebayes.OWNaiveBayes" title="Naive Bayes"/>
    <node id="9" name="Test and Score" position="(720, 310)" project_name="Orange3" qualified_name="Orange.widgets.evaluate.owtestandscore.OWTestAndScore" title="Test and Score (10-Fold CV)"/>
    <node id="10" name="Confusion Matrix" position="(880, 310)" project_name="Orange3" qualified_name="Orange.widgets.evaluate.owconfusionmatrix.OWConfusionMatrix" title="Confusion Matrix"/>
  </nodes>
  <links>
    <link id="0" source_node_id="0" sink_node_id="1" source_channel="Data" sink_channel="Data" enabled="true"/>
    <link id="1" source_node_id="0" sink_node_id="2" source_channel="Data" sink_channel="Data" enabled="true"/>
    <link id="2" source_node_id="2" sink_node_id="3" source_channel="Features" sink_channel="Data" enabled="true"/>
    <link id="3" source_node_id="3" sink_node_id="4" source_channel="Data" sink_channel="Data" enabled="true"/>
    <link id="4" source_node_id="4" sink_node_id="5" source_channel="Data" sink_channel="Data" enabled="true"/>
    <link id="5" source_node_id="3" sink_node_id="9" source_channel="Data" sink_channel="Data" enabled="true"/>
    <link id="6" source_node_id="6" sink_node_id="9" source_channel="Learner" sink_channel="Learner" enabled="true"/>
    <link id="7" source_node_id="7" sink_node_id="9" source_channel="Learner" sink_channel="Learner" enabled="true"/>
    <link id="8" source_node_id="8" sink_node_id="9" source_channel="Learner" sink_channel="Learner" enabled="true"/>
    <link id="9" source_node_id="9" sink_node_id="10" source_channel="Evaluation Results" sink_channel="Evaluation Results" enabled="true"/>
  </links>
</scheme>"""

def build_ows():
    stream = io.BytesIO(ows_xml.encode("utf-8"))
    res = parse_ows_stream(stream)
    print(f"Verified parse_ows_stream! Nodes: {len(res.nodes)}, Links: {len(res.links)}, Title: {res.title}")
    
    out_file = "marine_project.ows"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(ows_xml)
    print(f"Successfully wrote verified {out_file}!")

if __name__ == "__main__":
    build_ows()
