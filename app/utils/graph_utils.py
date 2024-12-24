import json
from typing import Dict, Any
import plotly.graph_objs as go
import plotly


def create_target_preferences_graph(data: Dict[str, Any]) -> Dict:
    preferences = data.get('target_preferences', {})
    traces = []
    for group_name, targets in preferences.items():
        sorted_targets = sorted(targets.items(), key=lambda x: x[1], reverse=True)
        target_names = [t[0] for t in sorted_targets]
        percentages = [t[1] for t in sorted_targets]

        trace = go.Bar(
            name=group_name,
            x=target_names,
            y=percentages,
            text=[f"{p:.1f}%" for p in percentages],
            textposition='auto',
        )
        traces.append(trace)

    layout = go.Layout(
        title='Target Preferences by Group',
        xaxis={
            'title': 'Target Type',
            'tickangle': 45
        },
        yaxis={
            'title': 'Percentage of Attacks',
            'range': [0, 100]
        },
        barmode='group',
        showlegend=True,
        legend={
            'orientation': 'h',
            'yanchor': 'bottom',
            'y': -0.5,
            'xanchor': 'center',
            'x': 0.5
        },
        margin={
            'b': 150
        },
        height=800,
        width=1200
    )

    fig = go.Figure(data=traces, layout=layout)

    summary = data.get('summary', {})
    annotations = [
        f"Total Groups: {summary.get('total_groups', 0)}",
        f"Groups with Similarities: {summary.get('groups_with_similarities', 0)}",
        f"Average Similarity Score: {summary.get('average_similarity_score', 0):.1f}%"
    ]

    for i, annotation in enumerate(annotations):
        fig.add_annotation(
            x=0.02,
            y=0.98 - (i * 0.05),
            xref='paper',
            yref='paper',
            text=annotation,
            showarrow=False,
            align='left',
            bgcolor='rgba(255, 255, 255, 0.8)'
        )

    return json.loads(json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder))































HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Target Preferences Analysis</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body { margin: 0; padding: 20px; font-family: Arial, sans-serif; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { color: #333; }
        #graph { width: 100%; height: 800px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Target Preferences Analysis</h1>
        <div id="graph"></div>
    </div>

    <script>
        // Fetch and display the graph
        async function loadGraph() {
            try {
                const response = await fetch('/v15/api/analysis/target-preferences/graph');
                const graphData = await response.json();
                Plotly.newPlot('graph', graphData.data, graphData.layout);
            } catch (error) {
                console.error('Error loading graph:', error);
            }
        }

        loadGraph();
    </script>
</body>
</html>
"""