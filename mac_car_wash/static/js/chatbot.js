class Chatbot {
    constructor() {
        this.isOpen = false;
        this.messages = [];
        this.initializeElements();
        this.bindEvents();
    }

    initializeElements() {
        this.chatbot = document.getElementById('chatbot');
        this.trigger = document.getElementById('chatbot-trigger');
        this.toggle = document.getElementById('chatbot-toggle');
        this.input = document.getElementById('chatbot-input');
        this.sendBtn = document.getElementById('chatbot-send');
        this.messagesContainer = document.getElementById('chatbot-messages');
    }

    bindEvents() {
        this.trigger?.addEventListener('click', () => this.toggleChat());
        this.toggle?.addEventListener('click', () => this.toggleChat());
        this.sendBtn?.addEventListener('click', () => this.sendMessage());
        this.input?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
    }

    toggleChat() {
        this.isOpen = !this.isOpen;
        if (this.chatbot) {
            this.chatbot.style.display = this.isOpen ? 'flex' : 'none';
        }
        if (this.trigger) {
            this.trigger.style.display = this.isOpen ? 'none' : 'block';
        }
    }

    async sendMessage() {
        const message = this.input?.value.trim();
        if (!message) return;

        // Add user message
        this.addMessage(message, 'user');
        this.input.value = '';

        // Show typing indicator
        this.showTyping();

        try {
            const response = await fetch('/api/chatbot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message })
            });

            const data = await response.json();
            
            // Remove typing indicator and add bot response
            setTimeout(() => {
                this.hideTyping();
                this.addMessage(data.response, 'bot');
            }, 1000);

        } catch (error) {
            this.hideTyping();
            this.addMessage('Sorry, I encountered an error. Please contact us directly at +971 5011 34356', 'bot');
        }
    }

    addMessage(message, sender) {
        if (!this.messagesContainer) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        messageDiv.innerHTML = `<p>${message}</p>`;

        this.messagesContainer.appendChild(messageDiv);
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    showTyping() {
        if (!this.messagesContainer) return;

        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing';
        typingDiv.innerHTML = '<p>Typing...</p>';
        typingDiv.id = 'typing-indicator';

        this.messagesContainer.appendChild(typingDiv);
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    hideTyping() {
        const typing = document.getElementById('typing-indicator');
        if (typing) {
            typing.remove();
        }
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new Chatbot();
});
