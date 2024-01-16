import React, { useState, useEffect, useRef } from "react";

import { ChatList } from "./chat-list";
import { ChatWindow } from "./chat-window";
import { getUsers } from "../../utils/api";
import { getChat } from "../../utils/api";

import styles from "./chat-page.module.css";

export const ChatPage = () => {
  const [selectedUserId, setSelectedUserId] = useState('0');
  const [messages, setMessages] = useState([]);
  const chatSocketRef = useRef(null);
  const [users, setUsers] = useState([]);
  

  useEffect(() => {
    if (selectedUserId) {
      getChat(selectedUserId, localStorage.getItem("auth_token"))
      .then((chatHistory) => {
        console.log(chatHistory);
        const newMessages = chatHistory.results.map((messageData) => `${messageData.username}: ${messageData.message}`);
        console.log(newMessages);
        setMessages(newMessages);
      })
      .catch((error) => {
        console.error("Ошибка при загрузке истории чата:", error);
        setMessages([]);
      });
    }
    getUsers()
      .then((data) => {
        setUsers(data.results);
      })
      .catch((error) => {
        console.error("Ошибка при получении списка пользователей:", error);
      });

    // Создание WebSocket-подключения
    const token = localStorage.getItem("auth_token");
    const socketUrl =
      (window.location.protocol === "https:" ? "wss://" : "ws://") +
      window.location.host +
      "/ws/chat/" +
      (selectedUserId ? selectedUserId : '0') +
      `/?token=${token}`;

    chatSocketRef.current = new WebSocket(socketUrl);
    setMessages([]);
    chatSocketRef.current.onmessage = function (e) {
      const data = JSON.parse(e.data);
      const newMessages = data.results.map((messageData) => `${messageData.username}: ${messageData.message}`);
      setMessages((prevMessages) => [
        ...prevMessages,
        ...newMessages
      ]);
    };

    chatSocketRef.current.onclose = function (e) {
      console.error("Chat socket closed unexpectedly");
    };

    return () => {
      chatSocketRef.current.close();
    };
  }, [selectedUserId]);

  const handleUserClick = (userId) => {
    setSelectedUserId(userId);
    setMessages([]); // Очищаем список сообщений при выборе нового пользователя
  };

  const handleGeneralChatClick = () => {
    setSelectedUserId(null);
    setMessages([]);
  };

  const handleSendMessage = (message) => {
    chatSocketRef.current.send(JSON.stringify({ message }));
  };

  return (
    <div className={styles.container}>
      <div>
        <ChatList
          users={users}
          onUserClick={handleUserClick}
          onGeneralChatClick={handleGeneralChatClick}
        />
      </div>
      <div>
        {selectedUserId !== null && (
          <ChatWindow
            messages={messages}
            userId={selectedUserId}
            onSubmitMessage={handleSendMessage}
          />
        )}
      </div>
    </div>
  );
};