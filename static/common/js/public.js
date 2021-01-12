/**
 * Created by PhpStorm.
 * User: AlbertLi
 * Date: 2020/4/18
 * Time: 17:12
 */
/*防止backspace回退*/
window.onload = function (e) {
    //禁止后退键 作用于Firefox、Opera
    document.onkeypress = backspace;
    //禁止后退键  作用于IE、Chrome
    document.onkeydown = backspace;
}

function backspace(e) {
    var ev = e || window.event;//获取event对象
    var obj = ev.target || ev.srcElement;//获取事件源
    var t = obj.type || obj.getAttribute('type');//获取事件源类型
    if (ev.keyCode == 8 && t != "password" && t != "text" && t != "textarea") {
        return false;
    }
}