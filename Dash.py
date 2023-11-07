# -*- coding: utf-8 -*-

# Ejecute esta aplicación con 
# python app1.py
# y luego visite el sitio
# http://127.0.0.1:8050/ 
# en su navegador.

import dash
from dash import dcc  # dash core components
from dash import html # dash html components
from dash.dependencies import Input, Output 
import plotly.express as px
import pandas as pd
import numpy as np
import bd_conexion as bd

consulta = """
SELECT course
    , CASE WHEN daytimeevening_attendance = 1 THEN 'Daytime'ELSE 'Evening' END AS attendance
    , previous_qualification_grade
    , CASE WHEN displaced = 1 THEN 'Yes' ELSE 'No' END AS displaced
    , CASE WHEN tuition_fees_up_to_date = 1 THEN 'Yes' ELSE 'No' END AS tuition_fees_up_to_date
    , CASE WHEN scholarship_holder = 1 THEN 'Yes' ELSE 'No' END AS scholarship_holder
    , curricular_units_1st_sem_evaluations 
    , CASE WHEN curricular_units_1st_sem_grade < 10 THEN 'G0 Failure'
        WHEN curricular_units_1st_sem_grade < 12 THEN 'G1 Low Failure'
        WHEN curricular_units_1st_sem_grade < 14 THEN 'G2 Satisfactory'
        WHEN curricular_units_1st_sem_grade < 20 THEN 'G3 Superior'
    END AS curricular_units_1st_sem_grade
    , unemployment_rate
    , inflation_rate
    , gdp
    , target
FROM ESTUDIANTE
;"""

bd.cursor.execute(consulta)
result = bd.cursor.fetchall()
df_disc = pd.DataFrame(result, columns=['course', 'attendance', 'previous_qualification_grade', 'displaced', 
    'tuition_fees_up_to_date', 'scholarship_holder', 'curricular_units_1st_sem_evaluations', 
    'curricular_units_1st_sem_grade', 'unemployment_rate', 'inflation_rate', 'gdp','target'])

course_list = df_disc['course'].unique().tolist()
course_dict = {
    33: "Biofuel Production Technologies",  # Ciencias exactas
    171: "Animation and Multimedia Design", # Diseño
    8014: "Social Service (evening attendance)", # Ciencias sociales
    9003: "Agronomy", # Ciencias agrarias
    9070: "Communication Design", # Diseño
    9085: "Veterinary Nursing", # Ciencias de la salud
    9119: "Informatics Engineering", # Ciencias exactas
    9130: "Equinculture", # Ciencias agrarias
    9147: "Management", # Ciencias exactas
    9238: "Social Service", # Ciencias Sociales
    9254: "Tourism", # Ciencias Sociales
    9500: "Nursing", # Ciencias de la salud
    9556: "Oral Hygiene", # Ciencias de la salud
    9670: "Advertising and Marketing Management", # Diseño
    9773: "Journalism and Communication", # Ciencias sociales
    9853: "Basic Education", # Ciencias sociales
    9991: "Management (evening attendance)" # Ciencias exactas

    # Ciencias exactas, Diseño, Ciencias sociales, Ciencias agrarias, Ciencias de la salud
}
def generate_heatmap (course, attendance, hm_click):
    x_axis = df_disc['target'].unique().tolist()
    y_axis = df_disc['curricular_units_1st_sem_grade'].sort_values().unique().tolist()
    filtered_df = df_disc[
        (df_disc["course"].isin(course)) & (df_disc["attendance"].isin(attendance))
    ]
    
    target_value = ""
    grade_1st = ""
    shapes=[]
    if hm_click is not None:
        target_value = hm_click["points"][0]["x"]
        grade_1st = hm_click["points"][0]["y"]

        # Add shapes
        x0 = x_axis.index(target_value) / 3
        x1 = x0 + 1 / 3
        y0 = y_axis.index(grade_1st) / 4
        y1 = y0 + 1 / 4

        shapes = [
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=x0,
                x1=x1,
                y0=y0,
                y1=y1,
                line=dict(color="#ff6347"),
            )
        ]

    # Get z value : sum(number of records) based on x, y,
    z = np.zeros((4, 3))
    annotations = []

    for ind_y, grade in enumerate(y_axis):
        filtered_grade = filtered_df[filtered_df["curricular_units_1st_sem_grade"] == grade]
        total_students = filtered_df["curricular_units_1st_sem_grade"].loc[filtered_df["curricular_units_1st_sem_grade"] == grade].count()
        for ind_x, x_val in enumerate(x_axis):
            count_target = round(filtered_grade[filtered_grade["target"] == x_val]["target"].count()/total_students * 100,2)
            value = str(count_target)
            # print(value)
            z[ind_y][ind_x] = value

            annotation_dict = dict(
                showarrow=False,
                text="<b>" + value + "<b>",
                xref="x",
                yref="y",
                x=x_val,
                y=grade,
                font=dict(family="sans-serif"),
            )
            # Highlight annotation text by self-click
            if x_val == target_value and grade == grade_1st:
                annotation_dict.update(size=20, font=dict(color="#ff6347"))

            annotations.append(annotation_dict)

    # Heatmap
    hovertemplate = "<b> %{y}  %{x} <br><br> %{z} % Students per Row"

    data = [
        dict(
            x=x_axis,
            y=y_axis,
            z=z,
            type="heatmap",
            name="",
            hovertemplate=hovertemplate,
            showscale=False,
            colorscale=[[0, "#caf3ff"], [1, "#2c82ff"]],
        )
    ]

    layout = dict(
        margin=dict(l=70, b=50, t=50, r=50),
        modebar={"orientation": "v"},
        font=dict(family="Open Sans"),
        annotations=annotations,
        shapes=shapes,
        xaxis=dict(
            side="top",
            ticks="",
            ticklen=2,
            tickfont=dict(family="sans-serif"),
            tickcolor="#ffffff",
        ),
        yaxis=dict(
            side="left", ticks="", tickfont=dict(family="sans-serif"), ticksuffix=" "
        ),
        hovermode="closest",
        showlegend=False,
    )
    return {"data": data, "layout": layout}

