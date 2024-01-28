# Importing Toolkits
import pandas as pd
import numpy as np
import plotly.express as px

# Importing Dash Components
from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc

used_color = ["#ADA2FF", "#C0DEFF", "#FCDDB0", "#FF9F9F", "#EDD2F3", "#98EECC", "#79E0EE"]
# ----------- Loading Dataset -----------
df = pd.read_csv("HR_Final_Database.csv")
df["Hire_Date"] = pd.to_datetime((df["Hire_Date"]))
df["Birth_Date"] = pd.to_datetime((df["Birth_Date"]))
df["Termination_Date"] = pd.to_datetime((df["Termination_Date"]))

year = df["Hire_Date"].dt.year.unique().tolist()
year.insert(0, "All Years")

departments = df["Department"].unique().tolist()
departments.insert(0, "All Departments")

# *******************************************************************************************************
# ** Notice: The Data Exploration & Preprocessing of This DataSet has Already Done In Jupyter Notebook **
# *******************************************************************************************************

# -------------- Start The Dash App ------------------ #
app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])

# To render on web app
server = app.server

# Pages Navigator
pages_dict = {
    "Home": "/",
    "Departments": "/Departments",
    "Locations": "/Locations",
    "Performance": "/Performance",
}

# Sidebar Style
sidebar_style = {
    "position": "fixed",
    "width": "16rem",
    "height": "100vh",
    "top": "0",
    "bottom": "0",
    "left": "0",
    "padding": "15px",
    "background-color": "#111",
    "border-right": "2px solid #5FBDFF"
}

# Page Content Style
content_style = {
    "margin-left": "16rem",
    "margin-right": "0rem",
    "padding": "15px",
    "height": "100%",
}

# DropDown Filter Style
filter_style = {
    "border-width": "0px",
    "font-family": "arial",
    "margin-bottom": "25px",
    "background-color": "#222",
}


def get_alert(year_value, department_value):
    return dbc.Alert(
        [
            html.H2("Warning", style={"font": "bold 30px arial"}),
            html.P(
                f"The Department {department_value} Did Not Exist In {year_value} !!😔😔",
                style={"font": "bold 22px arial"}
            ),
            html.Hr(),
            html.P(
                "Choose Another Department",
                style={"font": "bold 20px arial"},
                className="mb-0",
            ),
        ], color="danger",
        style={"box-shadow": "none", "text-shdow": "none"}
    )


# -------------- Start The App Layout ------------------ #
# Creating The SideBar
sidebar = html.Div(
    [
        dcc.Dropdown(
            id="theme-toggle",
            options=[
                {
                    "label": html.Span(
                        [
                            html.Img(src="/assets/light-mode.png", height=25),
                            html.Span("Light", style={'font-size': 14, 'padding-left': 10, "color": "#999"}),
                        ], style={'align-items': 'center', 'justify-content': 'center'}
                    ),
                    "value": "Light",
                },
                {
                    "label": html.Span(
                        [
                            html.Img(src="/assets/dark-mode.png", height=25),
                            html.Span("Dark", style={'font-size': 14, 'padding-left': 10, "color": "#999"}),
                        ], style={'align-items': 'center', 'justify-content': 'center'}
                    ),
                    "value": "Dark",
                }
            ],
            value="Light",
            multi=False,
            clearable=False,
            searchable=False,
            style=filter_style

        ),

        html.H1("HR Analysis",
                style={"font": "bold 35px arial",
                       "margin-top": "30px",
                       "margin-bottom": "20px",
                       "color": "#fefefe",
                       "text-align": "center"}),
        html.Hr(style={"border-color": "#444"}),

        dbc.Nav(
            [
                dbc.NavLink(f"{k}", href=f"{v}",
                            className="btn", active="exact",
                            style={"margin-bottom": "20px", "font-weight": "bold"})
                for k, v in pages_dict.items()
            ],
            vertical=True,
            pills=True,

        ),
        html.Br(),

        dcc.Dropdown(
            id="year-filter",
            options=[
                {"label": html.Span([i], style={'color': '#6499E9', 'font': "bold 16px arial", "margin": "12px 5px"}),
                 "value": i} for i in year
            ],
            value="All Years",

            multi=False,
            searchable=False,
            clearable=False,
            optionHeight=40,
            style=filter_style
        ),

        # html.Br(),
        dcc.RadioItems(
            id="filter-type",

            options=[
                {"label": html.Span(["Until Year"],
                                    style={'color': '#6499E9', 'font': "bold 16px arial", "margin": "12px 5px"}),
                 "value": "Until"},

                {"label": html.Span(["In Year"],
                                    style={'color': '#6499E9', 'font': "bold 16px arial", "margin": "12px 5px"}),
                 "value": "In"},

            ],
            value='Until',
            inline=True
        ),

        # html.Hr(),
        dcc.Dropdown(
            id="department-filter",
            options=[
                {"label": html.Span([i], style={'color': '#6499E9', 'font': "bold 16px arial", "margin": "12px 5px"}),
                 "value": i, } for i in departments

            ],
            value="All Departments",
            multi=False,
            optionHeight=40,
            clearable=False,
            searchable=True,
            style={"display": "none"}
        ),

    ],
    style=sidebar_style
)

