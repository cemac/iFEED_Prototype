import dash
from flask import session

class CustomDash(dash.Dash):
    def interpolate_index(self, **kwargs):

        headerbar = '''
<header id="masthead" class="site-header">
  <div class="inside-header grid-container grid-parent" style="padding-left: 0px;padding-right: 0px;">
    <div class="site-logo col-12 col-md-6" style="padding-top: 0px;padding-bottom: 0px;padding-left: 0px;">
      <a href="https://africap.info/" title="GCRF-AFRICAP" rel="home">
        <img  class="header-image is-logo-image" alt="GCRF-AFRICAP" src="/static/logos/africap-logo.svg" title="GCRF-AFRICAP" />
      </a>
    </div>
    <div class="col-12 col-md-6">
      <a href="/" title="iFEED" rel="home">
        <img  class="header-image-2 is-logo-image" alt="iFEED" src="/static/logos/iFEED-logo.png" title="iFEED" />
        <!--<span style="font-size: 35px; color: #593c2f; font-weight:700;">iFEED</span>-->
      </a>
      <span style="font-size: 15px; color: #593c2f;"><br><b>i</b>ntegrated <b>F</b>uture <b>E</b>stimator for <b>E</b>missions and <b>D</b>iets</span>
    </div>
  </div>
</header>
        '''

        navbar1 = '''
<nav id="site-navigation" class="main-navigation sub-menu-right" itemtype="https://schema.org/SiteNavigationElement" itemscope>
  <div class="inside-navigation grid-container grid-parent">
    <button class="menu-toggle" aria-controls="primary-menu" aria-expanded="false">
    	<span class="mobile-menu">Menu</span>
    </button>
		<div id="primary-menu" class="main-nav">
      <ul class="">
        <li class="menu-item menu-item-type-post_type menu-item-object-page menu-item-home menu-item-11">
          <a href="/" aria-current="page">Home</a>
        </li>
        <li class="menu-item menu-item-type-post_type menu-item-object-page current-menu-item page_item page-item-1216 current_page_item menu-item-1098">
          <a href="/countries">iFEED Results</a>
        </li>
        <li class="menu-item menu-item-type-post_type menu-item-object-page menu-item-1142">
          <a href="/about">About iFEED</a>
        </li>
        <li class="menu-item menu-item-type-post_type menu-item-object-page menu-item-1095">
          <a href="/modelling">iFEED Methods</a>
        </li>
        <li class="menu-item menu-item-type-post_type menu-item-object-page menu-item-1222">
          <a href="/contact">Contact</a>
        </li>
      </ul>

      <ul class="navbar-right">
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
        <!--<li><a href="/login"><span class="glyphicon glyphicon-log-in"> Login</a></li>-->
      </ul>
    </div>
  </div>
</nav>
<br>
            '''
        navbar=navbar1+navbar2+navbar3

        footer = '''
<hr>
<div class="footer grid-container" style="bottom: 0px; height: 68px; background: #FFFFFF; margin: auto">
  <div style="margin:auto; text-align: center;">
    Website designed by <a href="https://www.cemac.leeds.ac.uk/" target="_blank">CEMAC</a>
    &copy; 2021 <a href="https://www.leeds.ac.uk/" target="_blank">University of Leeds</a>, Leeds, LS2 9JT
  </div>
  <div id="icons" style="width:75%; margin: auto;">
    <center>
      <br>
      <a href="https://esrc.ukri.org/research/international-research/global-challenges-research-fund-gcrf/">
        <img class=icon src="/static/logos/GCRF-logo.png" alt="GCRF logo">
      </a>
      <a href="https://www.fanrpan.org/">
        <img class=icon src="/static/logos/fanrpan-logo.jpg" alt="FANRPAN logo">
      </a>
      <a href="http://esrftz.org/">
        <img class=icon src="/static/logos/esrf-logo.jpg" alt="ESRF logo">
      </a>
      <a href="https://www.namc.co.za/">
        <img class=icon src="/static/logos/namc-logo.jpg" alt="NAMC logo">
      </a>
      <a href="https://cisanetmalawi.org/">
        <img class=icon src="/static/logos/CISANET-logo.jpg" alt="CISANET logo">
      </a>
      <a href="http://www.acfzambia.org/">
        <img class=icon src="/static/logos/acf-logo.png" alt="ACF logo">
      </a>
  <!--</center>

  <center>-->
      <a href="https://www.ukri.org/">
        <img class=icon src="/static/logos/UKRI-logo.png" alt="UKRI logo">
      </a>
      <a href="https://www.chathamhouse.org/">
        <img class=icon src="/static/logos/chatham-logo.png" alt="Chatham House logo">
      </a>
      <a href="https://www.metoffice.gov.uk/">
        <img class=icon src="/static/logos/mo-logo.jpg" alt="Met Office logo">
      </a>
      <a href="http://www.leeds.ac.uk/">
        <img class=icon src="/static/logos/Leeds-logo.jpg" alt="Leeds logo">
      </a>
      <a href="https://www.abdn.ac.uk/">
        <img class=icon src="/static/logos/uoab-logo.jpg" alt="Aberdeen logo">
      </a>
    </center>
  </div>
  <div class=horline>
    <div class="leftline"><a href="/privacy">Privacy</a></div>
    <div class="rightline"><a href="/copyright">COPYRIGHT AND DISCLAIMER</a></div>
  </div>
</div>
        '''

        return '''
        <!DOCTYPE html>
        <html>
            <head>
                {metas}
                <title>{title}</title>
                <link rel="shortcut icon" href=/static/logos/icon.svg> <link rel="icon" href="/static/logos/icon.svg" sizes="192x192" />
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
            title='iFEED - A Climate Smart Food System Policy Pathway Tool',
            css=kwargs['css'],
            headerbar=headerbar,
            navbar=navbar,
            app_entry=kwargs['app_entry'],
            config=kwargs['config'],
            scripts=kwargs['scripts'],
            renderer=kwargs['renderer'],
            footer=footer)
