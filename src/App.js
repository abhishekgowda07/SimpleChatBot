import React, { useState, useEffect } from 'react';
import axios from 'axios';

const App = () => {
  const [chatMessages, setChatMessages] = useState([]);
  const [userInput, setUserInput] = useState('');

  useEffect(() => {
    // Scroll to the bottom of the chat window whenever new messages are added
    const chatWindow = document.getElementById('chat-window');
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }, [chatMessages]);

  const handleUserInput = async () => {
    if (userInput.trim() !== '') {
      setChatMessages((prevMessages) => [
        ...prevMessages,
        { content: userInput, sender: 'user' },
      ]);

      try {
        const response = await axios.post('http://localhost:5000/chatbot', { user_input: userInput });
        console.log(response.data.response);
        setChatMessages((prevMessages) => [
          ...prevMessages,
          {
            content: response.data.response, sender: 'chatbot' },
        ]);
      } catch (error) {
        console.error('Chatbot Error:', error);
      }

      setUserInput('');
    }
  };

  return (
    <div className="app">
      <h1>My Chatbot App</h1>

      <div id="chat-window" className="chat-window">
        {chatMessages.map((message, index) => (
          <div
            key={index}
            className={`message ${message.sender === 'user' ? 'user' : 'chatbot'}`}
          >
            {message.content}
          </div>
        ))}
      </div>

      <div className="user-input">
        <input
          type="text"
          placeholder="Type a message..."
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              handleUserInput();
            }
          }}
        />
        <button onClick={handleUserInput}>Send</button>
      </div>
    </div>
  );
};

export default App;
