import React, { useState, useEffect, useRef } from 'react';
import styled from '@emotion/styled';
import axios from 'axios';
import Cookies from 'js-cookie';

axios.defaults.withCredentials = true;

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

const ChatContainer = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 1rem;
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  margin-bottom: 1rem;
  padding: 1rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const MessageBubble = styled.div<{ isUser: boolean }>`
  max-width: 70%;
  margin: ${({ isUser }) => (isUser ? '0.5rem 0 0.5rem auto' : '0.5rem auto 0.5rem 0')};
  padding: 0.8rem 1rem;
  border-radius: 1rem;
  background-color: ${({ isUser }) => (isUser ? '#4a90e2' : '#e9ecef')};
  color: ${({ isUser }) => (isUser ? 'white' : 'black')};
`;

const InputContainer = styled.form`
  display: flex;
  gap: 1rem;
`;

const Input = styled.input`
  flex: 1;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  &:focus {
    outline: none;
    border-color: #4a90e2;
  }
`;

const SendButton = styled.button`
  padding: 0.8rem 1.5rem;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;

  &:hover {
    background-color: #357abd;
  }

  &:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
`;

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [totalCost, setTotalCost] = useState<number>(0);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Load chat history and total cost when component mounts
    const loadChatHistoryAndCost = async () => {
      try {
        const [historyResponse, costResponse] = await Promise.all([
          axios.get('/api/chat/history'),
          axios.get('/api/chat/cost')
        ]);
        setMessages(historyResponse.data.messages);
        setTotalCost(costResponse.data.total_cost);
      } catch (error) {
        console.error('Error loading chat history or cost:', error);
      }
    };

    loadChatHistoryAndCost();
  }, []);

  useEffect(() => {
    // Scroll to bottom when messages update
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post('/api/chat/message', {
        content: userMessage
      });

      // Store the session ID in cookies
      Cookies.set('session_id', response.data.session_id);

      setMessages(prev => [...prev, ...response.data.messages]);
      setTotalCost(response.data.total_cost);
    } catch (error) {
      console.error('Error sending message:', error);
      // You might want to show an error message to the user here
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ChatContainer>
      <div>
        <h2>Total Cost: ${totalCost.toFixed(2)}</h2>
      </div>
      <MessagesContainer>
        {messages.map((message, index) => (
          <MessageBubble key={index} isUser={message.role === 'user'}>
            {message.content}
          </MessageBubble>
        ))}
        <div ref={messagesEndRef} />
      </MessagesContainer>
      <InputContainer onSubmit={handleSubmit}>
        <Input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          disabled={isLoading}
        />
        <SendButton type="submit" disabled={!input.trim() || isLoading}>
          {isLoading ? 'Sending...' : 'Send'}
        </SendButton>
      </InputContainer>
    </ChatContainer>
  );
};

export default Chat; 