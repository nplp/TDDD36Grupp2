def init_ui(id='main'):
    """Build the UI."""
 
    global APP
    APP = ui.App('GPS Logger', id=id,
                 
                 menu=(
                       ui.Menu.Item(label='New', callback=on_new),
                       ui.Menu.Item(label='Open', callback=on_open),
                       ui.Menu.Item(label='Save', callback=on_save),
                       ui.Menu.Item(label='Save As', callback=on_save_as),
                       ),
                 
                 top=(
                      ui.Group('dev_stat', horizontal=True, border=None, 
                               children=(ui.Label(label='Status:'),
                                         ui.Label('status', 'Ready'),
                                         )
                               ),
                      ui.Group('controls', horizontal=True, border=None,
                               children=(ui.Button('start_btn',
                                                   label='Start',
                                                   callback=on_start),
                                         ui.Button('stop_btn',
                                                   label='Stop',
                                                   callback=on_stop))
                               ),
                      ),
                 
                 center=ui.Table('log', 'GPS Log',
                                 headers=('Time', 'Latitude',
                                          'Longitude',
                                          'Altitude (meters)'),
                                 types=(str, str, str, str)
                                 )
                 )