# page content
content = html.Div(id="page-content", children=[], style=content_style)

# ►►► App Layout
app.layout = html.Div([
    dcc.Location(id="page-url"),
    sidebar,
    # header,
    content,
    html.Div(id="output-text")
], className="container-fluid", style={"background-color": "#fafafa"})


def filter_the_data(the_year, filter_type):
    df_filtered = ""
    if the_year == "All Years":
        df_filtered = df.copy()
    else:
        if filter_type == "In":
            year_filt = (df["Hire_Date"].dt.year == the_year)
        else:
            year_filt = (df["Hire_Date"].dt.year <= the_year)
        df_filtered = df[year_filt].copy()

    return df_filtered


def custome_chart_layout(fig, title_size=28, showlegend=False):
    fig.update_layout(
        showlegend=showlegend,
        title={
            "font": {
                "size": title_size,
                "family": "tahoma"
            }
        },
        hoverlabel={
            "bgcolor": "#111",
            "font_size": 16,
            "font_family": "arial"
        }
    )


# ---------------------- Visualizations Graphs Functions ----------------------
# ====================== Home Page ================================
def create_home_cards(the_year, filter_type):
    df_filtered = filter_the_data(the_year, filter_type)

    emp_numbers = df_filtered["ID"].nunique()

    available_position = df_filtered["Position"].nunique()

    avg_salary = df_filtered["Salary"].mean()

    return emp_numbers, available_position, f"{avg_salary:,.0f}"


def create_gender_chart(the_year, filter_type, chart_theme):
    df_filtered = filter_the_data(the_year, filter_type)

    gender = df_filtered["Gender"].value_counts()
    fig = px.pie(names=gender.index,
                 values=gender,
                 color_discrete_sequence=["#42C2FF", "#A1EEBD"],
                 hole=0.4,
                 template=chart_theme,
                 title="Gender Frequency",
                 )

    custome_chart_layout(fig, showlegend=True)

    fig.update_traces(
        textfont={
            "size": 16,
            "family": "tahoma",
            "color": "#111"
        },
        hovertemplate="Gender: %{label}<br>Gender Frequency: %{value}<br>Gender Percentage(%): %{percent}",
        marker=dict(line=dict(color='#333', width=1))
    )
    return fig


def create_emp_department_chart(the_year, filter_type, chart_theme):
    df_filtered = filter_the_data(the_year, filter_type)

    emp_dep = df_filtered["Department"].value_counts()[::-1]
    fig = px.bar(data_frame=emp_dep,
                 orientation="h",
                 x=emp_dep,
                 y=emp_dep.index,
                 color_discrete_sequence=["#42C2FF", "#A1EEBD"],
                 template=chart_theme,
                 title="Employees Through Departments",
                 labels={"x": "Employees Count"},
                 text_auto=True
                 )

    custome_chart_layout(fig, showlegend=True)

    fig.update_traces(
        textfont={
            "size": 15,
            "family": "tahoma",
            "color": "#111"
        },
        hovertemplate="Department: %{y}<br>Count: %{x}",
        marker=dict(line=dict(color='#333', width=1))
    )
    return fig


def create_emp_education_chart(the_year, filter_type, chart_theme):
    df_filtered = filter_the_data(the_year, filter_type)

    emp_education = df_filtered["Education"].value_counts()

    fig = px.bar(x=emp_education.index,
                 y=emp_education,
                 color=emp_education.index,
                 # color_discrete_sequence=["#42C2FF"],
                 color_discrete_sequence=used_color,
                 template=chart_theme,
                 labels={"x": "Education Level", "y": "Employees Count"},
                 title="Number of Employees By Educational Level",
                 text_auto=True,

                 )

    custome_chart_layout(fig, showlegend=False)

    fig.update_traces(
        textfont={
            "size": 17,
            "family": "tahoma",
            "color": "#111"
        },
        hovertemplate="Education: %{x}<br>Employees Count: %{y}",
        marker=dict(line=dict(color='#111', width=1))
    )
    return fig


