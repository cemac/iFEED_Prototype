countrydict = {
    'MWI': 'Malawi',
    'TZA': 'Tanzania',
    'ZAF': 'South Africa',
    'ZMB': 'Zambia'
}

cropdict = {
    2: 'Maize',
    0: 'Potato',
    3: 'Soybean',
    1: 'Groundnut'
}

fielddict = {
    'yield': 'Yield',
    'biomass': 'Biomass',
    'dur': 'Duration',
    'plant_date': 'Planting Date'
}

quaddict = {
    'ZMB':{
        '00':'Low Climate Risk, High Market Connectivity',
        '01':'High Climate Risk, High Market Connectivity',
        '10':'Low Climate Risk, Low Market Connectivity',
        '11':'High Climate Risk, Low Market Connectivity'
    },
    'MWI':{
        '00':'Low Climate Risk, Good Policy Implementation',
        '01':'High Climate Risk, Good Policy Implementation',
        '10':'Low Climate Risk, Poor Policy Implementation',
        '11':'High Climate Risk, Poor Policy Implementation'
    },
    'TZA':{
        '00':'Low Climate Risk, High Technical Development',
        '01':'High Climate Risk, High Technical Development',
        '10':'Low Climate Risk, Low Technical Development',
        '11':'High Climate Risk, Low Technical Development'
    },
    'ZAF':{
        '00':'Low Climate Risk, Significant Land Reform',
        '01':'High Climate Risk, Significant Land Reform',
        '10':'Low Climate Risk, Little Land Reform',
        '11':'High Climate Risk, Little Land Reform'
    }
}
