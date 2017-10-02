import pandas
import matplotlib.pyplot as plt
import seaborn
seaborn.set_style("whitegrid")
seaborn.despine()

def plot_results(path, log_filename, graphs_info=False):
    """Plot several results"""
    # Path of the logs
    log_path = path + log_filename

    # Read log
    log = pandas.read_csv(log_path, index_col=0, parse_dates=[1])

    if not graphs_info:
        graphs = [{'keys': ['get_booster_earth', 'put_booster_earth'],
                   'title': 'Earth booster'},
                  {'keys': ['get_tank_earth', 'put_tank_earth'],
                   'title': 'Earth tank'},
                  {'keys': ['get_heartofgold_earth', 'put_heartofgold_earth'],
                   'title': 'Earth heartofgold'},
                  {'keys': ['get_booster_earth_graveyard', 'put_booster_earth_graveyard'],
                   'title': 'Earth graveyard booster'},
                  {'keys': ['get_tank_earth_graveyard', 'put_tank_earth_graveyard'],
                   'title': 'Earth graveyard tank'},
                  {'keys': ['get_heartofgold_earth_graveyard', 'put_heartofgold_earth_graveyard'],
                   'title': 'Earth graveyard heartofgold'},
                  {'keys': ['get_heartofgold_mars', 'put_heartofgold_mars'],
                   'title': 'Mars heartofgold'},
                   ]

    for graph in graphs:
        xy = create_timeserie(graph['keys'], log)
        plot_timeserie(xy, log, graph['title'], save=path + graph['title'] + '.png')

def create_timeserie(keys, log, freq='1D'):
    """Create a time series with keys"""
    # Filter keys
    data = log[log.key.isin(keys)]

    # Get unique dates
    x_set = pandas.unique(data['datetime'])

    # Get last value for each unique date
    data_set = []
    for x in x_set:
        data_set.append(data[data['datetime'] == x].iloc[-1])

    # Recreate a dataframe and resample to 1 day
    if len(data_set) == 0:
        # Couldn't find the key words in logs
        xy = pandas.DataFrame(columns=['datetime', 'value'])
        print('Warning: no logs for ' + str(keys))
    else:
        xy = pandas.DataFrame(data_set)[['datetime', 'value']]
        xy = xy.set_index(['datetime'])
        xy = xy.resample(freq).ffill()
    return xy

def plot_timeserie(timeserie, log, title='no title', ylabel='Stock', save=False, dpi=200):
    """Plot timeserie"""
    plt.figure(figsize=(10, 5))
    plot_window_open(log)
    plt.plot(timeserie)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel('Time')
    if save:
        plt.savefig(save, dpi=dpi)
        plt.close()
    else:
        plt.show()

def plot_window_open(log):
    """Plot line at window opening"""
    # Find date of window opening
    dates = log[log.key == 'launch_window_open'].datetime.tolist()

    # Plot lines
    for date in dates:
        plt.axvline(date, linewidth=4, color='r', alpha=0.5)
