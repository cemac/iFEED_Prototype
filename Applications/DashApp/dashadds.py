external_stylesheets = [
    'https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css',
    'https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css',
    'https://fonts.googleapis.com/css?family=Roboto:100,100italic,300,300italic,regular,italic,500,500italic,700,700italic,900,900italic|Roboto+Condensed:300,300italic,regular,italic,700,700italic',
    '/static/styles/wp_style.min.css',
    '/static/styles/blocks.style.build.css',
    '/static/styles/events_manager.css',
    '/static/styles/unsemantic-grid.min.css',
    '/static/styles/africap.css',
    '/static/styles/inline.css',
    '/static/styles/africap_mobile.css',
    '/static/styles/font-icons.min.css',
    '/static/styles/UoL_style.css',
    '/static/styles/stylev1.css',
    '/static/styles/scenario.css',
    '/static/styles/dash.css',
    '/static/styles/CEMACv1.css'
    ]

external_scripts = [
    '/static/js/menu.min.js',
    '/static/js/main.min.js',
    'https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js',
    'https://cdn.jsdelivr.net/npm/vue@2.5.13/dist/vue.js',
    'https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js',
    'https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.min.js'
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
