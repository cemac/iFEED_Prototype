external_stylesheets = [
    '/static/styles/dash.css',
    '/static/styles/CEMACv1.css',
    '/static/styles/stylev1.css',
    'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
    'http://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800',
    'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css'
    ]

external_scripts = [
    'https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js',
    'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js'
    ]

meta_tags = [
    # A description of the app, used by e.g.
    # search engines when displaying search results.
    {
        'name': 'description',
        'content': 'My description'
    },
    # A tag that tells Internet Explorer (IE)
    # to use the latest renderer version available
    # to that browser (e.g. Edge)
    {
        'http-equiv': 'X-UA-Compatible',
        'content': 'IE=edge'
    },
    # A tag that tells the browser not to scale
    # desktop widths to fit mobile screens.
    # Sets the width of the viewport (browser)
    # to the width of the device, and the zoom level
    # (initial scale) to 1.
    #
    # Necessary for "true" mobile support.
    {
        'name': 'viewport',
        'content': 'width=device-width, initial-scale=1.0'
    }
    ]
