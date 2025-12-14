//温度参数设置
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

//实时聊天界面渲染
function updateChatWindow(message, person) {
    const chat_window = document.getElementById("chat_window");
    if (!chat_window || message === undefined || message === null) return;

    const chat_block = document.createElement('div');
    // 使用 data.js 中的 bot 变量判断
    chat_block.className = (person === bot) ? 'chat_ai_block' : 'chat_person_block';

    const user_avatar_url = 'Webmaker/frontend/assets/user_avatar.jpg';
    const ai_avatar_url = 'Webmaker/frontend/assets/ai_avatar.jpg';

    const avatar = document.createElement('img');
    avatar.className = (person === bot) ? 'bot_avator' : 'person_avator';
    avatar.src = (person === bot) ? ai_avatar_url : user_avatar_url;
    avatar.width = 40;
    avatar.height = 40;

    const chat_bubble = document.createElement('div');
    chat_bubble.className = "chat_bubble";
    chat_bubble.textContent = message;

    const timestamps = document.createElement('div');
    timestamps.className = "timestamps";
    timestamps.textContent = new Date().toLocaleTimeString();

    if (person === bot) {
        chat_block.appendChild(avatar);
        chat_block.appendChild(chat_bubble);
    } else {
        chat_block.appendChild(chat_bubble);
        chat_block.appendChild(avatar);
    }
    chat_block.appendChild(timestamps);
    chat_window.appendChild(chat_block);
    chat_window.scrollTop = chat_window.scrollHeight;
}
//获取AI回复
async function getResponse(message) {
    if (!message) return false;
    try {
        const AIResponse = await fetch('http://127.0.0.1:8000/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                role: "User", // 明确使用 User 作为请求角色，不依赖全局 person
                question: message,
                numbers: cycle_token,
                status: 200
            })
        });
        if (!AIResponse.ok) {
            console.error("AI response not ok:", AIResponse.status);
            return false;
        }
        const data = await AIResponse.json();
        AIMessage = data.response;
        AITokenUsed = data.token_used;
        console.log("AI response:", AIMessage);
        //updateProgressBar(Number(AITokenUsed) || 0);
        updateChatWindow(AIMessage, "AI");
        cycle_token += 1;
        return true;
    } catch (error) {
        console.error("Error get response:", error);
        return false;
    }
}
//处理用户输入消息（使用局部 person，await AI 回复以减少竞态）
async function processMessage(input) {
    const chat_message_input = input || document.getElementById("user_input");
    if (!chat_message_input) return;
    const chat_message = String(chat_message_input.value.trim());
    if (!chat_message) return;
    chat_message_input.value = "";
    console.log("User input message:", chat_message);
    const currentPerson = "User"; // 使用局部变量，不覆盖全局 person
    updateChatWindow(chat_message, currentPerson);
    await getResponse(chat_message);
}
//发送消息按钮和回车键绑定事件
async function sendMessage() {
    const send_message_button = document.getElementById("send_button");
    const chat_message_input = document.getElementById("user_input");
    if (!chat_message_input) return;
    if (!send_message_button) return;
    send_message_button.addEventListener('click', () => {
        processMessage(chat_message_input);
    });
    chat_message_input.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            processMessage(chat_message_input);
        }
    });
}
//保存聊天记录
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
//新建聊天和历史聊天记录界面渲染
function createNewChat() {
}
//获取当前时间并显示在界面上
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
    const progressBar = document.getElementById('used_tokens');
    if (!progressBar) return;
    total_used_tokens = (typeof total_used_tokens === 'number') ? total_used_tokens + (Number(new_used_tokens) || 0) : (Number(new_used_tokens) || 0);
    const allowedMax = (typeof max_tokens === 'number' && max_tokens > 0) ? max_tokens : 1000;
    const percentage = Math.min(100, (total_used_tokens / allowedMax) * 100);
    progressBar.style.width = percentage + '%';
    const progressText = document.getElementById('used_tokens_text');
    if (progressText) progressText.innerHTML = 'Used Tokens: ' + total_used_tokens.toFixed(2);
}
document.addEventListener('DOMContentLoaded', () => {
    setTemperature();
    getCurrentTime();
    sendMessage();
    saveTalk();
    updateProgressBar(cycle_token);
    setInterval(getCurrentTime, 1000);
});