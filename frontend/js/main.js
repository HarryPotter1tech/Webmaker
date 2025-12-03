
function setTemperature() {
    const temperature_text = document.getElementById("temperature");// 获取对应id的内容
    if (!temperature_text) return;//如果找不到对应id
    temperature_text.addEventListener('click', () => {
        if (temperature_at >= 0 && temperature_at < 1.0) {
            temperature_at += 0.1;
            if (temperature_at >= 1.0) {
                temperature_at = 0.0;
            }
        }
        temperature_text.innerHTML = "Temperature: " + temperature_at.toFixed(1);
    });
}
function updateChatWindow(message, person) {

}
async function getResponse(message) {
    if (message === "") {
        return false;
    }
    else {
        try {
            AIResponse = await fetch('http://127.0.0.1:8000/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    role: person,
                    question: message,
                    numbers: cycle_token,
                    status: 200
                })
            });
            if (!AIResponse.ok) {
                console.error("AI response not ok: ", AIResponse.status);
                return false;
            }
            const AIMessage = await AIResponse.json();
            console.log("AI response: ", AIMessage);
            updateProgressBar(AIMessage.token_used);
            updateChatWindow(AIMessage.response, bot);
            cycle_token += 1;
            return true;
        } catch (error) {
            console.error("Error get response: ", error);
            return false;
        }
    }
}
function processMessage() {
    chat_message = chat_message_input.value.trim();
    chat_message_input.value = "";
    console.log("User input message: " + chat_message);
    updateChatWindow(chat_message, person);
    getResponse(chat_message);
}
async function sendMessage() {

    const send_message_button = document.getElementById("send_button");
    const chat_message_input = document.getElementById("user_input");
    if (!chat_message_input) return;
    if (!send_message_button) return;
    send_message_button.addEventListener('click', () => {
        processMessage();
    });
    chat_message_input.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {//keydown事件回调需要使用事件对象
            event.preventDefault();
            processMessage();
        }
    });
}
async function saveTalk() {
    const save_talk_button = document.getElementById("save_talk");
    if (!save_talk_button) return;
    save_talk_button.addEventListener('click', () => {
        // 在用户点击事件内直接导航/打开到后端下载地址，添加时间戳防缓存
        const backendUrl = 'http://127.0.0.1:8000/download_chat_history?t=' + Date.now();
        // 选择在当前页下载（location.href）或新标签打开（window.open）
        // location.href = backendUrl;
        window.open(backendUrl, '_blank');
    });
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
    if (!month || !day || !hour || !minute || !second) return;
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
    if (!progressText) return;
    progressText.innerHTML = 'Used Tokens: ' + total_used_tokens.toFixed(2);
}
document.addEventListener('DOMContentLoaded', () => {
    setTemperature();
    getCurrentTime();
    sendMessage();
    saveTalk();
    updateProgressBar(cycle_token);
    setInterval(getCurrentTime, 1000);
});