# ====================== Departments Page ================================
def create_gender_department_chart(the_year, filter_type, chart_theme):
    df_filtered = filter_the_data(the_year, filter_type)

    gender_dep = df_filtered.pivot_table(index="Department", columns="Gender", values="Employee",
                                         aggfunc="count").fillna(0)
    gender_dep = gender_dep.sort_values("Male", ascending=False)
    gender_dep = gender_dep.iloc[:, [1, 0]][::-1]

    fig = px.bar(gender_dep,
                 orientation="h",
                 title="Popularity of Gender Via Department",
                 color_discrete_sequence=["#5FBDFF", "#4FD3C4"],
                 template=chart_theme,
                 labels={"value": "Gender Frequency"},
                 text_auto=True
                 )
    custome_chart_layout(fig, showlegend=True, title_size=24)

    fig.update_traces(
        textposition="auto",
        textfont={
            "size": 14,
            "family": "tahoma",
            "color": "#000"
        },
        hovertemplate="Department: %{y}<br>Gender Frequency: %{x}",
        marker=dict(line=dict(color='#222', width=1))
    )
    return fig


def create_salary_department_chart(the_year, filter_type, chart_theme):
    df_filtered = filter_the_data(the_year, filter_type)
    salary_dep = df_filtered.groupby("Department")["Salary"].mean().sort_values(ascending=False)

    fig = px.bar(data_frame=salary_dep,
                 orientation="h",
                 y=salary_dep.index,
                 x=salary_dep,
                 color=salary_dep.index,
                 color_discrete_sequence=["#5FBDFF"],
                 template=chart_theme,
                 text_auto="0.4s",
                 labels={"x": "Average Salary"},
                 title="Average Salary for Each Department"
                 )

    custome_chart_layout(fig, title_size=24)

    fig.update_traces(
        textfont={
            "size": 14,
            "family": "tahoma",
            "color": "#000"
        },
        hovertemplate="Department: %{y}<br>Average Salary: %{x:0.3s}",
        marker=dict(line=dict(color='#222', width=1))

    )
    return fig


def create_dep_education_level(the_year, filter_type, chart_theme):
    df_filtered = filter_the_data(the_year, filter_type)

    edu_via_dep = df.pivot_table(index="Department",
                                 columns="Education",
                                 values="Employee", aggfunc="count").fillna(0)
    fig = px.scatter(edu_via_dep,
                     title="Employees Education Through Departments",
                     template=chart_theme,
                     )

    custome_chart_layout(fig, showlegend=True, title_size=28)

    fig.update_traces(marker=dict(size=18,
                                  line=dict(width=1,
                                            color='DarkSlateGrey')),
                      selector=dict(mode='markers'),
                      hovertemplate="Department: %{x}<br>Frequency: %{y}",
                      )

    return fig


def employees_table(the_year, filter_type, chart_theme):
    df_filtered = filter_the_data(the_year, filter_type)
    df_filtered = df_filtered[["Employee", "Gender", "Education", "City", "Performance_Review", "Salary"]].copy()

    df_filtered["Salary"] = df_filtered["Salary"].apply(lambda x: f"{x:,.0f}")
    df_filtered["Performance_Review"] = df_filtered["Performance_Review"].apply(lambda x: f"{x}")
    df_filtered.rename(columns={"Performance_Review":"Performance"}, inplace=True)

    if chart_theme == "plotly_dark":
        header_style = {
            'backgroundColor': '#1e1e1e',
            'color': '#fff',
            "font": "bold 18px arial"
        }

        data_style = {
            'backgroundColor': '#323232',
            'color': '#fff',
            "font": "400 16px arial"
        }

    else:
        header_style = {
            'backgroundColor': '#fafafa',
            'color': '#444',
            "font": "bold 18px arial"
        }

        data_style = {
            'backgroundColor': '#fff',
            'color': '#222',
            "font": "400 16px arial"
        }

    table = dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in df_filtered.columns
        ],
        style_header=header_style,
        style_data=data_style,
        data=df_filtered.to_dict('records'),
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=False,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
    )
    return table