def generate_heatmap_tuition_fees (course, attendance, hm_click, hm_tuition_click):
    x_axis = df_disc['target'].unique().tolist()
    y_axis = df_disc['tuition_fees_up_to_date'].sort_values().unique().tolist()
    filtered_df = df_disc[
        (df_disc["course"].isin(course)) & (df_disc["attendance"].isin(attendance))
    ]
    if hm_click is not None:
        filtered_df = filtered_df.loc[
            (filtered_df["target"] == hm_click["points"][0]["x"])  & (filtered_df["curricular_units_1st_sem_grade"] == hm_click["points"][0]["y"])
        ]
    target_value = ""
    scolarship = ""
    shapes=[]

    shapes=[]
    if hm_tuition_click is not None:
        target_value = hm_tuition_click["points"][0]["x"]
        scolarship = hm_tuition_click["points"][0]["y"]

        # Add shapes
        x0 = x_axis.index(target_value) / 3
        x1 = x0 + 1 / 3
        y0 = y_axis.index(scolarship) / 2
        y1 = y0 + 1 / 2

        shapes = [
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=x0,
                x1=x1,
                y0=y0,
                y1=y1,
                line=dict(color="#ff6347"),
            )
        ]
    
    # Get z value : sum(number of records) based on x, y,
    z = np.zeros((2, 3))
    annotations = []

    for ind_y, tuition_fees in enumerate(y_axis):
        filtered_tuition = filtered_df[filtered_df["tuition_fees_up_to_date"] == tuition_fees]
        for ind_x, x_val in enumerate(x_axis):
            total_students = filtered_df["target"].loc[filtered_df["target"] == x_val].count()
            if total_students > 0:
                count_target = round(filtered_tuition[filtered_tuition["target"] == x_val]["target"].count()/total_students * 100,2)
            else:
                count_target = 0

            value = str(count_target)
            # print(value)
            z[ind_y][ind_x] = value
            annotation_dict = dict(
                showarrow=False,
                text="<b>" + value + "<b>",
                xref="x",
                yref="y",
                x=x_val,
                y=tuition_fees,
                font=dict(family="sans-serif"),
            )

            annotations.append(annotation_dict)

    # Heatmap
    hovertemplate = "<b> %{y}  %{x} <br><br> %{z} % Students per Column"

    data = [
        dict(
            x=x_axis,
            y=y_axis,
            z=z,
            type="heatmap",
            name="",
            hovertemplate=hovertemplate,
            showscale=False,
            colorscale=[[0, "#caf3ff"], [1, "#2c82ff"]],
        )
    ]

    layout = dict(
        margin=dict(l=70, b=50, t=50, r=50),
        modebar={"orientation": "v"},
        font=dict(family="Open Sans"),
        annotations=annotations,
        shapes = shapes,
        xaxis=dict(
            side="top",
            ticks="",
            ticklen=2,
            tickfont=dict(family="sans-serif"),
            tickcolor="#ffffff",
        ),
        yaxis=dict(
            side="left", ticks="", tickfont=dict(family="sans-serif"), ticksuffix=" "
        ),
        hovermode="closest",
        showlegend=False,
    )
    return {"data": data, "layout": layout}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server

