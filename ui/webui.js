var express = require('express');
var app = express();
var exec = require('child_process').execSync;
var fs = require('fs');
var utils = require('./utils');

var port = (typeof process.argv[2] !== 'undefined') ? process.argv[2] : 3000;

var scriptpath = '/usr/local/sbin/managevpn.sh';

var status = "Ok";

var vpn1name = null, vpn2name = null, vpn3name = null, vpn4name = null;

var cmd = null;

try {
    vpn1name = exec(scriptpath+" info 1");
    vpn2name = exec(scriptpath+" info 2");
    vpn3name = exec(scriptpath+" info 3");
    vpn4name = exec(scriptpath+" info 4");
}
catch (e) {
   console.log(e);
}

app.set('view engine', 'ejs');

app.get('/', function (req, res) {
    res.redirect('/status');
})

app.get('/status', function (req, res) {
    var rndData = {
        status: status,
        vpn1name: vpn1name,
        vpn2name: vpn2name,
        vpn3name: vpn3name,
        vpn4name: vpn4name,
        vpn1: 'Off',
        vpn2: 'Off',
        vpn3: 'Off',
        vpn4: 'Off',
        clients: {}
    };

    xtrecent = fs.readFileSync('/proc/net/xt_recent/clients', 'utf8');
    ticksSinceBoot = parseFloat(exec("grep '^jiffies' /proc/timer_list | head -n 1 | cut -d ' ' -f 2"));
    rndData.clients = utils.getActiveClients(xtrecent, ticksSinceBoot);

    try {
        var output = exec(scriptpath+" status");
        if (output == 1)
            rndData.vpn1 = 'On';
        if (output == 2)
            rndData.vpn2 = 'On';
        if (output == 3)
            rndData.vpn3 = 'On';
        if (output == 4)
            rndData.vpn4 = 'On';

        if (status != "Disconnecting")
            if (output == 0)
                status = "Reconnecting";
            else
                status = "Ok";
        else if (output == 0)
            status = "Ok";
    }
    catch (e) { console.log(e); }
    finally {
        res.render('status', rndData);
    }
})

app.get('/connect/:id([0-9]+)', function (req, res) {
    status = "Reconnecting";
    try {
        exec(scriptpath+" connect "+req.params['id']);
    }
    catch (e) {}
    finally {
        res.redirect('/status');
    }
})

app.get('/disconnect', function (req, res) {
    status = "Disconnecting";
    try {
        exec(scriptpath+" disconnect");
    }
    catch (e) {}
    finally {
        res.redirect('/status');
    }
})

app.get('/shutdown', function (req, res) {
    status = "Powering off";
    try {
        exec("shutdown -h now");
    }
    catch (e) {}
    finally {
        res.redirect('/status');
    }
})

app.listen(port, function () {
  console.log('ViPi control listening on port '+port+' ...');
})
