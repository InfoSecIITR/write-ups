web/ Boot Failed:
This challenge was also interesting one.

https://ch641054151355.ch.eng.run/
First of all we checked gobuster on it but sadly nothing yield 200 OK 
Then we checked robots.txt
luckily there was an location to endpoint

Hello User:wave:, 
ThisApplication has rate limit: 100/hr ThisMight Help You: /e8e53a51ba308caf79e4628357787f65
Then to this endpoint we got a login page.
We forgot to look up the source code and tried SQLi and also Nosqli but nothing worked 
but finally we saw the source code and it was as below:

HTTP/2 200 OK
Date: Sat, 02 Mar 2024 13:44:55 GMT
Content-Type: application/javascript; charset=UTF-8
Content-Length: 1193
Server: nginx/1.25.4
X-Powered-By: Express
X-Ratelimit-Limit: 100
X-Ratelimit-Remaining: 90
X-Ratelimit-Reset: 1709390460
Accept-Ranges: bytes
Cache-Control: public, max-age=0
Last-Modified: Fri, 01 Mar 2024 09:25:56 GMT
Etag: W/"4a9-18df955a4a0"
console.log("<--system0:5yc0re-->");
document.getElementById('login-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    fetch('/auth', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
        credentials: 'include', // Include credentials in the request
    })
        .then(response => {
            if (response.ok) {
                // If the response is OK (status code 200-299), redirect to the protected page
                window.location.href = '/retroshop';
            } else {
                // If the response is not OK, log the status code
                if (response.status == 401) {
                    alert("Error: Invalid Username & Password")
                } else {
                    let resError = response.status;
                    alert(`Error: ${resError}`);
                }
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});
Then after looking at the source code We found 
console.log("<--system0:5yc0re-->");
which was quite unusual we tried it as username and password and it luckily worked

Then even after logging in we were not allowed to enter and it said only samarth can login
so we saw jwt token in the cookie and changed the username to Samarth
and finally entered…

Then we were given a shop machine which had Price of RAM was $8 and amount in wallet was $2

Then we intercepted the request and found 4 parameters as
price,wallet,hash1,hash2
and the respective code was as below:
	function _0x5933() {
    var _0x5cb948 = ['finalPrice', 'charCodeAt', '58323mjDghs', '18WIwleG', '714eYeaDT', '1942896RCOXXK', 'onload', 'replace', 'Final\x20Price:\x20$', 'itemCounter', 'text', '780DIlccu', '/buy', 'then', 'value', 'MD5', 'itemPrice', 'innerText', '45463sFtTDg', '5Chyxni', '637836IgAaEP', '12112sPcVLC', 'toString', 'getElementById', 'Server\x20error', '72ePkUML', '31924PZMEmO', 'stringify', '4821219ciiGrD'];
    _0x5933 = function() {
        return _0x5cb948;
    };
    return _0x5933();
}
var _0x5dd9b0 = _0x2bab;
(function(_0x4688c1, _0x5d3011) {
    var _0x4291a5 = _0x2bab,
        _0x5877ac = _0x4688c1();
    while (!![]) {
        try {
            var _0xa656a9 = -parseInt(_0x4291a5(0x157)) / 0x1 * (-parseInt(_0x4291a5(0x15d)) / 0x2) + parseInt(_0x4291a5(0x15c)) / 0x3 * (parseInt(_0x4291a5(0x156)) / 0x4) + -parseInt(_0x4291a5(0x16d)) / 0x5 * (parseInt(_0x4291a5(0x15f)) / 0x6) + parseInt(_0x4291a5(0x15e)) / 0x7 * (-parseInt(_0x4291a5(0x152)) / 0x8) + parseInt(_0x4291a5(0x159)) / 0x9 + -parseInt(_0x4291a5(0x165)) / 0xa * (parseInt(_0x4291a5(0x16c)) / 0xb) + -parseInt(_0x4291a5(0x16e)) / 0xc;
            if (_0xa656a9 === _0x5d3011) break;
            else _0x5877ac['push'](_0x5877ac['shift']());
        } catch (_0x40d319) {
            _0x5877ac['push'](_0x5877ac['shift']());
        }
    }
}(_0x5933, 0x4dec6), window[_0x5dd9b0(0x160)] = function() {
    updatePrice();
});

function updatePrice() {
    var _0x3b44e8 = _0x5dd9b0,
        _0x46c751 = parseFloat(document[_0x3b44e8(0x154)](_0x3b44e8(0x16a))[_0x3b44e8(0x16b)]),
        _0x449352 = document[_0x3b44e8(0x154)](_0x3b44e8(0x163))[_0x3b44e8(0x168)],
        _0x128027 = _0x46c751 * _0x449352;
    document[_0x3b44e8(0x154)](_0x3b44e8(0x15a))[_0x3b44e8(0x16b)] = 'Final\x20Price:\x20$' + _0x128027;
}

function increment() {
    var _0x696d33 = _0x5dd9b0,
        _0x5c3a1b = document[_0x696d33(0x154)](_0x696d33(0x163));
    _0x5c3a1b[_0x696d33(0x168)] = parseInt(_0x5c3a1b[_0x696d33(0x168)]) + 0x1, updatePrice();
}

function decrement() {
    var _0x396221 = _0x5dd9b0,
        _0x2b0bc2 = document[_0x396221(0x154)]('itemCounter');
    _0x2b0bc2[_0x396221(0x168)] > 0x1 && (_0x2b0bc2['value'] = parseInt(_0x2b0bc2[_0x396221(0x168)]) - 0x1, updatePrice());
}

function rotEnode(input) {
    var _0x2bcc9b = _0x5dd9b0;
    return input[_0x2bcc9b(0x161)](/[!-~]/g, function(_0x2d0c83) {
        var _0x33a703 = _0x2bcc9b;
        return String['fromCharCode']((_0x2d0c83[_0x33a703(0x15b)](0x0) + 0xe) % 0x5e + 0x21);
    });
}
const spell = '36cc6f4082acd41f3d05cc1d43387e70';

function _0x2bab(_0x1a7385, _0x2e0050) {
    var _0x59334c = _0x5933();
    return _0x2bab = function(_0x2bab14, _0x3345aa) {
        _0x2bab14 = _0x2bab14 - 0x152;
        var _0x64adbd = _0x59334c[_0x2bab14];
        return _0x64adbd;
    }, _0x2bab(_0x1a7385, _0x2e0050);
}

function buyNow() {
    var _0x2ff6b4 = _0x5dd9b0,
        _0x4b8702 = parseInt(document[_0x2ff6b4(0x154)](_0x2ff6b4(0x163))[_0x2ff6b4(0x168)]),
        _0x3a788f = parseFloat(document[_0x2ff6b4(0x154)](_0x2ff6b4(0x15a))[_0x2ff6b4(0x16b)][_0x2ff6b4(0x161)](_0x2ff6b4(0x162), '')),
        _0x566947 = CryptoJS[_0x2ff6b4(0x169)](_0x4b8702[_0x2ff6b4(0x153)]())[_0x2ff6b4(0x153)](),
        _0x35c26d = rotEnode((_0x3a788f + spell)['toString']()),
        _0x40ebe1 = {
            'amount': _0x4b8702,
            'price': _0x3a788f,
            'hash1': _0x566947,
            'hash2': _0x35c26d
        };
    fetch(_0x2ff6b4(0x166), {
        'method': 'POST',
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': JSON[_0x2ff6b4(0x158)](_0x40ebe1)
    })[_0x2ff6b4(0x167)](_0x10876e => {
        var _0x42057f = _0x2ff6b4;
        return _0x10876e[_0x42057f(0x164)]()['then'](_0x35b762 => {
            _0x10876e['ok'] ? alert(_0x35b762) : alert(_0x35b762);
        });
    })['catch'](_0xdabaa8 => {
        var _0x45ed2c = _0x2ff6b4;
        alert(_0x45ed2c(0x155));
    });
}

So basically we have to change the value of price to 3(anything less than wallet amount) and change the corresponding hash using the above code
So I made a script for calculating the hash

import hashlib
def rot_enode(input_string):
    return ''.join(chr((ord(c) + 0xE) % 0x5E + 0x21) if '!' <= c <= '~' else c for c in input_string)
def calculate_hash2(price):
   
    spell = '36cc6f4082acd41f3d05cc1d43387e70'
    
    price_str = str(price)   
   
    concat_str = price_str + spell
   
    hash2 = rot_enode(concat_str)
    
    return hash2
price = float(input("Enter the price: ")) 
hash2 = calculate_hash2(price)
print("hash2:", hash2)

So after changing hash and price we finally get the flag😊😊

VishwaCTF{s3r_y0u_d353rv3_t0_w1n}
