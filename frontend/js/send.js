(function () {
    const textarea = document.querySelector('.user-input');
    const btn = document.querySelector('.send-btn');
    const chat = document.querySelector('#chat-container');
    if (!textarea || !btn || !chat) {
        console.warn('缺少 .user-input / .send-btn / #chat-container，请检查 HTML');
        return;
    }

    function createMessageElement(text, sender) {
        const outer = document.createElement('div');
        outer.className = `message ${sender}`;
        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        const txt = document.createElement('div');
        txt.className = 'text';
        txt.textContent = text;
        const meta = document.createElement('div');
        meta.className = 'meta';
        meta.textContent = new Date().toLocaleTimeString();
        bubble.appendChild(txt);
        bubble.appendChild(meta);
        if (sender === 'user') {
            outer.appendChild(bubble);
        } else {
            outer.appendChild(bubble);
        }
        return outer;
    }

    function scrollToBottom() { chat.scrollTop = chat.scrollHeight; }

    let sending = false;
    async function sendMessage() {
        if (sending) return;
        const raw = textarea.value;
        if (!raw.trim()) return;
        const message = raw.trim();

        // 渲染用户消息
        const userEl = createMessageElement(message, 'user');
        chat.appendChild(userEl);
        scrollToBottom();

        textarea.value = '';
        btn.disabled = true;
        sending = true;

        // 发请求到后端（用后端实际地址）
        try {
            const res = await fetch('http://127.0.0.1:8000/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });

            if (!res.ok) {
                const text = await res.text().catch(() => '');
                console.error('后端错误', res.status, res.statusText, text);
                const errEl = createMessageElement('发送失败（后端返回错误）', 'assistant');
                errEl.classList.add('failed');
                chat.appendChild(errEl);
                scrollToBottom();
                return;
            }

            const data = await res.json().catch(() => null);
            const reply = data && (data.response || data.reply) ? (data.response || data.reply) : (typeof data === 'string' ? data : '[无回复]');
            const botEl = createMessageElement(reply, 'assistant');
            chat.appendChild(botEl);
            scrollToBottom();
        } catch (err) {
            console.error('请求失败', err);
            const errEl = createMessageElement('网络错误，无法连接后端', 'assistant');
            errEl.classList.add('failed');
            chat.appendChild(errEl);
            scrollToBottom();
        } finally {
            sending = false;
            btn.disabled = false;
            textarea.focus();
        }
    }

    btn.addEventListener('click', (e) => { e.preventDefault(); sendMessage(); });
    textarea.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
    });
})();