# ====================== Locations =====================
def filter_the_data_by_dep(the_dep):
    df_filtered = ""
    if the_dep == "All Departments":
        df_filtered = df.copy()
    else:
        dep_filt = (df["Department"] == the_dep)
        df_filtered = df[dep_filt].copy()

    return df_filtered


def create_location_map_chart(the_dep, chart_theme):
    df_filtered = filter_the_data_by_dep(the_dep)
    loc = pd.read_csv("https://raw.githubusercontent.com/jasperdebie/VisInfo/master/us-state-capitals.csv")
    df_filtered = df_filtered.merge(loc, left_on="City", right_on="name")
    locs_emp = df_filtered.groupby(["City", "latitude", "longitude"],
                                   as_index=False)["Employee"].count()

    fig = px.scatter_mapbox(locs_emp,
                            lat="latitude",
                            lon="longitude",
                            hover_name="City",
                            hover_data=["Employee"],
                            color="Employee",
                            size="Employee",
                            color_continuous_scale=px.colors.cyclical.IceFire,
                            zoom=3,
                            height=650,
                            title="\t\tEmployees Through Locations",
                            template=chart_theme
                            )

    fig.update_layout(
        mapbox_style="open-street-map",
        title={
            "font": {
                "size": 32,
                "family": "tahoma"
            }
        },
        hoverlabel={
            "bgcolor": "#222",
            "font_size": 15,
            "font_family": "tahoma"
        }
    )

    return fig


# ===================== Performance =====================
def filter_data_dep_date(the_year, filter_type, the_dep):
    df_filtered = ""
    if the_year == "All Years":
        df_filtered = df.copy()
    else:
        if filter_type == "In":
            year_filt = (df["Hire_Date"].dt.year == the_year)
        else:
            year_filt = (df["Hire_Date"].dt.year <= the_year)
        df_filtered = df[year_filt].copy()

    if the_dep == "All Departments":
        df_filtered = df_filtered.copy()
    else:
        dep_filt = (df_filtered["Department"] == the_dep)
        df_filtered = df_filtered[dep_filt].copy()

    return df_filtered


def create_performance_cards(the_year, filter_type, the_dep):
    df_filtered = filter_data_dep_date(the_year, filter_type, the_dep)

    # Performance Review Completion Rate
    completed_review = df_filtered.loc[df["Performance_Review"] == 10, "Performance_Review"].count()
    performance_rate = completed_review / len(df_filtered) * 100

    # Turnover Rate
    turnover_rate = (len(df_filtered["Termination_Date"]) - df_filtered["Termination_Date"].isna().sum()) / len(
        df_filtered) * 100

    termination = (~df_filtered["Termination_Date"].isna()).sum()

    promotions = (~df_filtered["Last_Promotion_Date"].isna()).sum()

    return f"{performance_rate:0.2f}%", f"{turnover_rate:0.2f}%", termination, promotions


def create_performance_department_chart(the_year, filter_type, the_dep, chart_theme):
    df_filtered = filter_data_dep_date(the_year, filter_type, the_dep)

    performance_dep = df_filtered.groupby("Department")["Performance_Review"].mean().sort_values(ascending=False)

    fig = px.bar(data_frame=performance_dep,
                 x=performance_dep.index,
                 y=performance_dep,
                 color=performance_dep.index,
                 color_discrete_sequence=used_color,
                 template=chart_theme,
                 text_auto="0.2s",
                 labels={"y": "Average Salary"},
                 title="Average Performance for Each Department"
                 )

    custome_chart_layout(fig)

    fig.update_traces(
        textfont={
            "size": 14,
            "family": "tahoma",
            "color": "#000"
        },
        hovertemplate="Department: %{x}<br>Average Salary: %{y:0.3s}",
        marker=dict(line=dict(color='#222', width=1))

    )
    return fig


