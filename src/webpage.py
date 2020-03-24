# NOTE: written on a Windows machine
# relies heavily on bokeh 1.4.0 (one release behind present version), not tested with 2.0.0

def construct():

    import pandas as pd
    import os
    from datetime import datetime
    os.system("tzutil /s \"Eastern Standard Time\"") # windows alert!

    import matplotlib.pyplot as plt


    # -------------initialize data ----------------------------
    infections = pd.concat([pd.read_csv('../data/{}'.format(file), sep='\t', names=['datetime', 'infected_user', 'infected_comment',
                                                                      'cause_user', 'cause', 'cause_type'],
                                       parse_dates=['datetime'])
               for file in os.listdir('../data') if 'infections' in file],
              axis=0, ignore_index=True).set_index('infected_user').sort_values('datetime', ascending=True)

    # drop weird duplicates
    infections = infections.loc[~infections.index.duplicated(keep='first')]

    comments = pd.concat([pd.read_csv('../data/{}'.format(file), sep='\t', names=['datetime', 'comment_user', 'comment', 'parent_user', 'parent',
                                                                     'parent_type', 'parent_inf'],
                                       parse_dates=['datetime'])
               for file in os.listdir('../data') if 'comments' in file],
              axis=0, ignore_index=True).set_index('comment')

    # clean up the microseconds where one file overlaps the hour, if applicable
    if infections['datetime'].max().hour!=comments['datetime'].max().hour:
        cutoff = min(infections['datetime'].max(), comments['datetime'].max())

        comments = comments[comments['datetime']<=cutoff]
        infections = infections[infections['datetime']<=cutoff]


    # indicate whether user was infected when they made the comment
    comments['user_status'] = 0
    f = comments.merge(infections, left_on='comment_user', right_index=True, suffixes=('_comment', '_infected'),
                  how='inner')
    comments.loc[f[f['datetime_comment']>f['datetime_infected']].index, 'user_status'] = 1
    del f

    # ---------------- create visualizations----------------------
    from bokeh.io import show
    from bokeh.themes import built_in_themes

    from bokeh.io import curdoc
    curdoc().theme = 'dark_minimal'

    from bokeh.plotting import figure
    from bokeh.layouts import widgetbox
    from bokeh.models import ColumnDataSource, HoverTool, DatetimeTickFormatter, NumeralTickFormatter, Band, Label, DataTable, TableColumn

    # vis 1
    hover = HoverTool(tooltips=[
        ("% of comments containing virus", "@y{%0%}"),
        ("# of comments", "@scale{0,0}"),
        ("Hour", '@x{%I:%M %p EST, %b %d}')],
        formatters={'x': 'datetime'}
        )

    fig1 = figure(title='Pandemic spread (comments made during event)',
                 plot_width=500, plot_height=300, tools=[hover,"ywheel_zoom,pan,reset"], y_range=(0,1),
                x_axis_type='datetime')

    x = comments.groupby(pd.Grouper(key='datetime', freq='H'))['user_status'].mean()
    data = ColumnDataSource(data=dict(y=x.values, x=x.index.values,
                                     scale=comments.groupby(pd.Grouper(key='datetime', freq='H')).size().values))

    fig1.line(y='y',x='x', line_width=2, source=data, color='red')

    fig1.xaxis.formatter=DatetimeTickFormatter(
            hours=["%I:%M %p EST, %b %d"],
            days=["%I:%M %p EST, %b %d"])
    fig1.xaxis.major_label_orientation = 3.14/4

    band = Band(base='x', upper='y', source=data, level='underlay',
                fill_alpha=0.35, fill_color='red')
    fig1.add_layout(band)

    fig1.yaxis.formatter = NumeralTickFormatter(format="%0%")
    fig1.yaxis.axis_label = '% of comments'

    # vis 2
    hover = HoverTool(tooltips=[
        ("% of users infected", "@ratio{%0%}"),
        ("# of infected users", "@y{0,0}"),
        ("# of active users", "@active{0,0}"),
        ("Hour", '@x{%I:%M %p EST, %b %d}')],
        formatters={'x': 'datetime'}
        )

    fig2 = figure(title='Pandemic spread (users active during event)',
                 plot_width=500, plot_height=300, tools=[hover,"ywheel_zoom,pan,reset"], y_range=(0,1),
                x_axis_type='datetime')

    x = infections.groupby(pd.Grouper(key='datetime', freq='H')).size().cumsum()

    active_users = pd.concat([comments.set_index('comment_user')['datetime'],
               infections['datetime']]).sort_values(ascending=False).groupby(level=0).first().reset_index().groupby(pd.Grouper(key='datetime', freq='H')).size()[1:].cumsum()
    active_users = active_users.reindex(x.index, fill_value=active_users.min())

    data = ColumnDataSource(data=dict(y=x.values, x=x.index.values,
                                     active=active_users.values,
                                     ratio=x.values/active_users.values))

    main_line = fig2.line(y='ratio',x='x', line_width=2, source=data, color='red')

    hover.renderers =[main_line]

    fig2.xaxis.formatter=DatetimeTickFormatter(
            hours=["%I:%M %p EST, %b %d"],
            days=["%I:%M %p EST, %b %d"])
    fig2.xaxis.major_label_orientation = 3.14/4

    band = Band(base='x', upper='ratio', source=data, level='underlay',
                fill_alpha=0.35, fill_color='red')
    fig2.add_layout(band)

    fig2.yaxis.formatter = NumeralTickFormatter(format="%0%")
    fig2.yaxis.axis_label = '% of active users'

    # ---------------- create tables----------------------
    from bokeh.models.widgets import Tabs, Panel

    #table 1
    data = infections.groupby('cause_user')['cause_type'].value_counts().unstack(fill_value=0).loc[infections['cause_user'].value_counts().nlargest(20).index]
    data = ColumnDataSource(data=dict(C=data['C'], S=data['S'],
                                     names=data.index, rank=range(1, len(data)+1)
                                     ))

    columns = [
            TableColumn(field="names", title="User"),
            TableColumn(field="rank", title="Ranking"),
            TableColumn(field="C", title="Infections via comment"),
            TableColumn(field="S", title="Infections via submission"),
        ]

    tab1 = DataTable(source=data, columns=columns, width=1000, index_position=None)
    pan1 = Panel(child=tab1,title="Best infectors")

    # table 2
    a = comments[~comments['comment_user'].isin(infections.index)].set_index('comment_user')

    a = a[a['parent_inf']!='N'].groupby(level=0)['parent_type'].value_counts().unstack(fill_value=0)

    data = a.loc[a.sum(axis=1).nlargest(20).index]

    data = ColumnDataSource(data=dict(C=data['C'], S=data['S'],
                                     names=data.index, rank=range(1, len(data)+1)
                                     ))

    columns = [
            TableColumn(field="names", title="User"),
            TableColumn(field="rank", title="Ranking"),
            TableColumn(field="C", title="# of comments under infected user"),
            TableColumn(field="S", title="# of comments on infected thread"),
        ]

    tab2 = DataTable(source=data, columns=columns, width=1000, index_position=None)
    pan2 = Panel(child=tab2,title="Most resilient")

    tabs = Tabs(tabs=[pan1, pan2]) # put tables in same object

    # ---------------------------------- make webpage itself --------------------
    # script for countdown shamelessly copied from https://www.w3schools.com/howto/howto_js_countdown.asp
    countdown_script = '''
    <script>
    // Set the date we're counting down to
    var countDownDate = new Date("Apr 1, 2020 00:00:00 EDT").getTime();
    
    // Update the count down every 1 second
    var x = setInterval(function() {
    
      // Get today's date and time
      var now = new Date().getTime();
        
      // Find the distance between now and the count down date
      var distance = countDownDate - now;
        
      // Time calculations for days, hours, minutes and seconds
      var days = Math.floor(distance / (1000 * 60 * 60 * 24));
      var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      var seconds = Math.floor((distance % (1000 * 60)) / 1000);
        
      // Output the result in an element with id="demo"
      document.getElementById("demo").innerHTML = days + "d " + hours + "h "
      + minutes + "m " + seconds + "s remaining";
        
      // If the count down is over, write some text 
      if (distance < 0) {
        clearInterval(x);
        document.getElementById("demo").innerHTML = "INFECTION COMPLETE";
      }
    }, 1000);
    </script>'''

    import io
    from bokeh.embed import components
    from bokeh.resources import CDN
    from jinja2 import Template

    # template for entire document
    template = Template(
        '''<!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="utf-8">
                    <title>Memonavirus Stats</title>
                    {{ resources }}
                    {{ script }}
                    
                    ---replace here---
                    <style>
                        p {
                            text-align: center;
                            font-size: 20px;
                            margin-top: 10px;
                            color: white;
                            width: 100%;
                        }
                        .embed-wrapper {
                            display: flex;
                            justify-content: space-evenly;
                        }
                        .warning {
                            text-align: center;
                            font-size: 60px;
                            margin-top: 0px;
                            color: red;
                        }
                        .demo {
                          text-align: center;
                          font-size: 40px;
                          margin-top: 0px;
                          color: white;
                          width: 100%;
                        }
                    </style>
                </head>
                
                <body style="background-color:black">
                    <div class="embed-wrapper">
                        {{ div }}
                    </div>
                </body>
            </html>
            '''.replace('---replace here---', countdown_script))

    # make the other HTML elements
    from bokeh.layouts import column, row
    from bokeh.models import Div

    header = Div(text='''<div class="warning">{:,} users infected!</div>'''.format(infections.index.nunique()))
    countdown = Div(text='''<div width="100%"><p id="demo">Loading...</p><div>''', width=800)
    blank_space = Div(text="""""", height=30)
    disclaimer = Div(text='''<p>Last updated at: {}<p>'''.format(datetime.now().strftime('%I:%M %p EST, %b %d')))

    # align everything into a single layout
    composite_layout = column(header, countdown, row(fig1, fig2), blank_space, tabs, disclaimer)

    # render everything together
    script_bokeh, div_bokeh = components(composite_layout)
    resources_bokeh = CDN.render()

    html = template.render(resources=resources_bokeh,
                           script=script_bokeh,
                           div=div_bokeh)
    # save to file
    out_file_path = "../html/index.html"
    with io.open(out_file_path, mode='w') as f:
        f.write(html)

if __name__ == "__main__":
    construct()
