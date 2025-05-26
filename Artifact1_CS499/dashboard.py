from dash import dash, Dash, html, dcc, dash_table, Input, Output, State
import dash_bootstrap_components as dbc
from animalReserveShelter import animalReserveShelter

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

db = animalReserveShelter()

# Initial read to show all animals on startup
animals = db.read()
columns = [{"name": k, "id": k} for k in animals[0].keys()] if animals else []


# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Animal Reserve Shelter Dashboard"),

    dbc.Row([
        dbc.Col([
            dcc.RadioItems(
                id='action-select',
                options=[
                    {'label': 'Intake a new dog', 'value': 'intake_dog'},
                    {'label': 'Intake a new monkey', 'value': 'intake_monkey'},
                    {'label': 'Reserve an animal', 'value': 'reserve_animal'},
                    {'label': 'List all dogs', 'value': 'list_dogs'},
                    {'label': 'List all monkeys', 'value': 'list_monkeys'},
                    {'label': 'List all unreserved animals', 'value': 'list_unreserved'},
                ],
                style={"padding": "10px"},
                value='list_all',
                inline=True
            )
        ])
    ]),
    html.Hr(),

    html.Div(id='action-form'),

     # Reserve animal input, hidden initially
    dcc.Input(id='input-reserve-name', placeholder='Animal Name to Reserve', type='text', style={'display': 'none'}),

    # Always present buttons (hidden initially)
    dbc.Button('Add Dog', id='btn-add-dog', color='primary', className='mt-2', style={'display': 'none'}),
    dbc.Button('Add Monkey', id='btn-add-monkey', color='primary', className='mt-2', style={'display': 'none'}),
    dbc.Button('Reserve Animal', id='btn-reserve', color='warning', className='mt-2', style={'display': 'none'}),

    dash_table.DataTable(
        id='animal-table',
        data=animals,
        columns=columns,
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'left',
            'padding': '5px',
            'border': '1px solid #ddd',
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        style_header={
            'backgroundColor': 'lightgrey',
            'fontWeight': 'bold'
        },
    ),

    html.Div(id='output-message', className='mt-3')
])

@app.callback(
    Output('action-form', 'children'),
    Output('btn-add-dog', 'style'),
    Output('btn-add-monkey', 'style'),
    Output('btn-reserve', 'style'),
    Input('action-select', 'value')
)
def display_action_form(action):
    # Hide all buttons by default
    dog_btn_style = {'display': 'none'}
    monkey_btn_style = {'display': 'none'}
    reserve_btn_style = {'display': 'none'}

    if action == 'intake_dog':
        dog_btn_style = {'display': 'inline-block'}
        return html.Div([
            dcc.Input(id='input-name', placeholder='Name', type='text'),
            dcc.Input(id='input-gender', placeholder='Gender', type='text'),
            dcc.Input(id='input-age', placeholder='Age', type='number'),
            dcc.Input(id='input-weight', placeholder='Weight', type='number'),
            dcc.Input(id='input-acquisitionDate', placeholder='Acquisition Date YYYY-MM-DD', type='text'),
            dcc.Input(id='input-acquisitionCountry', placeholder='Acquisition Country', type='text'),
            dcc.Input(id='input-trainingStatus', placeholder='Training Status', type='text'),
            dcc.Checklist(id='input-reserved', options=[{'label': 'Reserved', 'value': 'reserved'}], value=[]),
            dcc.Input(id='input-inServiceCountry', placeholder='In Service Country', type='text'),
            dcc.Input(id='input-breed', placeholder='Breed', type='text'),
        ]), dog_btn_style, monkey_btn_style, reserve_btn_style

    elif action == 'intake_monkey':
        monkey_btn_style = {'display': 'inline-block'}
        return html.Div([
            dcc.Input(id='input-name', placeholder='Name', type='text'),
            dcc.Input(id='input-gender', placeholder='Gender', type='text'),
            dcc.Input(id='input-age', placeholder='Age', type='number'),
            dcc.Input(id='input-weight', placeholder='Weight', type='number'),
            dcc.Input(id='input-acquisitionDate', placeholder='Acquisition Date YYYY-MM-DD', type='text'),
            dcc.Input(id='input-acquisitionCountry', placeholder='Acquisition Country', type='text'),
            dcc.Input(id='input-trainingStatus', placeholder='Training Status', type='text'),
            dcc.Checklist(id='input-reserved', options=[{'label': 'Reserved', 'value': 'reserved'}], value=[]),
            dcc.Input(id='input-inServiceCountry', placeholder='In Service Country', type='text'),
            dcc.Input(id='input-tailLength', placeholder='Tail Length', type='text'),
            dcc.Input(id='input-species', placeholder='Species', type='text'),
            dcc.Input(id='input-height', placeholder='Height', type='text'),
            dcc.Input(id='input-bodyLength', placeholder='Body Length', type='text'),
        ]), dog_btn_style, monkey_btn_style, reserve_btn_style

    elif action == 'reserve_animal':
        reserve_btn_style = {'display': 'inline-block'}
        return html.Div([
            dcc.Input(id='input-reserve-name', placeholder='Animal Name to Reserve', type='text')
        ]), dog_btn_style, monkey_btn_style, reserve_btn_style

    else:
        # For listing options or initial state, no form or buttons shown
        return html.Div("Select an option and press the button (if applicable) to see results."), dog_btn_style, monkey_btn_style, reserve_btn_style


