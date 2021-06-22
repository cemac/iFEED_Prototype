external_stylesheets = [
    '/static/styles/africap_mobile.css',
    '/static/blocks.style.build.css',
    '/static/events_manager.css',
    '/static/styles/font-icons.min.css',
    '/static/styles/fontawesome.min.css',
    '/static/styles/africap.css',
    '/static/styles/unsemantic-grid.min.css',
    '/static/styles/UoL_style.css',
    '/static/styles/wp_style.min.css',
    '/static/styles/inline.css',
    '/static/styles/dash.css',
    '/static/styles/CEMACv1.css',
    '/static/styles/stylev1.css',
    'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
    'http://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800',
    'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css'

    ]

external_scripts = [
    '/static/js/menu.min.js',
    '/static/js/main.min.js',
    'https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js',
    'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js'
    ]

meta_tags = [
    # A description of the app, used by e.g.
    # search engines when displaying search results.
    {
        'name': 'iFEED',
        'content': 'Integrated Assessment Framework providing a Climate-Smart Policy Pathway tool '
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
