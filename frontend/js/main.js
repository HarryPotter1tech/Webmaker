function setTemperature() {
}
function sendMessage() {
}
function saveTalk() {
}
function createNewChat() {
}
function openHistoryChat() {
}
function getCurrentTime() {
    var month = document.getElementById('month');
    var day = document.getElementById('day');
    var hour = document.getElementById('hour');
    var minute = document.getElementById('minute');
    var second = document.getElementById('second');
    var date = new Date();
    var _month = date.getMonth() + 1;
    var _day = date.getDate();
    var _hour = date.getHours();
    var _minute = date.getMinutes();
    var _second = date.getSeconds();

    if (_month < 10) _month = '0' + _month;
    if (_day < 10) _day = '0' + _day;
    if (_hour < 10) _hour = '0' + _hour;
    if (_minute < 10) _minute = '0' + _minute;
    if (_second < 10) _second = '0' + _second;
    month.innerHTML = _month;
    day.innerHTML = _day;
    hour.innerHTML = _hour;
    minute.innerHTML = _minute;
    second.innerHTML = _second;
}
let total_used_tokens = 0;
var max_tokens = 100000;
function updateProgressBar(new_used_tokens) {
    var progressBar = document.getElementById('used_tokens');
    total_used_tokens += new_used_tokens;
    if (total_used_tokens <= max_tokens) {
        var percentage = (total_used_tokens / max_tokens) * 100;
    } else {
        var percentage = 100;
    }
    progressBar.style.width = percentage + '%';
    var progressText = document.getElementById('used_tokens_text');
    progressText.innerHTML = 'Used Tokens: ' + total_used_tokens;
}
setInterval(getCurrentTime, 1000);
getCurrentTime(); 