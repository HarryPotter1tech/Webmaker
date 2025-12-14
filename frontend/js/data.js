var temperature_at = 0.0;
var total_used_tokens = 0;
const max_tokens = 100000;
var cycle_token = 0;
var chat_message = "";// 发送的消息内容

var person = "User";
var bot = "AI";
var restoringHistory = false; // 标记是否正在恢复历史记录
var chat_message_array = [];
const CHAT_HISTORY_MAX = 200;