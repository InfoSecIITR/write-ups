# Professor's Inheritance

*As we dive deeper into maths, it gets harder and harder. Mr. Rick a maths professor has also been facing such challenges. His mentor Mr. Newton left the key to his legacy encrypted in the following files but he has to prove that he is his student to get access to it. Help Mr.Rick solve the questions and decode the key.*

*Find the next number in the series. Series: 5, 12, 23, 50, 141, 488, 1859, 7326, ?*

Next number: `29177`

In the challenge we are given, `TunePocket-Rock-Guitar-Power-Intro-Preview.wav` and `encryptedcode.txt.nc` which is mcrypt encrypted file.

Using deepsound on the wav file we extract an image.

![prof_image](./assets/prof.png)

Running **stegosuite** on the image we find the following message

```
The letters of the word "VISHWA" are permuted in all possible ways and the words thus formed are arranged as in a dictionary. The rank of the word "VISHWA" is
Answer in the following format:
VISHWA-ANS
Example: Answer of above question is 127 then password for next file is:
VISHWA-127
```

Therefore,the password is `VISHWA-545`

Command: `mcrypt -d encryptedcode.txt.nc`

Using this password we get the `encryptedcode.txt` which has the following contents

```js
function _0x9b13(_0x2a7d1e, _0x2dc359) {
    const _0x59ade7 = _0x59ad();
    return _0x9b13 = function(_0x9b13d5, _0x72f1ea) {
        _0x9b13d5 = _0x9b13d5 - 0x1e3;
        let _0x37191c = _0x59ade7[_0x9b13d5];
        return _0x37191c;
    }, _0x9b13(_0x2a7d1e, _0x2dc359);
}
const _0x2eeaaf = _0x9b13;
(function(_0x3f030f, _0x4bf6b1) {
    const _0x490c84 = _0x9b13,
        _0x13dacc = _0x3f030f();
    while (!![]) {
        try {
            const _0x2ad922 = -parseInt(_0x490c84(0x1ec)) / 0x1 * (parseInt(_0x490c84(0x1ee)) / 0x2) + -parseInt(_0x490c84(0x1ed)) / 0x3 * (parseInt(_0x490c84(0x1ea)) / 0x4) + parseInt(_0x490c84(0x1e6)) / 0x5 + -parseInt(_0x490c84(0x1e8)) / 0x6 * (-parseInt(_0x490c84(0x1e4)) / 0x7) + parseInt(_0x490c84(0x1e9)) / 0x8 * (parseInt(_0x490c84(0x1e7)) / 0x9) + -parseInt(_0x490c84(0x1ef)) / 0xa + -parseInt(_0x490c84(0x1eb)) / 0xb;
            if (_0x2ad922 === _0x4bf6b1) break;
            else _0x13dacc['push'](_0x13dacc['shift']());
        } catch (_0x29f1d5) {
            _0x13dacc['push'](_0x13dacc['shift']());
        }
    }
}(_0x59ad, 0x2e67a));
let hexArray = ['56', '69', '73', '68', '77', '61', '43', '54', '46', '7b', '61', '34', '74', '68', '30', '72', '5f', '73', '61', '34', '79', '61', '7d'];

function _0x59ad() {
    const _0x174950 = ['1012WHsjvS', '651805BeNskl', '13031Kbcsug', '1845pCtCOx', '38eVCyrm', '1816090XhAWlX', 'length', 'fromCharCode', '643867uhhKfL', 'log', '1121035lmfkQH', '9iVMgaH', '18OJRFjA', '2671776GkWnpv'];
    _0x59ad = function() {
        return _0x174950;
    };
    return _0x59ad();
}

function hexToAscii(_0x5b4e2e) {
    const _0x13baed = _0x9b13;
    let _0x46040d = '';
    for (let _0x22baaa = 0x0; _0x22baaa < _0x5b4e2e[_0x13baed(0x1f0)]; _0x22baaa++) {
        _0x46040d += String[_0x13baed(0x1e3)](parseInt(_0x5b4e2e[_0x22baaa], 0x10));
    }
    return _0x46040d;
}
console[_0x2eeaaf(0x1e5)](hexToAscii(hexArray));
```

Observing carefully `hexArray` is the ascii values of the flag.

Flag: `VishwaCTF{a4th0r_sa4ya}` 