# CallBack Functions
@app.callback(
    Output(component_id="year-filter", component_property="style"),
    Output(component_id="filter-type", component_property="style"),

    Output(component_id="department-filter", component_property="style"),
    Output(component_id="department-filter", component_property="options"),

    Output(component_id="page-content", component_property="children"),
    Output(component_id="page-content", component_property="style"),

    Input(component_id="page-url", component_property="pathname"),
    Input(component_id="year-filter", component_property="value"),
    Input(component_id="filter-type", component_property="value"),
    Input(component_id="department-filter", component_property="value"),
    # Input(component_id="theme-toggle", component_property="n_clicks"),
    Input(component_id="theme-toggle", component_property="value"),

)
def get_content_layout(pathname, year_value, filter_type, dep_value, target_theme):
    app_theme = ""
    chart_theme = ""
    chart_border = ""
    card_bg = ""
    card_bg_border = ""
    card_font_color = ""

    if year_value != "All Years":
        if filter_type == "Until":
            year_filt = (df["Hire_Date"].dt.year <= year_value)
        else:
            year_filt = (df["Hire_Date"].dt.year == year_value)

        departments = df.loc[year_filt, "Department"].unique().tolist()
        departments.insert(0, "All Years")
    else:
        departments = df.loc[:, "Department"].unique().tolist()
        departments.insert(0, "All Departments")

    if target_theme == "Dark":
        app_theme = "#111"
        chart_theme = "plotly_dark"
        chart_border = "#222"

        card_bg = "#000"
        card_bg_border = "#00D7FF"
        card_font_color = "#fafafa"

    else:
        app_theme = "#fafafa"
        chart_theme = "plotly_white"
        chart_border = "#fafafa"

        card_bg = "#fff"
        card_bg_border = "#fafafa"
        card_font_color = "#555"

    card_style = {
        "background-color": card_bg,
        "text-align": "center",
        "padding-top": "25px",
        "padding-bottom": "25px",
        "border": f"2px solid {card_bg_border}",
        "border-radius": "5px",
        "margin-bottom": "5px",
        "box-shadow": "0 1px 2px 0 rgba(0, 0, 0, 0.05)"
    }
    graph_style = {
        "margin-bottom": "10px",
        "height": "560px",
        "border": f"3px solid {chart_border}",
        "border-radius": "4px"
    }

    the_app_theme = {
        "margin-left": "15rem",
        "margin-right": "0rem",
        "padding": "20px",
        "height": "100%",
        "background-color": app_theme
    }
    if pathname == "/":
        return [
            filter_style,
            {"display": "block"},
            {"display": "none"},
            [{"label": html.Span([i], style={'color': '#6499E9', 'font': "bold 16px arial", "margin": "12px 5px"}),
              "value": i, } for i in departments],

            html.Div([
                html.Br(),
                dbc.Row([
                    html.H1("HR Analysis", style={"font": "bold 40px arial", "text-align": "center"})
                ]),

                html.Br(),

                dbc.Row([
                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody([
                                html.H3(create_home_cards(year_value, filter_type)[0],
                                        style={"color": card_font_color, "font": "bold 32px tahoma"},
                                        id='emp-count-crd'),
                                html.H3("Employees", style={"font": "bold 20px tahoma"}),
                            ]), style=card_style,
                        ),

                    ]),
                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody([
                                html.H3(create_home_cards(year_value, filter_type)[1],
                                        style={"color": card_font_color, "font": "bold 32px tahoma"},
                                        id='available-pos-crd'),
                                html.H3("Available Positions", style={"font": "bold 20px tahoma"}),
                            ]), style=card_style
                        ),

                    ]),
                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody([
                                html.H3(create_home_cards(year_value, filter_type)[2],
                                        style={"color": card_font_color, "font": "bold 32px tahoma"},
                                        id='salary-job-crd'),
                                html.H3("Average Salary", style={"font": "bold 20px tahoma"}),
                            ]), style=card_style
                        ),
                    ]),
                ]),
                html.Br(),

                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(id="gender-chart",
                                          figure=create_gender_chart(year_value, filter_type, chart_theme),
                                          style=graph_style)
                            ]
                        ),
                        dbc.Col(
                            [
                                dcc.Graph(id="emp-department-chart",
                                          figure=create_emp_department_chart(year_value, filter_type, chart_theme),
                                          style=graph_style)
                            ]
                        )
                    ]
                ),

                html.Br(),
                dbc.Row([
                    dbc.Col(
                        [
                            dcc.Graph(id="emp_education_chart",
                                      figure=create_emp_education_chart(year_value, filter_type, chart_theme),
                                      style=graph_style)
                        ]
                    )
                ])

            ]),

            # App Theme Dark Or Light
            the_app_theme
        ]

    if pathname == "/Departments":
        return [
            filter_style,
            {"display": "block"},
            {"display": "none"},
            [{"label": html.Span([i], style={'color': '#6499E9', 'font': "bold 16px arial", "margin": "12px 5px"}),
              "value": i, } for i in departments],

            html.Div([
                html.Br(),
                dbc.Row([
                    html.H1("Departments", style={"font": "bold 40px arial", "text-align": "center"})
                ]),

                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(id="salary-department-chart",
                                          figure=create_salary_department_chart(year_value, filter_type, chart_theme),
                                          style=graph_style)
                            ]
                        ),
                        dbc.Col(
                            [
                                dcc.Graph(id="gender-department-chart",
                                          figure=create_gender_department_chart(year_value, filter_type, chart_theme),
                                          style=graph_style)
                            ]
                        ),
                    ]
                ),
                html.Br(),
                dbc.Row([
                    dbc.Col(
                        [
                            dcc.Graph(id="gender-department-chart",
                                      figure=create_dep_education_level(year_value, filter_type, chart_theme),
                                      style=graph_style)
                        ]
                    ),
                ])

            ]),

            # App Theme Dark or Light
            the_app_theme
        ]

    if pathname == "/Locations":
        return [
            {"display": "none"},
            {"display": "none"},
            filter_style,
            [{"label": html.Span([i], style={'color': '#6499E9', 'font': "bold 16px arial", "margin": "12px 5px"}),
              "value": i, } for i in departments],

            html.Div([
                html.Br(),
                dbc.Row([
                    html.H1("Locations", style={"font": "bold 40px arial", "text-align": "center"})
                ]),

                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(id="emp-locations-chart",
                                          figure=create_location_map_chart(dep_value, chart_theme),
                                          style=graph_style)
                            ]
                        )
                    ]
                ),
            ]),
            # App Theme Dark Or Light
            {
                "margin-left": "15rem",
                "margin-right": "0rem",
                "padding": "20px",
                "height": "100vh",
                "background-color": app_theme
            }
        ]

    if pathname == "/Performance":
        if dep_value not in departments:
            page_content = get_alert(year_value, dep_value)
        else:
            page_content = html.Div([
                html.Br(),
                dbc.Row([
                    html.H1("Performance", style={"font": "bold 40px arial", "text-align": "center"})
                ]),
                html.Br(),

                dbc.Row([
                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody([
                                html.H3(create_performance_cards(year_value, filter_type, dep_value)[0],
                                        style={"color": card_font_color, "font": "bold 32px tahoma"},
                                        id='performance-review-crd'),
                                html.H3("Performance Rate", style={"font": "bold 18px tahoma"}),
                            ]), style=card_style,
                        ),

                    ]),
                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody([
                                html.H3(create_performance_cards(year_value, filter_type, dep_value)[1],
                                        style={"color": card_font_color, "font": "bold 32px tahoma"},
                                        id='turnover-crd'),
                                html.H3("Turnover Rate", style={"font": "bold 18px tahoma"}),
                            ]), style=card_style
                        ),

                    ]),
                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody([
                                html.H3(create_performance_cards(year_value, filter_type, dep_value)[2],
                                        style={"color": card_font_color, "font": "bold 32px tahoma"},
                                        id='termination'),
                                html.H3("Terminated Employees", style={"font": "bold 18px tahoma"}),
                            ]), style=card_style
                        ),
                    ]),
                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody([
                                html.H3(create_performance_cards(year_value, filter_type, dep_value)[3],
                                        style={"color": card_font_color, "font": "bold 32px tahoma"},
                                        id='promotions'),
                                html.H3("Promoted Employees", style={"font": "bold 18px tahoma"}),
                            ]), style=card_style
                        ),
                    ]),
                ]),
                html.Br(),

                dbc.Row([
                    dbc.Col(
                        [
                            dcc.Graph(id="gender-department-chart",
                                      figure=create_performance_department_chart(year_value, filter_type, dep_value,
                                                                                 chart_theme),
                                      style=graph_style)
                        ]
                    ),
                ]),
                html.Br(),

                dbc.Row([
                    dbc.Col(
                        [
                            employees_table(year_value, filter_type, chart_theme)

                        ]
                    ),
                ])

            ]),

        return [
            filter_style,
            {"display": "block", "margin-bottom": "25px"},
            filter_style,

            [{"label": html.Span([i], style={'color': '#6499E9', 'font': "bold 16px arial", "margin": "12px 5px"}),
              "value": i, } for i in departments],

            page_content,

            the_app_theme
        ]


# Run The App
if __name__ == "__main__":
    app.run_server(debug=True)
