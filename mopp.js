var _pj;

function _pj_snippets(container) {
  function set_properties(cls, props) {
    var desc, value;
    var _pj_a = props;

    for (var p in _pj_a) {
      if (_pj_a.hasOwnProperty(p)) {
        value = props[p];

        if (!(value instanceof Map || value instanceof WeakMap) && value instanceof Object && "get" in value && value.get instanceof Function) {
          desc = value;
        } else {
          desc = {
            "value": value,
            "enumerable": false,
            "configurable": true,
            "writable": true
          };
        }

        Object.defineProperty(cls.prototype, p, desc);
      }
    }
  }

  container["set_properties"] = set_properties;
  return container;
}

_pj = {};

_pj_snippets(_pj);

class mopp {
  constructor(wpm = 20) {
    this.tx_wpm = wpm;
  }

  str2mopp(str) {
    var m;
    m = this.tx_protocol_version;
    m += bin(this.tx_serial).slice(2).zfill(6);
    m += bin(this.tx_wpm).slice(2).zfill(6);

    for (var c, _pj_c = 0, _pj_a = str, _pj_b = _pj_a.length; _pj_c < _pj_b; _pj_c += 1) {
      c = _pj_a[_pj_c];

      if (c === " ") {
        m += "11";
        continue;
      }

      for (var b, _pj_f = 0, _pj_d = this.morse[c.lower()], _pj_e = _pj_d.length; _pj_f < _pj_e; _pj_f += 1) {
        b = _pj_d[_pj_f];

        if (b === ".") {
          m += "01";
        } else {
          m += "10";
        }
      }

      m += "00";
    }

    m = m.slice(0, -2) + "11";
    m = m.ljust(Number.parseInt(8 * ceil(m.length / 8.0)), "0");
    this.tx_serial += 1;
    return this.bit2str(m);
  }

  bit2str(bit) {
    var m, res;
    m = bit;
    res = "";

    for (var i = 0, _pj_a = m.length; i < _pj_a; i += 8) {
      res += chr(Number.parseInt(m.slice(i, i + 8), 2));
    }

    return res;
  }

  decodePacket(packet) {
    /*
    //// byte 1: header; first two bits are the protocol version (curently 01), plus 6 bit packet serial number (starting from random)
    //// byte 2: first 6 bits are wpm (must be between 5 and 60; values 00 - 04 and 61 to 63 are invalid), the remaining 2 bits are already data payload!
     */
    var bits, l, msg;
    bits = 0;
    l = bits.length;
    this.rx_protocol_version = bits.slice(0, 2);
    this.rx_serial = bits.slice(3, 8);
    this.rx_wpm = Number.parseInt(bits.slice(9, 14), 2);
    msg = "";

    for (var i = 14, _pj_a = l; i < _pj_a; i += 2) {
      if (bits.slice(i, i + 2) === "01") {
        msg += ".";
      } else {
        if (bits.slice(i, i + 2) === "10") {
          msg += "-";
        } else {
          if (bits.slice(i, i + 2) === "00") {
            msg += " ";
          } else {
            if (bits.slice(i, i + 2) === "11") {
              msg += " ";
            }
          }
        }
      }
    }

    return msg;
  }

  mopp2str(packet) {
    var klist, msg, p, v, vlist;
    p = this.decodePacket(packet);
    klist = list(this.morse.keys());
    vlist = list(this.morse.values());
    msg = "";

    for (var c, _pj_c = 0, _pj_a = p.split(" "), _pj_b = _pj_a.length; _pj_c < _pj_b; _pj_c += 1) {
      c = _pj_a[_pj_c];
      v = list(this.morse.keys())[list(this.morse.values()).index(c)];
      msg += v;
    }

    return msg;
  }

}

_pj.set_properties(mopp, {
  "morse": {
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "a": ".-",
    "b": "-...",
    "c": "-.-.",
    "d": "-..",
    "e": ".",
    "f": "..-.",
    "g": "--.",
    "h": "....",
    "i": "..",
    "j": ".---",
    "k": "-.-",
    "l": ".-..",
    "m": "--",
    "n": "-.",
    "o": "---",
    "p": ".--.",
    "q": "--.-",
    "r": ".-.",
    "s": "...",
    "t": "-",
    "u": "..-",
    "v": "...-",
    "w": ".--",
    "x": "-..-",
    "y": "-.--",
    "z": "--..",
    "=": "-...-",
    "/": "-..-.",
    "+": ".-.-.",
    "-": "-....-",
    ".": ".-.-.-",
    ",": "--..--",
    "?": "..--..",
    ":": "---...",
    "!": "-.-.--",
    "'": ".----.",
    ";": "-.-.-.",
    "&": ".-...",
    "@": ".--.-.",
    "\u00e4": ".-.-",
    "\u00f6": "---.",
    "\u00fc": "..--",
    "ch": "----",
    "\"": ".-..-.",
    "(": "-.--.",
    ")": "-.--.-",
    "<sk>": "...-.-",
    "<bk>": "-...-.-",
    " ": ""
  },
  "rx_protocol_version": "01",
  "rx_serial": 1,
  "tx_protocol_version": "01",
  "tx_serial": 1,
  "tx_wpm": 20,
  "tx_wpm": 20
});