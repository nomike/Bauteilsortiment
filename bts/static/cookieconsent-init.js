// obtain plugin
var cc = initCookieConsent();

// run plugin with your configuration
cc.run({
    current_lang: 'en',
    autoclear_cookies: true,                   // default: false
    page_scripts: true,                        // default: false

    // mode: 'opt-in'                          // default: 'opt-in'; value: 'opt-in' or 'opt-out'
    // delay: 0,                               // default: 0
    // auto_language: null                     // default: null; could also be 'browser' or 'document'
    // autorun: true,                          // default: true
    // force_consent: false,                   // default: false
    // hide_from_bots: true,                   // default: true
    // remove_cookie_tables: false             // default: false
    // cookie_name: 'cc_cookie',               // default: 'cc_cookie'
    // cookie_expiration: 182,                 // default: 182 (days)
    // cookie_necessary_only_expiration: 182   // default: disabled
    // cookie_domain: location.hostname,       // default: current domain
    // cookie_path: '/',                       // default: root
    // cookie_same_site: 'Lax',                // default: 'Lax'
    // use_rfc_cookie: false,                  // default: false
    // revision: 0,                            // default: 0

    onFirstAction: function(user_preferences, cookie){
        // callback triggered only once
    },

    onAccept: function (cookie) {
        // ...
    },

    onChange: function (cookie, changed_preferences) {
        // ...
    },

    languages: {
        'en': {
            consent_modal: {
                title: 'We use cookies!',
                description: 'Hi, this website uses the minimal amount of cookies necessary to function. To ensure its proper operation. Absolutely no tracking or advertisement cookies will be used. <button type="button" data-cc="c-settings" class="cc-link">Let me choose</button>',
                primary_btn: {
                    text: 'Accept all',
                    role: 'accept_all'              // 'accept_selected' or 'accept_all'
                },
            },
            settings_modal: {
                title: 'Cookie preferences',
                save_settings_btn: 'Save settings',
                accept_all_btn: 'Accept all',
                close_btn_label: 'Close',
                cookie_table_headers: [
                    {col1: 'Name'},
                    {col2: 'Domain'},
                    {col3: 'Expiration'},
                    {col4: 'Description'}
                ],
                blocks: [
                    {
                        title: 'Cookie usage 📢',
                        description: 'We use cookies to ensure the basic functionalities of the website. As this website only uses the minimal amount of cookies necessary to function, we do not offer any cookie settings. If you continue to use this site we will assume that you are happy with it.'
                    }, {
                        title: 'Strictly necessary cookies',
                        description: 'These cookies are essential for the proper functioning of my website. Without these cookies, the website would not work properly',
                        toggle: {
                            value: 'necessary',
                            enabled: true,
                            readonly: true          // cookie categories with readonly=true are all treated as "necessary cookies"
                        },
                        cookie_table: [             // list of all expected cookies
                            {
                                col1: 'sessionid',
                                col2: 'bauteilsortiment.nomike.com',
                                col3: '2 weeks',
                                col4: 'Stores the your session ID if you login to the backend.',
                            },
                            {
                                col1: 'csrftoken',
                                col2: 'bauteilsortiment.nomike.com',
                                col3: '1 year',
                                col4: 'Stores a token to prevent cross site request forgery attacks.',
                            },
                            {
                                col1: 'cc_cookie',
                                col2: 'bauteilsortiment.nomike.com',
                                col3: '6 months',
                                col4: 'Stores your consent to cookies.',
                            }
                        ]
                    }, {
                        title: 'More information',
                        description: 'For any queries in relation to our policy on cookies and your choices, please <a class="cc-link" href="https://nomike.com/card/">contact us</a>.',
                    }
                ]
            }
        }
    }
});