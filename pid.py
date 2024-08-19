# pip install plotly pandas
import plotly.express as px
import pandas as pd

kp = 0.7
ki = 0.5
kd = 0

setpoint = 100
setpoints = [setpoint]
commands = [0]
measureds = [0]
errors = [setpoints[0] - measureds[0]]
feedforward = 0

integrator = 0

nsteps = 50
time_constant = 1

for step in range(1, nsteps, time_constant):
    setpoints.append(setpoint if step < 10 else 40)

    # calc error
    error = setpoints[step-1] - measureds[step-1] # the last value we measured

    # calc pterm
    pterm = kp * error

    # calc iterm
    integrator = integrator + ((error*ki) * time_constant)

    # calc dterm
    dterm = kd * (error-errors[step-1]) / time_constant

    # calc output
    command = pterm + integrator # + dterm + ffterm
    commands.append(command)

    # calc process var
    measured = (command-commands[step-1])*0.8 + commands[step-1]*0.8
    measureds.append(measured)

    errors.append(error)


df = pd.DataFrame({
    "time": [i for i in range(0, nsteps, time_constant)],
    "setpoint": setpoints,
    "command": commands,
    "measured": measureds,
    "error": errors
})

fig = px.line(df,
    x="time",
    y=["setpoint", "command", "measured", "error"],
    color_discrete_sequence=["black", "red", "blue", "gray"],
    #hover_data={'x': ':.2f'},
    markers=True
)

fig.show()