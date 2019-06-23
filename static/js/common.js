/**
* String.format
* 例：String.format("今日は{0}年{1}月{2}日", year, month, date)
*     String.format("hello {0} {1}",'world',' tre')
*/
String.format = function () {
    var param = [];
    for (var i = 0, l = arguments.length; i < l; i++) {
        param.push(arguments[i]);
    }
    var statment = param[0]; // get the first element(the original statement)
    param.shift(); // remove the first element from array
    return statment.replace(/\{(\d+)\}/g, function (m, n) {
        return param[n];
    });
}
/**
* 端末判断
* 例：
*/
DeviceTool = {
    isWindows: /windows/i.test(navigator.userAgent),
    isAndroid: /Android/i.test(navigator.userAgent),
    isiPhone: /iPhone/i.test(navigator.userAgent),
    isiPad: /iPad/i.test(navigator.userAgent),
    isiPod: /iPod/i.test(navigator.userAgent),
    isBlackBerry: /BlackBerry/i.test(navigator.userAgent),
    iswebOS: /webOS/i.test(navigator.userAgent),
    isWinCE: /windows ce/i.test(navigator.userAgent),
    isWinMobile: /windows mobile/i.test(navigator.userAgent),
    isApple: /iPhone|iPad|iPod/i.test(navigator.userAgent),
    isMobile: /Android|webOS|iPhone|iPad|iPod|BlackBerry/i
        .test(navigator.userAgent),
    isPacer: location.href.toLowerCase().indexOf("loginusercd") >= 0,
    is: function (dev) {
        return eval('/' + dev + '/i').test(navigator.userAgent);
    }
}
// 端末がPCかスマホ
function Mobile() {
	var sUserAgent = navigator.userAgent.toLowerCase();
	var bIsIpad = sUserAgent.match(/ipad/i) == "ipad";
	var bIsIphoneOs = sUserAgent.match(/iphone os/i) == "iphone os";
	var bIsMidp = sUserAgent.match(/midp/i) == "midp";
	var bIsUc7 = sUserAgent.match(/rv:1.2.3.4/i) == "rv:1.2.3.4";
	var bIsUc = sUserAgent.match(/ucweb/i) == "ucweb";
	var bIsAndroid = sUserAgent.match(/android/i) == "android";
	var bIsCE = sUserAgent.match(/windows ce/i) == "windows ce";
	var bIsWM = sUserAgent.match(/windows mobile/i) == "windows mobile";
	var bIsPacer = location.href.indexOf("LoginUserCd") >= 0;
	if (bIsPacer) {
		return "Pacer";
	} else if (bIsIpad || bIsMidp || bIsUc7 || bIsUc || bIsCE || bIsWM) {
		return "Mobile";
	} else if (bIsIphoneOs) {
		return "Iphone";
	} else if (bIsAndroid) {
		return "Android";
	} else {
		return "PC";
	}
}

// 画面リロード
function Refresh() {
    window.location.reload();
}
// 前ページに
function goBack() {
    window.history.go(-1);
}
// 前ページに。※URL変更
function goBackByFresh() {
    window.location.href=document.referrer;
}

// ○ページへ
// goPage('') goPage('login') 
function goPage(pageName) {
    window.location.href = encodeURI('./'+pageName);
}

// ローカルにデータを保存
function setLocalData(name, value) {
    localStorage[name] = value;
}
// ローカルからデータを取得
function getLocalData(name) {
    return localStorage[name];
}
// ローカルのデータを削除
function delLocalData(name) {
    localStorage.removeItem(name);
}
/**
* 00,000
*/
var currency = function (val) {
    if (val) {
        val = val + '';
        //	val = val.replace(/^&nbsp;/g,"").replace(/,/g,"");
        var rex = /\d{1,3}(?=(\d{3})+$)/g;
        return val.replace(/^(-?)(\d+)((\.\d+)?)$/, function (s, s1, s2,
            s3) {
            //	return '\\' + s1 + s2.replace(rex, '$&,') + s3;
            return s1 + s2.replace(rex, '$&,');
        })
    } else {
        return val;
    }
};
// ひらかなをカタカナに変換する
var jpConvert = function (obj) {
    try {
        var name = obj.split('');
        obj = '';
        for (var i = 0; i < name.length; i++) {
            var chara = name[i].charCodeAt();
            if ((chara >= 12353 && chara <= 12438) || chara == 12445 || chara == 12446) {
                obj = obj + String.fromCharCode(chara + 96);
            } else {
                obj = obj + name[i];
            }
        }
        return obj;
    } catch (e) {

    }
}
