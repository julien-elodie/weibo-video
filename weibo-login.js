var request = require('request');
var promise = require('promise');
// var ursa = require('ursa');
var bignumber = require('bignumber.js');
// var iconv = require('iconv-lite');
var python = require('python.js');

var url = 'https://login.sina.com.cn/signup/signin.php?entry=sso';

// var user = process.argv[2];
// var pass = process.argv[3];

// console.log(user, pass);

function simulateUserLogging(user, pass) {
    return new Promise(function(resolve, reject) {
        var data = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'qrcode_flag': false,
            'useticket': '1',
            'pagerefer': 'http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl',
            'vsnf': '1',
            'su': '',
            'service': 'miniblog',
            'servertime': '',
            'nonce': '',
            'pwencode': 'rsa2',
            'rsakv': '',
            'sp': '',
            'sr': '1366*768',
            'encoding': 'UTF-8',
            // 'prelt': '955',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META',
        }
        resolve(data);
    })
}

var login = {
    login(user, pass, callback) 
    {
        simulateUserLogging(user, pass)
            .then(function(data) {
                data.su = Buffer(user).toString('base64');
                var prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&' +
                    'su=' + data.su + '&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)';
                // console.log(data);
                return new Promise(function(resolve, reject) {
                    request.get(prelogin_url, function(err, res, body) {
                        if (!err && res.statusCode == 200) {
                            body = body.match(/[{][\s\S]*[}]/);
                            body = JSON.parse(body[0]);
                            data.servertime = body.servertime.toString();
                            data.nonce = body.nonce;
                            data.rsakv = body.rsakv;

                            /*
                            // RSA2 failed
                            pubkey = new bignumber(body.pubkey, 16)
                                // console.log(body.pubkey);
                                // console.log(pubkey.c);
                            var rsakey = '';
                            for (var i = 0; i <= pubkey.c.length - 1; i++) {
                                rsakey = rsakey + pubkey.c[i].toString();
                            }
                            // console.log(rsakey);
                            var key = ursa.createPublicKeyFromComponents(
                                new Buffer(rsakey, 'hex'),
                                // new Buffer('65537', 'hex')
                                new Buffer('65537', 'hex')
                            );
                            // console.log(key);
                            const message = [data.servertime, data.nonce].join("\t") + "\n" + pass;
                            // console.log(message);
                            secret = key.encrypt(
                                    message,
                                    'utf8',
                                    'hex',
                                    ursa.RSA_PKCS1_PADDING
                                    // ursa.RSA_PKCS1_OAEP_PADDING
                                )
                                // console.log(secret);
                            */

                            // python
                            var sys = python.import('sys');

                            sys.path.append(__dirname);

                            var encrypt = python.import('encrypt');

                            secret = encrypt.get_sp(body.pubkey, body.servertime, body.nonce, pass)
                                // console.log(secret);

                            data.sp = secret;
                            resolve(data);
                        }
                    });
                })
            })
            .then(function(data) {
                // console.log(data);
                post_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
                return new Promise(function(resolve, reject) {
                    request
                        .post({
                            url: post_url,
                            form: data,
                        }, function(err, res, body) {
                            // body = iconv.decode(body, 'GBK');
                            // console.log(body);
                            body = body.match(/replace\([\'"](.*?)[\'"]\)/);
                            // console.log(body[1]);
                            resolve(body[1]);
                        });
                })
            })
            .then(function(url) {
                // console.log(url);

                url_base = 'http://weibo.com/login.php'

                var j = request.jar()
                request({
                    url: url_base,
                    jar: j
                }, function() {
                    var cookie_string = j.getCookieString(url);
                    // console.log(cookie_string);
                    var cookies = j.getCookies(url);
                    // console.log(cookies);
                })

                return new Promise(function(resolve, reject) {
                    request
                        .get({
                            url: url,
                            jar: j
                        }, function(err, res, body) {
                            if (!err && res.statusCode == 200) {
                                // body = body.match(/replace\([\'"](.*?)[\'"]\)/);
                                body = body.match(/"uniqueid":"(\d+)",/)
                                    // console.log(body[1]);
                                resolve([
                                    body[1],
                                    j
                                ]);
                            }
                        })
                })
            })
            .then(function(param) {
                uid = param[0];
                j = param[1];

                url = 'http://weibo.com/u/' + uid;
                request
                    .get({
                        url: url,
                        jar: j
                    }, function(err, res, body) {
                        if (!err && res.statusCode == 200) {
                            // console.log(body);
                            console.log('login sucess!')
                        }
                    });
                callback(j);
            })
    }
}

module.exports = login;