from dash import Dash, html, dcc, dash_table, Input, Output, State, ctx
import dash_bootstrap_components as dbc
from animalReserveShelter import animalReserveShelter

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

db = animalReserveShelter()
animals = db.read()
columns = [{"name": k, "id": k} for k in animals[0].keys()] if animals else []

# Main layout
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
                value='list_all',
                inline=True,
                style={"padding": "10px"}
            )
        ])
    ]),

    html.Hr(),
    html.Div(id='action-form'),

    # Action buttons
    dbc.Button('Add Dog', id='btn-add-dog', color='primary', className='mt-2', style={'display': 'none'}),
    dbc.Button('Add Monkey', id='btn-add-monkey', color='primary', className='mt-2', style={'display': 'none'}),
    dbc.Button('Reserve Animal', id='btn-reserve', color='warning', className='mt-2', style={'display': 'none'}),

    # Table
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
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
    ),

    html.Div(id='output-message', className='mt-3')
])

# Display appropriate form and buttons
@app.callback(
    Output('action-form', 'children'),
    Output('btn-add-dog', 'style'),
    Output('btn-add-monkey', 'style'),
    Output('btn-reserve', 'style'),
    Input('action-select', 'value')
)
def display_action_form(action):
    dog_btn_style = monkey_btn_style = reserve_btn_style = {'display': 'none'}
    form_fields = []

    common_fields = lambda: [
        dcc.Input(id='input-name', placeholder='Name', type='text'),
        dcc.Input(id='input-gender', placeholder='Gender', type='text'),
        dcc.Input(id='input-age', placeholder='Age', type='number'),
        dcc.Input(id='input-weight', placeholder='Weight', type='number'),
        dcc.Input(id='input-acquisitionDate', placeholder='Acquisition Date YYYY-MM-DD', type='text'),
        dcc.Input(id='input-acquisitionCountry', placeholder='Acquisition Country', type='text'),
        dcc.Input(id='input-trainingStatus', placeholder='Training Status', type='text'),
        dcc.Checklist(id='input-reserved', options=[{'label': 'Reserved', 'value': 'reserved'}], value=[]),
        dcc.Input(id='input-inServiceCountry', placeholder='In Service Country', type='text'),
    ]

    if action == 'intake_dog':
        dog_btn_style = {'display': 'inline-block'}
        form_fields = common_fields() + [
            dcc.Input(id='input-breed', placeholder='Breed', type='text'),
        ]

    elif action == 'intake_monkey':
        monkey_btn_style = {'display': 'inline-block'}
        form_fields = common_fields() + [
            dcc.Input(id='input-tailLength', placeholder='Tail Length', type='text'),
            dcc.Input(id='input-species', placeholder='Species', type='text'),
            dcc.Input(id='input-height', placeholder='Height', type='text'),
            dcc.Input(id='input-bodyLength', placeholder='Body Length', type='text'),
        ]

    elif action == 'reserve_animal':
        reserve_btn_style = {'display': 'inline-block'}
        form_fields = [
            dcc.Input(id='input-reserve-name', placeholder='Animal Name to Reserve', type='text')
        ]

    else:
        form_fields = [html.Div("Select an option and press the button (if applicable) to see results.")]

    return html.Div(form_fields), dog_btn_style, monkey_btn_style, reserve_btn_style

# Handle actions
@app.callback(
    Output('output-message', 'children'),
    Output('animal-table', 'data'),
    Output('animal-table', 'columns'),
    Input('btn-add-dog', 'n_clicks'),
    Input('btn-add-monkey', 'n_clicks'),
    Input('btn-reserve', 'n_clicks'),
    State('action-select', 'value'),
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
def handle_actions(btn_add_dog, btn_add_monkey, btn_reserve, action,
                   name, gender, age, weight, acquisitionDate, acquisitionCountry,
                   trainingStatus, reserved, inServiceCountry,
                   breed, tailLength, species, height, bodyLength, reserve_name):
    button_id = ctx.triggered_id
    msg = ''

    try:
        if button_id == 'btn-add-dog':
            db.create({
                "name": name, "animalType": "Dog", "gender": gender, "age": age, "weight": weight,
                "acquisitionDate": acquisitionDate, "acquisitionCountry": acquisitionCountry,
                "trainingStatus": trainingStatus, "reserved": bool(reserved),
                "inServiceCountry": inServiceCountry, "breed": breed
            })
            msg = f"Dog '{name}' added."

        elif button_id == 'btn-add-monkey':
            db.create({
                "name": name, "animalType": "Monkey", "gender": gender, "age": age, "weight": weight,
                "acquisitionDate": acquisitionDate, "acquisitionCountry": acquisitionCountry,
                "trainingStatus": trainingStatus, "reserved": bool(reserved),
                "inServiceCountry": inServiceCountry, "tailLength": tailLength,
                "species": species, "height": height, "bodyLength": bodyLength
            })
            msg = f"Monkey '{name}' added."

        elif button_id == 'btn-reserve':
            if reserve_name:
                updated = db.reserve(reserve_name)
                msg = f"Animal '{reserve_name}' reserved." if updated else f"No animal named '{reserve_name}' found."
            else:
                msg = "Please enter an animal name to reserve."

    except Exception as e:
        msg = f"Error: {str(e)}"

    # Read updated data
    if action == 'list_dogs':
        animals = db.read(filter={"animalType": "Dog"})
    elif action == 'list_monkeys':
        animals = db.read(filter={"animalType": "Monkey"})
    elif action == 'list_unreserved':
        animals = db.read(filter={"reserved": False})
    else:
        animals = db.read()

    columns = [{"name": k, "id": k} for k in animals[0].keys()] if animals else []

    return msg, animals, columns

if __name__ == '__main__':
    app.run(debug=True, port=8050)