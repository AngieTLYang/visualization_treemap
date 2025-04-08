import os
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

def create_treemap_app(file, port):
    script_directory = os.path.dirname(os.path.abspath(__file__))  # Directory where the script is located
    file_path = os.path.join(script_directory, file)

    try:
        data = pd.read_csv(file_path)
        print(f"File {file} loaded successfully!")
    except FileNotFoundError:
        print(f"File not found at {file_path}. Please check the path.")

    targets = ['mean_ghgs', 'mean_land', 'mean_watuse', 'mean_eut', 'mean_bio', 'mean_acid']
    treemaps = []

    for target in targets:
        treemap = px.treemap(
            data,
            path=['sex', 'diet_group', 'age_group'],  # Adjust hierarchy as needed
            values=target,  # Target metric for sizing rectangles
            color=target,  # Target metric for coloring rectangles
            color_continuous_scale=px.colors.sequential.Turbo,  # Vibrant color scale
            title=f'Treemap for {target}'
        )
        treemaps.append(treemap)

    app = Dash(__name__)

    app.layout = html.Div([
        html.H1(f"Environmental Impact Treemaps for {file}", style={"textAlign": "center"}),
        *[dcc.Graph(figure=fig) for fig in treemaps]  # Dynamically add all treemaps
    ])

    app.run(debug=True, port=port)