@app.callback(
    Output('output-message', 'children'),
    Output('animal-table', 'data'),
    Output('animal-table', 'columns'),
    Input('btn-add-dog', 'n_clicks'),
    Input('btn-add-monkey', 'n_clicks'),
    Input('btn-reserve', 'n_clicks'),
    Input('action-select', 'value'),
    State('input-name', 'value'),
    State('input-gender', 'value'),
    State('input-age', 'value'),
    State('input-weight', 'value'),
    State('input-acquisitionDate', 'value'),
    State('input-acquisitionCountry', 'value'),
    State('input-trainingStatus', 'value'),
    State('input-reserved', 'value'),
    State('input-inServiceCountry', 'value'),
    State('input-breed', 'value'),
    State('input-tailLength', 'value'),
    State('input-species', 'value'),
    State('input-height', 'value'),
    State('input-bodyLength', 'value'),
    State('input-reserve-name', 'value'),
    prevent_initial_call=True
)
def handle_actions(btn_add_dog, btn_add_monkey, btn_reserve, action, name, gender, age, weight, acquisitionDate, acquisitionCountry, trainingStatus, reserved, inServiceCountry, breed, tailLength, species, height, bodyLength,reserve_name):
    ctx = dash.callback_context
    if not ctx.triggered:
        return '', [], []

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    msg = ''

    if button_id == 'btn-add-dog':
        animal = {
            "name": name,
            "animalType": "Dog",
            "gender": gender,
            "age": age,
            "weight": weight,
            "acquisitionDate": acquisitionDate,
            "acquisitionCountry": acquisitionCountry,
            "trainingStatus": trainingStatus,
            "reserved": bool(reserved),
            "inServiceCountry": inServiceCountry,
            "breed": breed
        }
        db.create(animal)
        msg = f"Dog '{name}' added."

    elif button_id == 'btn-add-monkey':
        animal = {
            "name": name,
            "animalType": "Monkey",
            "gender": gender,
            "age": age,
            "weight": weight,
            "acquisitionDate": acquisitionDate,
            "acquisitionCountry": acquisitionCountry,
            "trainingStatus": trainingStatus,
            "reserved": bool(reserved),
            "inServiceCountry": inServiceCountry,
            "tailLength": tailLength,
            "species": species,
            "height": height,
            "bodyLength": bodyLength
        }
        db.create(animal)
        msg = f"Monkey '{name}' added."

    elif button_id == 'btn-reserve':
        if reserve_name:
            updated = db.reserve(reserve_name)
            msg = f"Animal '{reserve_name}' reserved." if updated else f"No animal named '{reserve_name}' found."
        else:
            msg = "Please enter an animal name to reserve."

    # Listing based on selected action
    if action == 'list_dogs':
        animals = db.read(filter={"animalType": "Dog"})
    elif action == 'list_monkeys':
        animals = db.read(filter={"animalType": "Monkey"})
    elif action == 'list_unreserved':
        animals = db.read(filter={"reserved": False})
    elif action == 'list_all':
        animals = db.read()
    else:
        animals = db.read()

    if animals:
        columns = [{"name": k, "id": k} for k in animals[0].keys()]
    else:
        columns, animals = [], []

    return msg, animals, columns


if __name__ == '__main__':
    app.run(debug=True, port=8050)