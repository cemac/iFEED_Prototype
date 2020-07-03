import dash
from flask import session

class CustomDash(dash.Dash):
    def interpolate_index(self, **kwargs):

        headerbar = '''
<div style="text-align: center; width: 100%;">
  <div class="headbox">
    <div class="headrow">
      <div class="divhead">
        <a href="http://africap.info"><img src="/static/logos/africap-logo.svg" alt="Africap Banner" style="float:left;width:100%;"></a>
      </div>
      <div>
        <a href="/" title="Climate Smart Food System Policy Pathway Tool" rel="home"><span style="font-size: 35px; color: #593c2f;">Climate Smart Food System Policy Pathway Tool</span></a><span style="font-size: 15px; color: #593c2f;"><br><b>i</b>ntegrated <b>F</b>uture <b>E</b>stimator for <b>E</b>missions and <b>D</b>iets</span>
      </div>
      <div class="divhead"></div>
    </div>
  </div>
</div>
        '''

        navbar1 = '''
<br>
<nav class="navbar-ifeed" style="background-color: #e56819">
  <div class="navcontainer" style="width:100%; margin:auto;">
    <div class="navbar-brand">
      <a href="/">Home</a>
    </div>
    <div id="navbar" class="collapse navbar-collapse">
      <ul class="nav navbar-nav">
        <li><a href="/about">About</a></li>
        <li><a href="/infopage1">Info Page 1</a></li>
        <li><a href="/infopage2">Info Page 2</a></li>
        <li><a href="/infopage3">Info Page 3</a></li>
        <li><a href="/glossary">Glossary</a></li>
        <li><a href="/contact">Contact</a></li>
      </ul>

      <ul class="nav navbar-nav navbar-right">
        '''
        navbar2 = ''
        if 'logged_in' in session:
            navbar3 = '''
        <li class="dropdown">
          <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Account<span class="caret"></span></a>
          <ul class="dropdown-menu">
            <li class="dropdown-header">Logged in as <b>'''+session['username']+'''</b></li>
            <li><a href=/change-pwd>Change Password</a> </li>
            <li><a href=/account/{{session.username}}>Account</a> </li>
            <li><a href=/logout>Logout </a> </li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
</nav>
            '''

            if session['usertype'] == "Admins":
                navbar2 = '''
          <li class="dropdown">
            <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Admin Menu<span class="caret"></span></a>
            <ul class="dropdown-menu">
              <li><a href="/admin/users">Users</a></li>
              <li><a href="/admin/information">Admin info</a></li>
            </ul>
          </li>
                '''
        else:
            navbar3 = '''
        <li><a href="/login"><span class="glyphicon glyphicon-log-in"> Login</a></li>
      </ul>
    </div>
  </div>
</nav>
<br>
            '''
        navbar=navbar1+navbar2+navbar3

        footer = '''
<hr>
<div class="footer" style="left: 30px; bottom: 0px; height: 68px; width: 85%; background: #FFFFFF; margin: 30px">
    <div  style="height: 14px;  float: left;">
  <a href="/copyright">COPYRIGHT AND DISCLAIMER</a>
  </div>
  <!--<div style="height: 14px; float: right;"><a href="/contribute">CONTRIBUTOR GUIDELINES</a>
  </div>-->
  <div style="height: 16px; text-align: center;">
    Website designed by <a href="https://www.cemac.leeds.ac.uk/" target="_blank">CEMAC</a>
    &copy; 2019 <a href="https://www.leeds.ac.uk/" target="_blank">University of Leeds</a>, Leeds, LS2 9JT
  </div style="height: 55px; ">
  <center>
    <a href="https://africap.info/">
      <img src="/static/logos/icon.svg" alt="GCRF AFRICAP logo" style="height:75px; width:auto; padding: 5px">
    </a>
    <a href="https://esrc.ukri.org/research/international-research/global-challenges-research-fund-gcrf/">
      <img src="/static/logos/GCRF-logo.jpg" alt="GCRF logo" style="height:75px; width:auto; padding: 5px">
    </a>
    <a href="https://www.fanrpan.org/">
      <img src="/static/logos/fanrpan-logo.jpg" alt="FANRPAN logo" style="height:75px; width:auto; padding: 5px">
    </a>
    <a href="http://esrftz.org/">
      <img src="/static/logos/esrf-logo.jpg" alt="ESRF logo" style="height:75px; width:auto; padding: 5px">
    </a>
    <a href="https://www.namc.co.za/">
      <img src="/static/logos/namc-logo.jpg" alt="NAMC logo" style="height:75px; width:auto; padding: 5px">
    </a>
    <a href="https://cisanetmalawi.org/">
      <img src="/static/logos/CISANET-logo.jpg" alt="CISANET logo" style="height:75px; width:auto; padding: 5px">
    </a>
    <a href="http://www.acfzambia.org/">
      <img src="/static/logos/acf-logo.png" alt="ACF logo" style="height:75px; width:auto; padding: 5px">
    </a>
  </center>

  <center>
    <a href="https://www.ukri.org/">
      <img src="/static/logos/UKRI-logo.png" alt="UKRI logo" style="height:75px; width:auto; padding: 5px">
    </a>
    <a href="https://www.chathamhouse.org/">
      <img src="/static/logos/chatham-logo.png" alt="Chatham House logo" style="height:75px; width:auto; padding: 5px">
    </a>
    <a href="https://www.metoffice.gov.uk/">
      <img src="/static/logos/mo-logo.jpg" alt="Met Office logo" style="height:75px; width:auto; padding: 5px">
    </a>
    <a href="http://www.leeds.ac.uk/">
      <img src="/static/logos/Leeds-logo.jpg" alt="Leeds logo" style="height:75px; width:auto; padding: 5px">
    </a>
    <a href="https://www.abdn.ac.uk/">
      <img src="/static/logos/uoab-logo.jpg" alt="Aberdeen logo" style="height:75px; width:auto; padding: 5px">
    </a>
  </center>

  <center>
    <a href="/privacy">Privacy</a>
  </center>
</div>
        '''

        return '''
        <!DOCTYPE html>
        <html>
            <head>
                {metas}
                <title>{title}</title>
                <link rel="shortcut icon" href=/static/icon.png> <link rel="icon" href="/static/icon.svg" sizes="192x192" />
                {css}
            </head>
            <body>
                {headerbar}
                {navbar}
                {app_entry}
                {config}
                {scripts}
                {renderer}
                {footer}
            </body>
        </html>
        '''.format(
            metas=kwargs['metas'],
            title='iFEED Tool Dashboard',
            css=kwargs['css'],
            headerbar=headerbar,
            navbar=navbar,
            app_entry=kwargs['app_entry'],
            config=kwargs['config'],
            scripts=kwargs['scripts'],
            renderer=kwargs['renderer'],
            footer=footer)