#Definición de barra lateral
def generate_control_card():
    """

    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.B("Select Courses"),
            dcc.Dropdown(
                options=[{"label": valor, "value": clave} for clave, valor in course_dict.items()],
                value=course_list[:], 
                id='dropdown-course',
                multi=True
            ),
            html.Br(),
            html.P("Select daytime attendance"),
            dcc.Checklist(
                options=df_disc.attendance.unique(),
                inline = True,
                value=["Evening", "Daytime"],
                id='checklist-daytime'
            ),
            html.Br(),
        ],
    )

# def description_prediction():
#     """
#     :return: A description about levels to be set in prediction dash
#     """
#     return html.Div(
#         id="description-prediction",
#         children=[
#             html.Div(
#                 id="intro-prediction",
#                 children="Select filters to see information",
#             ),
#         ],
#     )

def description_card():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Students Prediction"),
            html.H3("Welcome to the Students Prediction Dashboard"),
            html.Div(
                id="intro",
                children="The Dashboard was created as part of a project with the objective of contributing to the reduction of academic dropout and failure in higher education. It leverages Bayesian network techniques to identify students at risk at an early stage of their academic journey.",
            )
            # html.Ol([
            #     html.Li("To generate a prediction and assess students' risk, please follow these steps:"),
            #     html.Li("Use the provided dropdown menus and checklist filters to select the relevant parameters and attributes related to the student's profile and academic situation."),
            #     html.Li("After selecting the desired filters, view the selected values in the right panel and observe the generated prediction.."),
            #     html.Li("Utilize the generated predictions to implement appropriate strategies and support measures to help students succeed in their academic endeavors.")
            # ]),
        ],
    )
def graphs():
    return html.Div(
                    id="other-graphs",
                    children = [
                        html.B("Target vs Grade 1st Sem Heatmap"),
                        html.Hr(),
                        dcc.Graph(id='target_heatmap'),
                        html.Br(),
                        html.B("Tuition Fees Up to Date Heatmap"),
                        html.Hr(),
                        dcc.Graph(id='target_heatmap_tuition'),
                        html.Br(),
                        html.B("Scholarship Holders"),
                        html.Hr(),
                        dcc.Graph(id='bar-graph')
                        # html.Div(id='prueba')
                    ]
                )
app.layout =  html.Div(
    id="app-container",
    children= [
        # Banner
        html.Div(
            id="banner",
            className="banner",
            children=[html.Img(src=app.get_asset_url("logo_uniandes.png"))],
        ),
        # Left column
        html.Div( 
            id="left-column",
            className="three columns",
            children=[description_card(),
            dcc.Tabs(id='tabs-example-1', value='tab-1', children=[
                dcc.Tab(label='Visualizations', value='tab-1'),
                dcc.Tab(label='Prediction', value='tab-2'),
            ]),
            html.Div(id='tabs-example-content-1')] #  generate_prediction_card(), description_prediction(), 
            + [
                html.Div(
                    ["initial child"], id="output-clientside", style={"display": "none"}
                )
            ],
        ),
        # Right column
        html.Div(
            id="right-column",
            className="eight columns",
            children= [
            html.Div(id='tabs-example-content-2')
                
            ]
        ),
])

