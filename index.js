var request = require('request');
var cheerio = require('cheerio');

var login = require('sina_login');

var user = '15168173848';
var pass = 'wyq2644756656';

var url = 'https://weibo.com/tv';

var count = 0;

// login in weibo
login.login(user, pass, function(j) {
    // console.log(j);
    request
        .get({
            url: url,
            jar: j
        }, function(err, res, body) {
            if (!err && res.statusCode == 200) {
                // console.log(body);
                var $ = cheerio.load(body);

                $('.L_ctit.W_f20.clearfix').each(function(item) {
                    var url_sub_pre = $(this).find('a');
                    var url_sub = url_sub_pre.attr('href');

                    // console.log(url_sub);
                    url_sub = 'https://weibo.com' + url_sub;

                    // get subpage
                    request
                        .get({
                            url: url_sub,
                            jar: j
                        }, function(err, res, body) {
                            if (!err && res.statusCode == 200) {
                                var $ = cheerio.load(body);

                                $('.weibo_tv_frame').each(function(item) {
                                    var href = $(this).find('.li_list_1').children('a');

                                    href.each(function(item) {
                                        var url_sub_sub = $(this).attr('href');

                                        // console.log(url_sub_sub);
                                        url_sub_sub = 'https://weibo.com' + url_sub_sub;

                                        // get videopage
                                        request
                                            .get({
                                                url: url_sub_sub,
                                                jar: j
                                            }, function(err, res, body) {
                                                if (!err && res.statusCode == 200) {
                                                    var $ = cheerio.load(body);

                                                    $('#playerRoom.weibo_player_fa').each(function(item) {
                                                        var data_pre = $(this).find('div');
                                                        var data = data_pre.attr('action-data');

                                                        data = data.split('&');
                                                        data = data[5].match(/\=(.*)/)[1];
                                                        data = decodeURIComponent(data);

                                                        url_video = 'http:'+data;

                                                        console.log(url_video);
                                                    })
                                                }
                                            })
                                    })
                                })
                            }
                        })
                })
            }
        })
});