@app.callback(
    Output('tabs-example-content-1', 'children'),
    Output('tabs-example-content-2', 'children'),
    Input('tabs-example-1', 'value')
)
def render_content(tab):
    if tab == 'tab-1':
        return generate_control_card(), graphs() #  generate_prediction_card(),     
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ]), html.Div([
            html.H3('Tab content 2')
        ])
    
@app.callback(
            Output('bar-graph', 'figure'),
            Output('target_heatmap', 'figure'),
            Output('target_heatmap_tuition', 'figure'),
            Input('dropdown-course', 'value'),
            Input('checklist-daytime', 'value'),
            Input("target_heatmap", "clickData"),
            Input("target_heatmap_tuition", "clickData") 
        )
def update_output(course_value, daytime_value, hm_click, hm_tuition_click):
    
    filtered_df = df_disc[
            (df_disc['course'].isin(course_value) & (df_disc['attendance'].isin(daytime_value)))
        ]
    filtered_hm = filtered_df
    if hm_click is not None:
        filtered_hm = filtered_df.loc[
            (filtered_df["target"] == hm_click["points"][0]["x"])  & (filtered_df["curricular_units_1st_sem_grade"] == hm_click["points"][0]["y"])
        ]
        if hm_tuition_click is not None:
            filtered_hm = filtered_df.loc[
                (filtered_df["target"] == hm_tuition_click["points"][0]["x"])  & (filtered_df["tuition_fees_up_to_date"] == hm_tuition_click["points"][0]["y"]) & \
                (filtered_df["target"] == hm_click["points"][0]["x"])  & (filtered_df["curricular_units_1st_sem_grade"] == hm_click["points"][0]["y"])
            ]
    
    # print(filtered_df)
    
    fig2 = px.histogram(filtered_hm, x="scholarship_holder", text_auto=True, category_orders=dict(scholarship_holder=["Yes","No"])) 
    fig2.update_layout(
        xaxis_title= None,
        yaxis_title='Count'
    )
    return fig2, generate_heatmap(course_value, daytime_value, hm_click), generate_heatmap_tuition_fees (course_value, daytime_value, hm_click, hm_tuition_click)#, f'Selected values {hm_click}'

""" 
@app.callback(
    # Output('bar-graph', 'figure'),
    # Output('target_heatmap', 'figure'),
    # Output('target_heatmap_tuition', 'figure'),
    # Input('dropdown-course', 'value'),
    # Input('checklist-daytime', 'value'),
    # Input("target_heatmap", "clickData"),
    # Input("target_heatmap_tuition", "clickData")
)
def update_output(course_value, daytime_value, hm_click, hm_tuition_click):
    
    filtered_df = df_disc[
            (df_disc['course'].isin(course_value) & (df_disc['attendance'].isin(daytime_value)))
        ]
    filtered_hm = filtered_df
    if hm_click is not None:
        filtered_hm = filtered_df.loc[
            (filtered_df["target"] == hm_click["points"][0]["x"])  & (filtered_df["curricular_units_1st_sem_grade"] == hm_click["points"][0]["y"])
        ]
        if hm_tuition_click is not None:
            filtered_hm = filtered_df.loc[
                (filtered_df["target"] == hm_tuition_click["points"][0]["x"])  & (filtered_df["tuition_fees_up_to_date"] == hm_tuition_click["points"][0]["y"]) & \
                (filtered_df["target"] == hm_click["points"][0]["x"])  & (filtered_df["curricular_units_1st_sem_grade"] == hm_click["points"][0]["y"])
            ]
    
    # print(filtered_df)
    
    fig2 = px.histogram(filtered_hm, x="scholarship_holder", text_auto=True, category_orders=dict(scholarship_holder=["Yes","No"])) 
    fig2.update_layout(
        xaxis_title= None,
        yaxis_title='Count'
    )
    return generate_control_card(), graphs(), fig2, generate_heatmap(course_value, daytime_value, hm_click), generate_heatmap_tuition_fees (course_value, daytime_value, hm_click, hm_tuition_click)#, f'Selected values {hm_click}'

    # return generate_control_card() #  generate_prediction_card(), 
        
     """
    

    
if __name__ == '__main__':
    app.run_server(debug=True)

